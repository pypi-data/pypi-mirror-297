from collections import defaultdict
from copy import deepcopy
import os
from typing import Any, Dict, Final, List, Optional

import requests

from .api import KDBAIException
from .constants import p_type_mapping, q_type_mapping, VdbScopes
from .table import TablePyKx


os.environ['IGNORE_QHOME'] = '1'
os.environ['PYKX_NOQCE'] = '1'
os.environ['SKIP_UNDERQ'] = '1'
os.environ['QARGS'] = '--unlicensed'
import pykx as kx  # noqa: E402


class SessionPyKx:
    """Session represents a connection to a KDB.AI instance using QIPC connection."""
    def __init__(self,
                 api_key: Optional[str] = None,
                 *,
                 host: Optional[str] = None,
                 port: Optional[int] = None,
                 endpoint: Optional[str] = None):
        """Create a QIPC API connection to a KDB.AI endpoint.

        Args:
            api_key (str): API Key to be used for authentication.
            endpoint (str): Server endpoint to connect to.
            host (str): Server host.
            port (int): Server port number.

        Example:
            Open a session on a custom KDB.AI instance on http://localhost:8082:

            ```python
            session = kdbai.Session(endpoint='http://localhost:8082')
            session = kdbai.session.SessionPyKx(host='localhost' port=8082)
            ```
        """
        self.api_key = api_key
        if host is None or port is None:
            if endpoint is None:
                raise KDBAIException('Either host and port or endpoint must be provided')
            else:
                url = requests.utils.urlparse(endpoint)
                host = url.hostname
                port = url.port
        self.host = host
        self.port = port
        try:
            self.gw = kx.SyncQConnection(host=host, port=port, no_ctx=True)
        except Exception as e:
            raise KDBAIException(f'Error during creating connection: {e}')
        self.operator_map: Final[Dict[str, Any]] = self.gw(kx.SymbolAtom('getSupportedFilters'), None).py()

    def version(self) -> dict:
        """Retrieve version information from server"""
        return self.gw(kx.SymbolAtom('getVersion'), None).py()

    def meta(self, scope: VdbScopes = VdbScopes.MetaManaged) -> dict:
        """Retrieves tables' metadata from server

        Returns:
            Dictionary containing metadata information.
        """
        try:
            data = self.gw(kx.SymbolAtom('getVdbMeta'), None).py()
            result = dict()
            for key, tables in data.items():
                temp = []
                for name, schema in tables.items():
                    schema['vdb'] = name[0]
                    temp.append(schema)
                result[key] = temp
            if scope == VdbScopes.ALL:
                return result
            return {scope.value: result[scope.value]}

        except Exception as e:
            raise KDBAIException(f'Failed to retrieve table metadata: {e}')

    def tables(self, scope: VdbScopes = VdbScopes.MetaManaged) -> List[TablePyKx]:
        """Retrieve the list of tables.

        Returns:
            A list of Table instances representing the existing tables.
        """
        data = self.meta(scope)

        tables: List[TablePyKx] = []
        for scope, schemas in data.items():
            for schema in schemas:
                tables.append(TablePyKx(name=schema['vdb'], schema=schema, session=self, scope=VdbScopes(scope)))

        return tables

    def list(self, scope: VdbScopes = VdbScopes.MetaManaged) -> List[str]:
        """Retrieve the list of tables.

        Returns:
            A list of strings with the names of the existing tables.

        Example:
            ```python
            session.list()
            ["trade", "quote"]
            ```
        """
        return [t.name for t in self.tables(scope)]

    def table(self, name: str, scope: VdbScopes = VdbScopes.MetaManaged) -> TablePyKx:
        """Retrieve an existing table which was created in the previous session.

        Args:
            name (str): Name of the table to retrieve.
            scope (VdbScopes): The vdb scope of the table.

        Returns:
                A `Table` object representing the KDB.AI table.
        """
        if scope == VdbScopes.ALL:
            raise KDBAIException('You must select one scope to fetch table from')
        data = self.meta(scope=scope)
        for schema in data[scope.value]:
            if schema['vdb'] == name:
                return TablePyKx(name=name, schema=schema, session=self, scope=scope)

        raise KDBAIException(f'Table "{name}" does not exist')

    def create_table(self,
                     name: str,
                     schema: dict,
                     scope: VdbScopes = VdbScopes.MetaManaged,
                     default_result_type: str = 'pd') -> TablePyKx:
        """Create a table with a schema

        Args:
            name (str): Name of the table to create.
            schema (dict): The index table's properties
            scope (VdbScopes): The vdb scope of the table.
            default_result_type (str): data type to convert result into in search and query (pd|py|q)

        Returns:
                A newly created `Table` object based on the schema.

        Example:
            nometa = {"partn": False, "idxParams": {"type": "hnsw", "dims": 25}}
            managed_meta = {
                "partn": False,
                "emdCol": "embeddings",
                "idxParams": {"type": "hnsw", "dims": 25},
            }
            meta_fromref = {
                "partn": False,
                "emdCol": "embeddings",
                "vdbMetaPath": "/tmp",
                "idxParams": {"type": "hnsw", "dims": 25},
            }
            self.table_nometa = self.session.create_table(
                name="table_nometa", schema=nometa, scope=VdbScopes.NoMeta
            )
            self.table_managed_meta = self.session.create_table(
                name="table_managed_meta", schema=managed_meta, scope=VdbScopes.MetaManaged
            )
            self.table_meta_fromref = self.session.create_table(
                name="table_meta_fromref", schema=meta_fromref, scope=VdbScopes.MetaFromRef
            )
        """
        schema = deepcopy(schema)
        columns = schema.pop('columns', None)
        if columns is not None:
            table_schema = defaultdict(list)
            indexes = []
            is_tsc = False
            for column in columns:
                table_schema['c'].append(column['name'])
                table_schema['t'].append(self._get_q_type(column).encode())
                table_schema['a'].append('')
                if 'vectorIndex' in column or 'sparseIndex' in column:
                    indexes.append(column)
                    if 'embedding' in column:
                        is_tsc = True

            if indexes:
                # backward compatibility
                schema = {'partn': False}
                for id, index in enumerate(indexes):
                    if index.get('vectorIndex', dict()).get('type') != 'tss':
                        if 'emdCol' not in schema:
                            schema['emdCol'] = [index['name']]
                        else:
                            schema['emdCol'].append(index['name'])

                        if 'idxParams' not in schema:
                            schema['idxParams'] = []
                        if 'vectorIndex' in index:
                            schema['idxParams'].append({'name': f'defaultIndexName{id}', **index['vectorIndex']})
                        else:
                            schema['idxParams'].append({'name': f'defaultIndexName{id}',
                                                        'sparse': True,
                                                        **index['sparseIndex']})
                        if is_tsc:
                            if 'embedding' not in schema:
                                schema['embedding'] = [index.get('embedding', kx.SymbolAtom(""))]
                            else:
                                schema['embedding'].append(index.get('embedding', kx.SymbolAtom("")))

                    else:
                        schema['searchCol'] = index['name']
            if table_schema:
                schema['schema'] = dict(table_schema)

        if 'partn' not in schema:
            schema['partn'] = False
        schema['vdb'] = name
        schema['vdbType'] = scope.category



        try:
            result = self.gw(kx.SymbolAtom('vdbCreate'), schema)
        except Exception as e:
            raise KDBAIException(f'Failed to create the new table: {e}')
        if isinstance(result, kx.CharVector):
            raise KDBAIException(f'Failed to create the new table: {result.py().decode("utf-8")}')

        result = result.py()
        schema = result[(name,)]
        schema['vdb'] = name

        return TablePyKx(name=name, schema=schema, session=self, scope=scope, default_result_type=default_result_type)

    @staticmethod
    def _get_q_type(column: dict) -> str:
        def _get_type_form_dict(column):
            if 'qtype' in column:
                if column['qtype'] not in q_type_mapping:
                    raise KDBAIException(f'Unsupported column qtype: {column["qtype"]}')
                return q_type_mapping[column['qtype']]
            elif 'pytype' in column:
                if column['pytype'] not in p_type_mapping:
                    raise KDBAIException(f'Unsupported column pytype: {column["pytype"]}')
                return p_type_mapping[column['pytype']]
            raise KDBAIException('qtype or pytype must be provided')

        if 'sparseIndex' in column:
            return p_type_mapping['dict']
        if 'vectorIndex' in column:
            tss = column['vectorIndex'].get('type') == 'tss'
            atom_or_list = '' if tss else 's'
            default_type = 'float64' if tss else 'float32'
            if 'pytype' in column:
                if column['pytype'] in ['float32', 'float64']:
                    column['pytype'] = f"{column['pytype']}{atom_or_list}"
                return _get_type_form_dict(column)
            if 'qtype' in column:
                if column['qtype'] in ['real', 'float']:
                    column['qtype'] = f"{column['qtype']}{atom_or_list}"
                return _get_type_form_dict(column)
            return p_type_mapping[f"{default_type}{atom_or_list}"]
        return _get_type_form_dict(column)
