from copy import deepcopy
import os
from typing import Any, Dict, Final, List, Optional, Union

from numpy import arange, float32, float64
from pandas import DataFrame

from .api import KDBAIException
from .constants import VdbScopes


os.environ['PYKX_IGNORE_QHOME'] = '1'
os.environ['PYKX_NOQCE'] = '1'
os.environ['SKIP_UNDERQ'] = '1'
os.environ['QARGS'] = '--unlicensed'
import pykx as kx  # noqa: E402


def _convert_filter(operator_map:dict, filters: list) -> list:
    """Converts filters to appropriate format for the server

    Args:
        operator_map (dict): Dictionary that contains pykx value for filter operators.
        filters (list): list of filter conditions.

    Returns:
        List of conditions that is accepted by the server
    """
    def _convert_filter_inner(filters: list) -> list:
        if isinstance(filters[0], (list, tuple)):
            # this is for the operands of `and`, `or` and top level conditions
            return [_convert_filter_inner(list(x)) for x in filters]
        operator = filters[0]
        if operator in ['or', 'and', 'not']:
            return [operator_map.get(operator, operator), *[_convert_filter_inner(x) for x in filters[1:]]]
        if operator == '>=':
            return _convert_filter_inner(['not', ['<', *filters[1:]]])
        if operator == '<=':
            return _convert_filter_inner(['not', ['>', *filters[1:]]])
        if operator == '<>':
            return _convert_filter_inner(['not', ['=', *filters[1:]]])
        if operator == 'like' and isinstance(filters[2], str):
            pattern = filters[2].encode()
            if len(pattern) == 1:
                pattern = [pattern]
            filters[2] = pattern
        if operator == '=' and isinstance(filters[2], str):
            filters[2] = [filters[2]]
        try:
            # `in` needs enlist ("in", "colname", [['AA', 'BB']])
            if operator == 'in' and isinstance(filters[2][0], str):
                filters[2] = [filters[2]]
        except KeyError:
            # we can't figure out, server will respond if parameter is incorrect
            pass
        if operator not in operator_map:
            raise KDBAIException(f"Unsupported filter function: {operator}")
        return [operator_map.get(operator, operator), *filters[1:]]

    # we make changes inplace and don't want any side effect for the user's data
    filters = deepcopy(filters)
    if isinstance(filters, tuple):
        filters = list(filters)
    if not isinstance(filters[0], (list, tuple)):
        # we require a list of filters. Where only one is provided in isolation we will nest it
        filters = [filters]
    return _convert_filter_inner(filters)


conversions: Final[Dict[str, Union[kx.Table, kx.List]]] = {
    'pd': lambda x: x.pd(),
    'py': lambda x: x.py(),
    'q': lambda x: x
}

class TablePyKx:
    """KDB.AI table."""

    def __init__(self,
                 name: str,
                 schema: dict,
                 session,
                 *args,
                 scope: VdbScopes = VdbScopes.MetaManaged,
                 default_result_type: str = 'pd',
                 **kwargs
                 ) -> None:

        self.name: Final[str] = name
        self.schema: dict = schema
        self.session: Final = session
        self.scope: Final[VdbScopes] = scope
        self.default_result_type: str = default_result_type
        indexes = self.schema.get('idxParams')
        self.dense_index_name = None
        self.sparse_index_name = None
        if indexes:
            if isinstance(indexes, list):
                try:
                    self.dense_index_name = [index['name'] for index in indexes if not index.get('sparse')][0]
                except KeyError:
                    pass
                try:
                    self.sparse_index_name = [index['name'] for index in indexes if index.get('sparse')][0]
                except KeyError:
                    pass
            else:
                if indexes.get('sparse', [False])[0]:
                    self.sparse_index_name = indexes['name'][0]
                else:
                    self.dense_index_name = indexes['name'][0]

        insert_functions = {
            VdbScopes.MetaManaged: self._insert_with_meta,
            VdbScopes.MetaFromRef: self._insert_from_meta,
            VdbScopes.NoMeta: self._insert_from_vector,
        }
        self.insert_function = insert_functions[scope]

    def refresh(self):
        """Refresh table metadata"""
        self.schema = self.session.table(name=self.name, scope=self.scope).schema

    @staticmethod
    def _validate_dataframe(data, warn:Optional[bool] = True):
        if data is None or len(data) == 0:
            raise KDBAIException('`data` should not be empty.')
        if isinstance(data, dict):
            data = DataFrame(data=data)
        elif isinstance(data, DataFrame) and (data.index.values != arange(len(data))).any():
            data = data.reset_index(drop=True)

        return data

    def train(self, data: Union[dict, DataFrame, kx.Table], warn:Optional[bool] = True) -> bool:
        """Train the index (IVF and IVFPQ only).

        Args:
            data (dict|DataFrame|kx.Table): Table with column names/types matching the target table.
            warn (bool): Ignored, kept for backward compatibility

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
        # TBD: It can be done without branching with separate insert functions like with insert
        if self.scope == VdbScopes.NoMeta:
            payload = {'vdb': self.name, 'vectors': data}
        else:
            data = TablePyKx._validate_dataframe(data, warn)
            payload = {'vdb': self.name, 'payload': data}
        return self._do_train('vdbTrain', payload)

    def _do_train(self, insert_function: str, payload)-> bool:
        result = self.session.gw(kx.SymbolAtom(insert_function), payload)
        result_type = type(result)
        if result_type == kx.BooleanAtom:
            return True
        if result_type == kx.CharVector:
            raise KDBAIException(f'Failed to train data in table named {self.name}: {result.py().decode("utf-8")}')
        raise KDBAIException(f'Unexpected return type: {result_type}')

    def insert(self,
               data: Union[DataFrame, List[list]],
               part: Optional[int] = None,
               warn: Optional[bool] = True, **kwargs):
        """Insert data into the table.

        Args:
            data (DataFrame | List[list]): Pandas dataframe with column names/types matching the target
                table(metaManaged) or List of vectors (noMeta).
            warn (bool): If True, display a warning when `data` has a trivial which will be dropped before insertion.
            part (int): Partition id (optional).

        Returns:
            A dictionary with inserted data's start and end IDs.

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

            table_nometa.insert(np.random.rand(ROWS, DIMS).astype(np.float32))
            ```

        Raises:
            KDBAIException: Raised when an error occurs during insert.
        """
        return self.insert_function(data, part=part, warn=warn, **kwargs)

    def _do_insert(self, insert_function: str, payload, **kwargs):
        result = self.session.gw(kx.SymbolAtom(insert_function), payload)
        result_type = type(result)
        if result_type == kx.Table:
            return {key: value[0] for key, value in result.py().items()}
        if result_type == kx.List:
            retval = [{key: value[0] for key, value in table.py().items()} for table in result]
            return retval
        if result_type == kx.CharVector:
            raise KDBAIException(f'Failed to insert data in table named {self.name}: {result.py().decode("utf-8")}')
        raise KDBAIException(f'Unexpected return type: {result_type}')

    def _insert_with_meta(self, data: Union[dict, DataFrame, kx.Table], part: Optional[int] = None, **kwargs):
        # TBD: if this can be standardised as part of _do_insert
        data = TablePyKx._validate_dataframe(data)

        payload = {'vdb': self.name, 'payload': data}
        if part is not None:
            payload['part'] = part
        return self._do_insert('vdbInsert', payload, **kwargs)

    def _insert_from_meta(self, data: str, part: Optional[int] = None, **kwargs):
        raise NotImplementedError()

    def _insert_from_vector(self, data: List[list], part: Optional[int] = None, **kwargs):
        payload = {'vdb': self.name, 'vectors': data}
        if part is not None:
            payload['part'] = part
        return self._do_insert('vdbInsert', payload, **kwargs)

    def query(
        self,
        filter: Optional[List[list]] = None,
        group_by: Optional[str] = None,
        aggs: Optional[List[list]] = None,
        sort_by: Optional[List[str]] = None,
        fill: Optional[str] = None,
        result_type: Optional[str] = None
    ) -> Union[DataFrame, dict]:
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
            result_type (str): data type to convert result into (pd|py|q)

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
        params: Dict[str, Any] = {"vdb": self.name}

        optional_params_map = (
            ("groupBy", group_by),
            ("agg", aggs),
            ("fill", fill),
            ("sortCols", sort_by),
        )
        for key, value in optional_params_map:
            if value:
                params[key] = value

        if filter:
            params['filter'] = _convert_filter(self.session.operator_map, filter)

        result = self.session.gw(
            kx.SymbolAtom('getData'),
            params
        )
        if type(result) == kx.CharVector:
            raise KDBAIException(
                f'Failed to process the query {params} on table named: {self.name}: {result.py().decode("utf-8")}.')

        return conversions[result_type or self.default_result_type](result)

    def search(self,
               vectors: List[List],
               n: int = 5,
               search_column: Optional[str] = None,
               index_options: Optional[dict] = None,
               distances: Optional[str] = None,
               filter: Optional[List[list]] = None,
               index_only: Optional[bool] = None,
               group_by: Optional[str] = None,
               aggs: Optional[List[list]] = None,
               sort_by: Optional[List[str]] = None,
               return_matches: Optional[bool] = None,
               result_type: Optional[str] = None, **kwargs):
        """Perform similarity search on the table

        Args:
            vectors (List[List]): Query vectors for the search.
            n (int): Number of neighbours to return.
            search_column (str): column to perform a Non Transformed TSS search on.
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
            result_type (str): data type to convert result into (pd|py|q)
            kwargs (dict): extra keyword options that are passed to the search function

        Examples:
            ```python
            #Find the closest neighbour of a single (dense) query vector
            table.search(vectors=[[0,0,0,0,0,0,0,0,0,0]], n=1)

            #Find the 3 closest neighbours of 2 query vectors
            table.search(vectors=[[0,0,0,0,0,0,0,0,0,0], [1,1,1,1,1,1,1,1,1,1]], n=3)

            # Filter
            table.search(vectors=[[0,0,0,0,0,0,0,0,0,0]],
            n=3,
            filter=[['within','size',(5,999)],['like','sym',b'AAP*']])

            # Index options
            table.search(vectors=[[0,0,0,0,0,0,0,0,0,0]], n=3, index_options=dict(efSearch=512))
            ```

        Raises:
            KDBAIException: Raised when an error occurs during search.
        """
        payload = {
            'vdb': self.name,
            'k': n,
            **kwargs
        }
        optional_params_map = (
            ("groupBy", group_by),
            ("agg", aggs),
            ("sortCols", sort_by),
            ("param", index_options),
            ("indexOnly", index_only),
        )
        for key, value in optional_params_map:
            if value:
                payload[key] = value
        if filter:
            payload['filter'] = _convert_filter(self.session.operator_map, filter)
        if distances:
            payload['options'] = {"distCol": distances}
        if return_matches:
            payload['returnMatches'] = True

        if not search_column and self.schema.get('searchCol', '') != '':
            search_column = self.schema['searchCol']

        results = []
        if (search_column or self.schema.get("searchCol")) and isinstance(vectors[0], list):
            for vector in vectors:
                payload['qry'] = float64(vector)
                payload['searchCol'] = search_column or self.schema["searchCol"]
                result = self.session.gw(kx.SymbolAtom('vdbSearch'), payload)
                if isinstance(result, kx.CharVector):
                        raise KDBAIException(f'Error during search: {result.py().decode("utf-8")}')
                results.append(conversions[result_type or self.default_result_type](result))

        else:
            for vector in vectors:
                if isinstance(vector, dict):
                    index_name = self.sparse_index_name
                    vector = {int(k): v for k, v in vector.items()}
                else:
                    index_name = self.dense_index_name
                    vector = float32(vector)
                payload['qry'] = {index_name: vector}
                payload['weights'] = {index_name: 1.0}
                result = self.session.gw(
                    kx.SymbolAtom('vdbSearch'),
                    payload
                )
                if isinstance(result, kx.CharVector):
                    raise KDBAIException(f'Error during search: {result.py().decode("utf-8")}')
                results.append(conversions[result_type or self.default_result_type](result))

        return results

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
        result_type: Optional[str] = None, **kwargs) -> List[DataFrame]:
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
            result_type (str): data type to convert result into (pd|py|q)
            kwargs (dict): extra keyword options that are passed to the search function

        Returns:
            List of Pandas dataframes/PyKx table/python dictionary with one dataframe of matching neighbors for each
            query vector.

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
        if len(dense_vectors) != len(sparse_vectors):
            raise KDBAIException("Number of Dense Query vectors does not equal Number of Sparse Query vectors")
        payload = {
            "vdb": self.name,
            "k": n,
            "weights": {self.dense_index_name: alpha, self.sparse_index_name: 1.0 - alpha},
            **kwargs
        }
        optional_params_map = (
            ("groupBy", group_by),
            ("agg", aggs),
            ("sortCols", sort_by)
        )
        for key, value in optional_params_map:
            if value:
                payload[key] = value

        if filter:
            payload["filter"] = _convert_filter(self.session.operator_map, filter)
        if distances:
            payload["options"] = {"distCol": distances}

        params = {}
        if dense_index_options:
            params[self.dense_index_name] = dense_index_options
        if sparse_index_options:
            params[self.sparse_index_name] = sparse_index_options
        if params:
            payload["param"] = params

        results = []
        for vector, sparse_vector in zip(dense_vectors, sparse_vectors):
            payload['qry'] = {
                    self.dense_index_name: float32(vector),
                    self.sparse_index_name: {int(k): v for k, v in sparse_vector.items()}
                }
            result = self.session.gw(
                kx.SymbolAtom('vdbSearch'),
                payload
            )
            if isinstance(result, kx.CharVector):
                raise KDBAIException(f'Error during search: {result.py().decode("utf-8")}')

            results.append(conversions[result_type or self.default_result_type](result))

        return results

    def drop(self) -> bool:
        """Delete table"""
        try:
            result = self.session.gw(kx.SymbolAtom('vdbDelete'), {'vdb': self.name})
        except Exception as e:
            raise KDBAIException(f'Error during dropping table: {e}')
        if isinstance(result, kx.CharVector):
            raise KDBAIException(f'Error during dropping table: {result.py().decode("utf-8")}')
        return True

    def __eq__(self, rhs: object) -> bool:
        return self.name == rhs.name and \
            self.schema == rhs.schema and \
            self.scope == rhs.scope
