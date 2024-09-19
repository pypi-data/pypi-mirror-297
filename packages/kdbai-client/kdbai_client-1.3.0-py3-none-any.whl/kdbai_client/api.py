from __future__ import annotations

from datetime import datetime
import json
import logging
import os
import time
from typing import Any, Dict, List, Optional
from urllib import parse, request
import urllib.error
from urllib.error import HTTPError
import uuid

import numpy as np
from packaging import version
import pandas as pd


os.environ['IGNORE_QHOME'] = '1'
os.environ['PYKX_NOQCE'] = '1'
os.environ['SKIP_UNDERQ'] = '1'
os.environ['QARGS'] = '--unlicensed'
import pykx as kx  # noqa: E402


MAX_QIPC_SERIALIZATION_SIZE = 10*1024*1024  # 10MB
TABLE_RETRIEVAL_FAILURE = 'Failed to retrieve the list of tables.'
CONTENT_TYPE = {
    'json': 'application/json',
    'octet-stream': 'application/octet-stream'
}

# Minimum datetime/timestmp supported by q/kdb+
MIN_DATETIME = datetime(1707, 9, 22, 0, 12, 43, 145224)
# Maximum datetime/timestamp supported by q/kdb+
MAX_DATETIME = datetime(2262, 4, 11, 23, 47, 16, 854775)


__version__ = None

def _set_version(version):
    global __version__
    __version__ = version


_qtype_to_dtype = dict(
    boolean='bool',
    guid='str',
    byte='uint8',
    short='int16',
    int='int32',
    long='int64',
    real='float32',
    float='float64',
    chars='bytes',
    symbol='str',
    timestamp='datetime64[ns]',
    timespan='timedelta64[ns]'
)

_qtype_to_dtype[' '] = "dict"

_dtype_to_qtype = {v: k for k, v in _qtype_to_dtype.items()}
for key in list(_qtype_to_dtype.keys()):
    _qtype_to_dtype[f'{key}s'] = _qtype_to_dtype[key]

class Session:
    """Session represents a connection to a KDB.AI instance."""

    PROTOCOL  = 'https'
    HOST   = 'localhost'
    PORT   = 443

    READY_PATH          = '/api/v1/ready'
    VERSION_PATH        = '/api/v1/version'
    CONFIG_PATH         = '/api/v1/config/table'
    CREATE_PATH         = '/api/v1/config/table/%s'
    DROP_PATH           = '/api/v1/config/table/%s'
    QUERY_PATH          = '/api/v1/data'
    INSERT_PATH         = '/api/v1/insert'
    TRAIN_PATH          = '/api/v1/train'
    SEARCH_PATH         = '/api/v1/kxi/search'
    HYBRID_SEARCH_PATH  = '/api/v1/kxi/hybridSearch'

    def __init__(
        self,
        api_key = None,
        *,
        endpoint = 'http://localhost:8082'
    ):
        """Create a REST API connection to a KDB.AI endpoint.

        Args:
            api_key (str): API Key to be used for authentication.
            endpoint (str): Server endpoint to connect to.

        Example:
            Open a session on KDB.AI Cloud with an api key:

            ```python
            session = Session(endpoint='YOUR_INSTANCE_ENDPOINT', api_key='YOUR_API_KEY')
            ```

            Open a session on a custom KDB.AI instance on http://localhost:8082:

            ```python
            session = kdbai.api.Session(endpoint='http://localhost:8082')
            ```
        """
        self.api_key = api_key
        self.endpoint = endpoint
        self._check_endpoint()
        self._check_readiness()
        self._check_version()

    def _check_endpoint(self):
        try:
            url = parse.urlparse(self.endpoint)
            assert url.scheme in ('http', 'https')
            assert url.netloc != ''
        except Exception:
            raise KDBAIException(f'Invalid URL: {self.endpoint}.')
        return True

    def _check_readiness(self):
        try:
            assert self._test_readiness()
        except Exception:
            tmp = None if self.api_key is None else self.api_key[:10]
            raise KDBAIException(
                f'Failed to open a session on {self.endpoint} using API key with prefix {tmp}. '
                'Please double check your `endpoint` and `api_key`.'
                )

    def _test_readiness(self):
        result = self._rest_get(Session.READY_PATH)
        return result == 'OK' or json.loads(result) == {'status': 'OK'}

    def _check_version(self):
        if __version__ == 'dev':
            logging.warning(
                'You are running a development version of `kdbai_client`.\n'
                'Compatibility with the KDB.AI server is not guaranteed.'
            )
            return

        try:
            versions = self.version()
        except HTTPError:
            # First version of KDB.AI 0.1.0 does not have the /version API
            # and is compatible with kdbai_client<=0.1.1
            raise KDBAIException(
                f'Your KDB.AI server is not compatible with this client (kdbai_client=={__version__}).\n'
                'Please use kdbai_client==0.1.1.'
            )

        if (version.parse(__version__) < version.parse(versions['clientMinVersion'])
            or (versions['clientMaxVersion'] != 'latest'
                and version.parse(__version__) > version.parse(versions['clientMaxVersion']))):
            raise KDBAIException(
                f'Your KDB.AI server is not compatible with this client (kdbai_client=={__version__}).\n'
                f"Please use kdbai_client >={versions['clientMinVersion']} and <={versions['clientMaxVersion']}."
            )

    def _wait_for_readiness(self, timeout=10):
        i = 0
        while True:
            try:
                if self._test_readiness():
                    break
            except Exception:
                pass
            time.sleep(1)
            i += 1
            if i > timeout:
                return False
        return True

    def version(self) -> dict:
        """Retrieve version information from server"""
        return json.loads(self._rest_get(Session.VERSION_PATH))

    def list(self) -> List[str]:
        """Retrieve the list of tables.

        Returns:
            A list of strings with the names of the existing tables.

        Example:
            ```python
            session.list()
            ["trade", "quote"]
            ```
        """
        try:
            return self._list()
        except Exception:
            raise KDBAIException(TABLE_RETRIEVAL_FAILURE)
        
    def table(self, name: str) -> Table:
        """Retrieve an existing table which was created in the previous session.

        Args:
            name (str): Name of the table to retrieve.

        Returns:
                A `Table` object representing the KDB.AI table.

        Example:
            Retrieve the `trade` table:

            ```python
            session1 = kdbai.Session(endpoint='http://localhost:8082') # Previous session
            table1 = session1.create_table('trade1', schema)           # Create table 'trade1'

            session2 = kdbai.Session(endpoint='http://localhost:8082') # Current session
            table2 = session2.table("trade1")                          # Retrieve table 'trade1'
            ```
        """
        return Table(name=name, session=self)

    def create_table(self, name, schema) -> Table:
        """Create a table with a schema

        Args:
            name (str): Name of the table to create.
            schema (dict): Schema of the table to create. This schema must contain a list of columns. All columns
                must have a `pytype` specified except the column of vectors.
                One column of vector embeddings may also have a `vectorIndex` attribute with the configuration of the
                index for similarity search - this column is implicitly an array of `float32`.

        Returns:
                A newly created `Table` object based on the schema.

        Raises:
            KDBAIException: Raised when a error happens during the creation of the table.

        Example Flat Index:
            ```python
            schema = {'columns': [{'name': 'id', 'pytype': 'str'},
                                  {'name': 'tag', 'pytype': 'str'},
                                  {'name': 'text', 'pytype': 'bytes'},
                                  {'name': 'embeddings',
                                   'vectorIndex': {'dims': 1536, 'metric': 'L2', 'type': 'flat'}}]}
            table = session.create_table('documents', schema)
            ```

        Example qFlat Index:
            ```python
            schema = {'columns': [{'name': 'id', 'pytype': 'str'},
                                  {'name': 'tag', 'pytype': 'str'},
                                  {'name': 'text', 'pytype': 'bytes'},
                                  {'name': 'embeddings',
                                   'vectorIndex': {'dims': 1536, 'metric': 'L2', 'type': 'qFlat'}}]}
            table = session.create_table('documents', schema)
            ```

        Example IVF Index:
            ```python
            schema = {'columns': [{'name': 'id', 'pytype': 'str'},
                                  {'name': 'tag', 'pytype': 'str'},
                                  {'name': 'text', 'pytype': 'bytes'},
                                  {'name': 'embeddings',
                                   'vectorIndex': {'trainingVectors': 1000,
                                                   'metric': 'CS',
                                                   'type': 'ivf',
                                                   'nclusters': 10}}]}
            table = session.create_table('documents', schema)
            ```

        Example IVFPQ Index:
            ```python
            schema = {'columns': [{'name': 'id', 'pytype': 'str'},
                                  {'name': 'tag', 'pytype': 'str'},
                                  {'name': 'text', 'pytype': 'bytes'},
                                  {'name': 'embeddings',
                                   'vectorIndex': {'trainingVectors': 5000,
                                                   'metric': 'L2',
                                                   'type': 'ivfpq',
                                                   'nclusters': 50,
                                                   'nsplits': 8,
                                                   'nbits': 8}}]}
            table = session.create_table('documents', schema)
            ```

        Example HNSW Index:
            ```python
            schema = {'columns': [{'name': 'id', 'pytype': 'str'},
                                  {'name': 'tag', 'pytype': 'str'},
                                  {'name': 'text', 'pytype': 'bytes'},
                                  {'name': 'embeddings',
                                   'vectorIndex': {'dims': 1536,
                                                   'metric': 'IP',
                                                   'type': 'hnsw',
                                                   'efConstruction' : 8, 'M': 8}}]}
            table = session.create_table('documents', schema)
            ```

        Example Sparse Index:
            ```python
            schema = {'columns': [{'name': 'id', 'pytype': 'str'},
                                  {'name': 'tag', 'pytype': 'str'},
                                  {'name': 'text', 'pytype': 'bytes'},
                                  {'name': 'embeddings',
                                   'sparseIndex': {'k': 1.25,
                                                   'b': 0.75}}]}
            table = session.create_table('documents', schema)
            ```

        Example Flat with Sparse Index:
            ```python
            schema = {'columns': [{'name': 'id', 'pytype': 'str'},
                                  {'name': 'tag', 'pytype': 'str'},
                                  {'name': 'text', 'pytype': 'bytes'},
                                  {'name': 'denseCol',
                                   'vectorIndex': {'dims': 1536,
                                                   'metric': 'L2',
                                                   'type': 'flat'}},
                                  {'name': 'sparseCol',
                                   'sparseIndex': {'k': 1.25,
                                                   'b': 0.75}}]}
            table = session.create_table('documents', schema)
            ```

        """
        try:
            schema = self._format_schema_to_q(schema)
            self._create_table(name, schema)
            if self._wait_for_readiness(timeout=10):
                return Table(name=name, session=self)
            else:
                raise KDBAIException(f'Failed to create the new table named {name} with schema {schema}'
                                     ' because of timeout expiration.')
        except urllib.error.HTTPError as e:
            raise KDBAIException(f'Failed to create the new table named {name} with schema {schema}.', e=e)
        except KDBAIException as e:
            raise e
        except Exception:
            raise KDBAIException(f'Failed to create the new table named {name} with schema {schema}.')

    def _format_schema_to_q(self, schema):
        out = {}
        out['type'] = 'splayed'
        out['columns'] = []
        for column in schema['columns']:
            out_col = self._process_out_column(column)
            out['columns'].append(out_col)
        return out

    def _process_out_column(self, column):

        allowed_col_keys = ['name', 'pytype', 'qtype', 'vectorIndex', 'sparseIndex', 'embedding']
        if not(all(key in allowed_col_keys for key in column.keys())):
            raise KDBAIException('Invalid column key provided. Only these are allowed: '+', '.join(allowed_col_keys))

        out_col = dict(name=column['name'])

        if 'qtype' in column:
            if column['qtype'] not in _qtype_to_dtype:
                raise KDBAIException(f'Unsupported column qtype: {column["qtype"]}')
            out_col['type'] = column['qtype']
        elif 'pytype' in column:
            if column['pytype'] not in _dtype_to_qtype:
                raise KDBAIException(f'Unsupported column pytype: {column["pytype"]}')
            out_col['type'] = _dtype_to_qtype[column['pytype']]

        # check the vector index column and extract necessary info to move to out_col
        out_col_check_vector_index = self._check_vector_index(column)
        out_col.update(out_col_check_vector_index)

        if 'sparseIndex' in column:
            out_col['sparseIndex'] = column['sparseIndex']
            out_col['type'] = ''

        if 'embedding' in column:
            out_col['embedding'] = column['embedding']

        if 'type' not in out_col:
            raise KDBAIException('Invalid column, missing `pytype` or `qtype`.')

        return out_col

    def _check_vector_index(self, column):
        vector_index = column.get('vectorIndex')

        out_col={}
        if vector_index:
            out_col['vectorIndex'] = vector_index
            vector_index_type = vector_index.get('type')
            if vector_index_type == 'tss':
                if ('pytype' not in column) or ('pytype' in column and column['pytype'] == 'float64'):
                    out_col['type'] = 'float'  # vectorIndex-column's entries of TSS cases should be 64-bit scalar;
                else:
                    raise KDBAIException('`pytype` of the tss-column should be `float64`.')
            elif vector_index_type:
                out_col['type'] = 'reals'   # vectorIndex-column's entries of non-TSS cases should be 32-bit vector
            else:
                raise KDBAIException('Invalid column, missing `type` in `vectorIndex`.')
        return out_col

    def _create_table(self, name, schema):
        body = self._rest_post_json(self.CREATE_PATH % name, schema)
        return self._create_table_status(body)

    def _create_table_status(self, body):
        if 'message' in body and body['message'] == 'success':
            return True
        else:
            raise KDBAIException(body)

    def _config(self):
        return self._rest_get_json(Session.CONFIG_PATH)

    def _list(self):
        config = self._config()
        tables = list(config.keys())
        return tables

    def _rest_get(self, path):
        headers = {'Content-type': CONTENT_TYPE['json'],
                   'Accept': CONTENT_TYPE['json']}
        req = self._rest_request('GET', path, headers)
        res = request.urlopen(req)
        return res.read().decode('utf-8')

    def _rest_get_json(self, path):
        body = json.loads(self._rest_get(path))
        return body

    def _rest_post_json(self, path, data, dumps: bool = True):
        headers = {'Content-type': CONTENT_TYPE['json'],
                   'Accept': CONTENT_TYPE['json']}
        if dumps:
            data = json.dumps(data, default=str)
        data = data.encode('utf-8')
        req = self._rest_request('POST', path, headers, data)
        res = request.urlopen(req)
        body = json.loads(res.read().decode('utf-8'))
        return body

    def _rest_post_json_to_qipc(self, path, data):
        headers = {'Content-type': CONTENT_TYPE['json'],
                   'Accept': CONTENT_TYPE['octet-stream']}
        data = json.dumps(data, default=str).encode('utf-8')
        req = self._rest_request('POST', path, headers, data)
        res = request.urlopen(req)
        res = kx._wrappers.deserialize(res.read())
        return self._format_qipc_result(res)

    def _rest_post_qipc(self, path, table, data, guid = False):
        headers = {'Content-type': CONTENT_TYPE['octet-stream'],
                   'Accept': CONTENT_TYPE['json']}
        if guid:
            data = bytes(kx._wrappers.k_pickle(kx.toq([uuid.uuid4(), table, data])))
        else:
            data = bytes(kx._wrappers.k_pickle(kx.toq([table, data])))
        if len(data) > MAX_QIPC_SERIALIZATION_SIZE:
            raise KDBAIException(
                f'The maximum serialized size of the data to insert is {MAX_QIPC_SERIALIZATION_SIZE} bytes. '
                f'The size of your serialized data is {len(data)} bytes. '
                'Please insert your data by smaller batches.'
                )
        req = self._rest_request('POST', path, headers, data)
        res = request.urlopen(req)
        return self._format_json_result(res.read().decode('utf-8'))

    def _rest_delete(self, path):
        headers = {'Content-type': CONTENT_TYPE['json'],
                   'Accept': CONTENT_TYPE['json']}
        req = self._rest_request('DELETE', path, headers)
        res = request.urlopen(req)
        body = json.loads(res.read().decode('utf-8'))
        return body

    def _rest_request(self, method, path, headers, data = None):
        url = self._build_url(path)
        if self.api_key is not None:
            headers['X-Api-Key'] = self.api_key
        return request.Request(url, method=method, headers=headers, data=data)

    def _build_url(self, path):
        return self.endpoint + path

    def _format_qipc_result(self, res):
        if isinstance(res, kx.Table):
            return res.pd()
        elif isinstance(res, kx.List):
            result = []
            for i in range(len(res)):
                result.append(res._unlicensed_getitem(i).pd())
            return result
        else:
            raise KDBAIException('Not implemented.')

    def _format_json_result(self, res):
        try:
            r = json.loads(res)
            if 'message' in r:
                return r['message']
        except json.decoder.JSONDecodeError:
            return True
        return True


class Table:
    """KDB.AI table."""

    def __init__(self, name: str, *, session: Session, **kwargs):
        """kdbai_client.Table

        Table object shall be created with `session.create_table(...)` or retrieved with `session.table(...)`.
        This constructor shall not be used directly.
        """
        self.name = name
        self.session = session

        try:
            tables = self.session._list()
        except urllib.error.HTTPError as e:
            raise KDBAIException(TABLE_RETRIEVAL_FAILURE, e=e)
        except Exception:
            raise KDBAIException(TABLE_RETRIEVAL_FAILURE)

        self._check_table_name(tables)

    def _check_table_name(self, tables: list):
        if self.name not in tables:
            raise KDBAIException(f'Failed to retrieve the table named: {self.name}.')
        return True

    def _check_index_options(self, index_options: dict):

        search_index_options = { # allowed index options for dense column of search/hybrid_search
            "flat":[],
            "hnsw":["efSearch"],
            "ivf":["clusters"],
            "ivfpq":["clusters"],
            "tss":[],
            "qFlat":[],
            "qHnsw":["efSearch"],
            "bm25":["k","b"],
            }

        schema = self.schema()['columns']
        vector_index_cols = [col for col in schema if 'vectorIndex' in col]
        col_type = vector_index_cols[0]['vectorIndex'].get('type') if vector_index_cols else None # search-column's type
        allowed_index_options = search_index_options[col_type] if col_type else []

        if index_options:
            for key in index_options:
                if vector_index_cols and (key not in allowed_index_options):
                    raise KDBAIException(f'Invalid index option: {key}.')

        return True

    def schema(self) -> Dict:
        """Retrieve the schema of the table.

        Raises:
            KDBAIException: Raised when an error occurs during schema retrieval

        Returns:
            A `dict` containing the table name
                and the list of column names and appropriate numpy datatypes.

        Example:
            ```python
            table.schema()

            {'columns': [{'name': 'id', 'pytype': 'str'},
                          {'name': 'tag', 'pytype': 'str'},
                          {'name': 'text', 'pytype': 'bytes'},
                          {'name': 'embeddings',
                           'pytype': 'float32',
                           'vectorIndex': {'dims': 1536, 'metric': 'L2', 'type': 'flat'}}]}
            ```
        """
        try:
            config = self.session._config()
            schema = config[self.name]
            return self._format_schema_to_py(schema)
        except Exception:
            raise KDBAIException(f'Failed to retrieve the schema of table named: {self.name}.')


    def _format_schema_to_py(self, schema: dict):
        schema.pop('type')
        for column in schema['columns']:
            column['qtype'] = column.pop('type')
            column['pytype'] = self._translate_qtype(column['qtype'])
            if 'attrMem' in column:
                column.pop('attrMem')
        return schema

    def _translate_qtype(self, qtype: int):
        return _qtype_to_dtype.get(qtype, 'object')

    def _validate_dataframe(self, data: pd.DataFrame, warn:Optional[bool] = True):
        if not isinstance(data, pd.DataFrame):
            raise KDBAIException('`data` should be a pandas.DataFrame.')
        elif len(data) == 0:
            raise KDBAIException('`data` should not be empty.')
        else:
            if (data.index.values != np.arange(len(data))).any():
                if warn:
                    logging.warning('`data` DataFrame has a non trivial index. It will be dropped before insertion.')
                data = data.reset_index(drop=True)
        return data


    def train(self, data: pd.DataFrame, warn:Optional[bool] = True) -> str:
        """Train the index (IVF and IVFPQ only).

        Args:
            data (DataFrame): Pandas dataframe with column names/types matching the target table.
            warn (bool): If True, display a warning when `data` has a trivial which will be dropped before training.

        Returns:
            A `string` containing the status after training

        Examples:
            ```python
            from datetime import timedelta
            from datetime import datetime

            ROWS = 50
            DIMS = 10

            data = {
                "time": [timedelta(microseconds=np.random.randint(0, int(1e10))) for _ in range(ROWS)],
                "sym": [f"sym_{np.random.randint(0, 999)}" for _ in range(ROWS)],
                "realTime": [datetime.utcnow() for _ in range(ROWS)],
                "price": [np.random.rand(DIMS).astype(np.float32) for _ in range(ROWS)],
                "size": [np.random.randint(1, 100) for _ in range(ROWS)],
            }
            df = pd.DataFrame(data)
            table.train(df)
            ```

        Raises:
            KDBAIException: Raised when an error occurs during training.
        """
        data = self._validate_dataframe(data, warn)

        try:
            return self.session._rest_post_qipc(Session.TRAIN_PATH, self.name, data)
        except urllib.error.HTTPError as e:
            raise KDBAIException(f'Failed to insert training data in table named: {self.name}.', e=e)
        except KDBAIException as e:
            raise e
        except Exception:
            raise KDBAIException(f'Failed to insert training data in table named: {self.name}.')

    def insert(self, data: pd.DataFrame, warn: Optional[bool] = True) -> bool:
        """Insert data into the table.

        Args:
            data (DataFrame): Pandas dataframe with column names/types matching the target table.
            warn (bool): If True, display a warning when `data` has a trivial which will be dropped before insertion.

        Returns:
            A boolean which is True if the insertion was successful.

        Examples:
            ```python
            ROWS = 50
            DIMS = 10

            data = {
                "time": [timedelta(microseconds=np.random.randint(0, int(1e10))) for _ in range(ROWS)],
                "sym": [f"sym_{np.random.randint(0, 999)}" for _ in range(ROWS)],
                "realTime": [datetime.utcnow() for _ in range(ROWS)],
                "price": [np.random.rand(DIMS).astype(np.float32) for _ in range(ROWS)],
                "size": [np.random.randint(1, 100) for _ in range(ROWS)],
            }
            df = pd.DataFrame(data)
            table.insert(df)
            ```

        Raises:
            KDBAIException: Raised when an error occurs during insert.
        """
        data = self._validate_dataframe(data, warn)

        try:
            return self.session._rest_post_qipc(Session.INSERT_PATH, self.name, data)
        except urllib.error.HTTPError as e:
            raise KDBAIException(f'Failed to insert data in table named: {self.name}.', e=e, key='message')
        except KDBAIException as e:
            raise e
        except Exception:
            raise KDBAIException(f'Failed to insert data in table named: {self.name}.')

    def query(
        self,
        filter: Optional[List[list]] = None,
        group_by: Optional[str] = None,
        aggs: Optional[List[list]] = None,
        sort_by: Optional[List[str]] = None,
        fill: Optional[str] = None,
    ) -> pd.DataFrame:
        """Query data from the table.

        Args:
            filter: A list of filter conditions as triplets in the following format:
                `[['function', 'column name', 'parameter'], ... ]`
                See all filter operators [here](https://code.kx.com/kdbai/use/filter.html#supported-filter-functions)
            group_by: A list of column names to use for group by.
            aggs: Either a list of column names to select or a list of aggregations to perform as a
                list of triplers in the following form:
                `[['output_column', 'agg_function', 'input_column'], ... ]`
                See all aggregation functions [here](https://code.kx.com/kdbai/use/query.html#supported-aggregations)
            sort_by: List of column names to sort on.
            fill: This defines how to handle null values. This should be either `'forward'` or `'zero'` or `None`.

        Returns:
            Pandas dataframe with the query results.

        Examples:
            ```python
            table.query(group_by = ['sensorID', 'qual'])
            table.query(filter = [['within', 'qual', [0, 2]]])

            # Select subset of columns
            table.query(aggs=['size'])
            table.query(aggs=['size', 'price'])
            ```

        Raises:
            KDBAIException: Raised when an error occurs during query.
        """
        params: Dict[str, Any] = {"table": self.name}

        optional_params_map = (
            ("filter", filter),
            ("groupBy", group_by),
            ("agg", aggs),
            ("fill", fill),
            ("sortCols", sort_by),
        )
        for key, value in optional_params_map:
            if value is not None:
                params[key] = value

        try:
            return self.session._rest_post_json_to_qipc(Session.QUERY_PATH, params)
        except urllib.error.HTTPError as e:
            raise KDBAIException(
                f'Failed to process the query {params} on table named: {self.name}.', e=e, key='message')
        except Exception:
            raise KDBAIException(
                f'Failed to process the query {params} on table named: {self.name}.')

    def search(
        self,
        vectors: List[List]|List[dict],
        n: int = 5,
        index_options: Optional[dict] = None,
        distances: Optional[str] = None,
        filter: Optional[List[list]] = None,
        index_only: Optional[bool] = None,
        group_by: Optional[str] = None,
        aggs: Optional[List[list]] = None,
        sort_by: Optional[List[str]] = None
    ) -> List[pd.DataFrame]:
        """Perform similarity search on the table, supports dense or sparse queries.

        Args:
            vectors (List[list]|List[dict]): Query vectors for the search.
            n (int): Number of neighbours to return.
            index_options (dict): Index specific options for similarity search.
            distances (str): Optional name of a column to output the distances.
                If not specified, __nn_distance
                will be added as an extra column to the result table.
            filter: A list of filter conditions as triplets in the following format:
                `[['function', 'column name', 'parameter'], ... ]`
                See all filter operators [here](https://code.kx.com/kdbai/use/filter.html#supported-filter-functions)
            group_by: A list of column names to use for group by.
            aggs: Either a list of column names to select or a list of aggregations to perform as a
                list of triplers in the following form:
                `[['output_column', 'agg_function', 'input_column'], ... ]`
                See all aggregation functions [here](https://code.kx.com/kdbai/use/query.html#supported-aggregations)
            sort_by: List of column names to sort on.

        Returns:
            List of Pandas dataframes with one dataframe of matching neighbors for each query vector.

        Examples:
            ```python
            #Find the closest neighbour of a single (dense) query vector
            table.search(vectors=[[0,0,0,0,0,0,0,0,0,0]], n=1)

            #Find the closest neighbour of a single (sparse) query vector
            table.search(vectors=[{101:1,4578:1,102:1}], n=1)

            #Find the 3 closest neighbours of 2 query vectors
            table.search(vectors=[[0,0,0,0,0,0,0,0,0,0], [1,1,1,1,1,1,1,1,1,1]], n=3)

            # With aggregation and sorting
            table.search(vectors=[[0,0,0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1,1,1]],
            n=3,
            aggs=[['sumSize','sum','size']],
            group_by=['sym'],
            sort_by=['sumSize'])

            # Returns a subset of columns for each match
            table.search(vectors=[[0,0,0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1,1,1]], n=3, aggs=['size'])
            table.search(vectors=[[0,0,0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1,1,1]], n=3, aggs=['size', 'price'])

            # Filter
            table.search(vectors=[[0,0,0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1,1,1]],
            n=3,
            filter=[['within','size',(5,999)],['like','sym','AAP*']])

            # Customized distance name
            table.search(vectors=[[0,0,0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1,1,1]],
            n=3,
            distances='myDist')

            # Index options
            table.search(vectors=[[0,0,0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1,1,1]],n=3,index_options=dict(efSearch=512))
            table.search(vectors=[[0,0,0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1,1,1]],n=3,index_options=dict(clusters=16))
            ```

        Raises:
            KDBAIException: Raised when an error occurs during search.
        """
        params: Dict[str, Any] = {"table": self.name}

        params['vectors'] = vectors
        params['n'] = n

        optional_params_map = (
            ("distances", distances),
            ("filter", filter),
            ("groupBy", group_by),
            ("agg", aggs),
            ("sortCols", sort_by),
            ("indexOnly",index_only),
        )
        for key, value in optional_params_map:
            if value is not None:
                params[key] = value # type: ignore

        if index_options is not None:
            self._check_index_options(index_options)
            for key, value in index_options.items():
                params[key] = value

        try:
            return self.session._rest_post_json_to_qipc(Session.SEARCH_PATH, params)
        except urllib.error.HTTPError as e:
            raise KDBAIException(
                f'Failed to process the query {params} on table named: {self.name}.', e=e)
        except Exception:
            raise KDBAIException(
                f'Failed to process the query {params} on table named: {self.name}.')


    def hybrid_search(
        self,
        dense_vectors: List[List],
        sparse_vectors: List[dict],
        n: int = 5,
        dense_index_options: Optional[dict] = None,
        sparse_index_options: Optional[dict] = None,
        alpha: float = 0.5,
        distances: Optional[str] = None,
        filter: Optional[List[list]] = None,
        group_by: Optional[str] = None,
        aggs: Optional[List[list]] = None,
        sort_by: Optional[List[str]] = None,
    ) -> List[pd.DataFrame]:
        """Perform hybrid search on the table.

        Args:
            dense_vectors (list of lists): Dense query vectors for the search.
            sparse_vectors (list of dicts): Sparse query vectors for the search.
            n (int): Number of neighbours to return.
            dense_index_options (dict): Index specific options for similarity search.
            sparse_index_options (dict): Index specific options for similarity search.
            alpha (float): Weight of strategy in [0,1], 0 sparse vs 1 dense
            distances (str): Optional name of a column to output the distances.
                If not specified, __nn_distance
                will be added as an extra column to the result table.
            filter: A list of filter conditions as triplets in the following format:
                `[['function', 'column name', 'parameter'], ... ]`
                See all filter operators [here](https://code.kx.com/kdbai/use/filter.html#supported-filter-functions)
            group_by: A list of column names to use for group by.
            aggs: Either a list of column names to select or a list of aggregations to perform as a
                list of triplers in the following form:
                `[['output_column', 'agg_function', 'input_column'], ... ]`
                See all aggregation functions [here](https://code.kx.com/kdbai/use/query.html#supported-aggregations)
            sort_by: List of column names to sort on.

        Returns:
            List of Pandas dataframes with one dataframe of matching neighbors for each query vector.

        Raises:
            KDBAIException: Raised when an error occurs during search.

        Examples:
            ```python
            # Find the closest neighbour of a single hybrid query vector
            table.hybrid_search(dense_vectors=[[0,0,0,0,0,0,0,0,0,0]],
                                sparse_vectors=[{101:1,4578:1,102:1}],
                                n=1)

            # Find the 3 closest neighbours for 2 hybrid queries
            table.hybrid_search(dense_vectors=[[0,0,0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1,1,1]],
                                sparse_vectors=[{101:1,4578:1,102:1},{101:1,6079:2,102:1}],
                                n=3)

            # Weight the sparse leg of the query higher setting alpha = 0.1
            table.hybrid_search(dense_vectors=[[0,0,0,0,0,0,0,0,0,0]],
                                sparse_vectors=[{101:1,4578:1,102:1}],
                                alpha=0.1,
                                n=1)

            # Filter
            table.hybrid_search(dense_vectors=[[0,0,0,0,0,0,0,0,0,0]],
                                sparse_vectors=[{101:1,4578:1,102:1}],
                                n=1,
                                filter=[['within','size',(5,999)],['like','sym','AAP*']])

            # Index options
            table.hybrid_search(dense_vectors=[[0,0,0,0,0,0,0,0,0,0]],
                                sparse_vectors=[{101:1,4578:1,102:1}],
                                n=1,
                                dense_index_options=dict(efSearch=521),
                                sparse_index_options={'k':1.4,'b':0.78})

            # Customized distance name
            table.hybrid_search(dense_vectors=[[0,0,0,0,0,0,0,0,0,0]],
                                sparse_vectors=[{101:1,4578:1,102:1}],
                                n=1,
                                distances='myDist')
            ```
        """
        params: Dict[str, Any] = {"table": self.name}

        params['denseVectors'] = dense_vectors
        params['sparseVectors'] = sparse_vectors

        params['n'] = n

        self._check_index_options(dense_index_options)

        optional_params_map = (
            ("alpha", alpha),
            ("denseIndexOptions", dense_index_options),
            ("sparseIndexOptions", sparse_index_options),
            ("distances", distances),
            ("filter", filter),
            ("groupBy", group_by),
            ("agg", aggs),
            ("sortCols", sort_by),
        )
        for key, value in optional_params_map:
            if value is not None:
                params[key] = value # type: ignore

        try:
            return self.session._rest_post_json_to_qipc(Session.HYBRID_SEARCH_PATH, params)
        except urllib.error.HTTPError as e:
            raise KDBAIException(
                f'Failed to process the query {params} on table named: {self.name}.', e=e)
        except Exception:
            raise KDBAIException(
                f'Failed to process the query {params} on table named: {self.name}.')

    def drop(self) -> bool:
        """Drop the table.

        Returns:
            A boolean which is True if the table was successfully dropped.

        Examples:
            ```python
            table.drop()
            ```

        Raises:
            KDBAIException: Raised when an error occurs during the table deletion.
        """
        try:
            body = self.session._rest_delete(Session.DROP_PATH % self.name)
            return self._drop_status(body)
        except urllib.error.HTTPError as e:
            raise KDBAIException(
                f'Failed to drop the table named: {self.name}.', e=e)
        except KDBAIException as e:
            raise e
        except Exception:
            raise KDBAIException(
                f'Failed to drop the table named: {self.name}.')

    def _drop_status(self, body):
        if 'message' in body and body['message'] == 'success':
            return True
        else:
            raise KDBAIException(body)

class KDBAIException(Exception):
    """KDB.AI exception."""

    def __init__(self, msg, e = None, key = None, *args, **kwargs):
        super().__init__(msg, *args, **kwargs)
        self.e = e
        if self.e is not None:
            reason = None
            data = self.e.fp.read()
            try:
                if (self.e.getcode() == 400
                    and self.e.headers.get('Content-type') == CONTENT_TYPE['octet-stream']):
                    reason = kx._wrappers.deserialize(data).py()[0]['ai'].decode('utf-8')
                else:
                    reason = json.loads(data.decode('utf-8'))
                    if key is not None:
                        reason = reason[key]
            except Exception:
                reason = data.decode('utf-8')
            self.code = self.e.code
            if reason is not None:
                self.text = f'{msg[:-1]}, because of: {reason}.'
            self.args = (self.text,)
