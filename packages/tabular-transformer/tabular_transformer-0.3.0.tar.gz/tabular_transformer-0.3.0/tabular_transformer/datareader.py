from pathlib import Path
from typing import Dict, Literal, Optional, Union, List
import pandas as pd
import os
import pyarrow.compute as pc
import pyarrow.csv as csv
import pyarrow.parquet as parquet
import pyarrow as pa
import numpy as np
import inspect


class DataReader():
    r"""
    A utility class for loading, processing, and splitting tabular data from CSV or Parquet files.

    The `DataReader` serves as the entry point for the `tabular-transformer` processing pipeline, facilitating 
    the ingestion of data. It distinguishes tabular columns as either CATEGORICAL or NUMERICAL. Categorical columns 
    denote discrete categories (e.g., 'gender', 'color'), while numerical columns represent continuous values 
    (e.g., 'age', 'income'). This classification is based on the semantic meaning of the columns rather than 
    their stored data types, is determined by your understanding of the data and your discretion.
    """
    file_path: Path
    ensure_categorical_cols: List[str]
    ensure_numerical_cols: List[str]
    label: Optional[str]
    id: Optional[str]
    header: bool
    column_names: Optional[List[str]]
    file_type: Literal['csv', 'parquet']

    def __init__(self,
                 file_path: Union[str, Path],
                 ensure_categorical_cols: List[str] = [],
                 ensure_numerical_cols: List[str] = [],
                 label: Optional[str] = None,
                 id: Optional[str] = None,
                 header: bool = True,
                 column_names: Optional[List[str]] = None):
        """
        The `DataReader` acts as an interface for accessing and interpreting data. 
        It classifies tabular columns as either CATEGORICAL or NUMERICAL. 
        Categorical columns represent discrete categories (e.g., 'gender', 'color'), 
        while numerical columns denote continuous values (e.g., 'age', 'income'). 
        This classification is based on the semantic meaning of the columns rather than
        their stored data types and is determined by your understanding of the data at your discretion.

        DataReader instances are callable object, invoking them with new arguments to 
        update settings returns a new DataReader instance configured accordingly. 
        This feature is particularly handy for reusing configurations across datasets, 
        such as when having similar training and testing datasets.
        >>> test_data_reader = train_data_reader(file_path='new_path', label=None)

        will return a DataReader instance with updated file_path and label

        Args:
            file_path (Union[str, Path]): Path to the data file.

            ensure_categorical_cols (List[str], optional): Columns to treat as categorical.
                If omitted or left empty, the default behavior is to treat all columns not explicitly specified in `ensure_numerical_cols` as categorical. Defaults to `[]`.

            ensure_numerical_cols (List[str], optional): Columns to treat as numerical.
                If omitted or left empty, the default behavior is to treat all columns not explicitly specified in `ensure_categorical_cols` as numerical. Defaults to `[]`.

            label (Optional[str], optional): Name of the label column. Defaults to `None`.

            id (Optional[str], optional): Name of the ID column. Defaults to `None`.

            header (bool, optional): Indicates if the file contains a header row. Defaults to `True`.

            column_names (Optional[List[str]], optional): Column names to use if `header` is `False`. Defaults to `None`.
        """
        self.file_path = Path(file_path)
        self._check_file_types()

        assert header or column_names is not None, \
            "if no header in data file, you must denfine `column_names`"
        self.header = header

        self.column_names = column_names \
            if column_names is not None else self._get_column_names()

        self._check_cat_num_cols(
            ensure_categorical_cols,
            ensure_numerical_cols
        )

        self.label = label
        assert self.label is None or self.label in self.column_names, \
            f"`label` '{self.label}' not exists in table column names."

        self.id = id
        assert self.id is None or self.id != self.label
        assert self.id is None or self.id in self.ensure_categorical_cols, \
            f"id column `{id}` must be `categorical`"

    def __call__(self, **kwargs):
        """
        Creates a new `DataReader` instance with updated parameters.

        **Parameters:**

        - **kwargs**: Keyword arguments corresponding to the `__init__` parameters.

        **Returns:**

        - A new instance of `DataReader` with the updated parameters.
        """
        sig = inspect.signature(self.__init__)
        paras = [param.name for param in sig.parameters.values()
                 if param.name != 'self']
        assert set(kwargs.keys()).issubset(set(paras)), \
            f"bad arguments: {set(kwargs.keys()) - set(paras)}"

        original_val = {key: getattr(self, key) for key in paras}
        if 'label' in kwargs and kwargs['label'] is None and original_val['label'] is not None:
            label_col = original_val['label']
            original_val['ensure_categorical_cols'] = \
                [col for col in original_val['ensure_categorical_cols']
                    if col != label_col]
            original_val['ensure_numerical_cols'] = \
                [col for col in original_val['ensure_numerical_cols']
                    if col != label_col]
            if original_val['column_names'] is not None:
                original_val['column_names'] = \
                    [col for col in original_val['column_names']
                     if col != label_col]
        original_val.update(kwargs)
        return self.__class__(**original_val)

    def read(self) -> pa.Table:
        """
        Loads the data file and returns it as a PyArrow Table.
        To convert the returned table into a Pandas DataFrame,
        use the `.to_pandas()` method.

        >>> df = data_reader.read().to_pandas()
        >>> df.head(3)

        **Returns:**

        - **table** (*pa.Table*): The data loaded into a PyArrow Table.
        """
        cat_schema = [(col, pa.string())
                      for col in self.ensure_categorical_cols]
        num_schema = [(col, pa.float32())
                      for col in self.ensure_numerical_cols]
        schema = pa.schema(cat_schema + num_schema)

        print('start reading file, it may take a while..')
        if self.file_type == 'csv':
            table = csv.read_csv(
                self.file_path,
                read_options=csv.ReadOptions(
                    column_names=self.column_names if not self.header else None),
                convert_options=csv.ConvertOptions(column_types=schema)
            )
        else:
            table = parquet.read_table(self.file_path)
            reordered_schema = pa.schema(
                [schema.field(col) for col in table.column_names])
            table = table.cast(reordered_schema)
        print('read file completed.')

        assert self.column_names == table.column_names, \
            f"`column_names` not right. Mismatched columns: \
                {set(self.column_names) ^ set(table.column_names)}"

        return table

    def _check_file_types(self):
        if self.file_path.suffix == '.csv' or self.file_path.suffixes[0] == '.csv':
            self.file_type = 'csv'
        elif self.file_path.suffix == '.parquet':
            self.file_type = 'parquet'
        else:
            raise ValueError(
                "DataReader only support file type with extension: `csv`, `csv.gz`, `parquet`")

    def _get_column_names(self):
        if self.file_type == 'csv':
            with csv.open_csv(self.file_path) as reader:
                schema = reader.schema
                column_names = schema.names
        else:
            parquet_file = parquet.ParquetFile(self.file_path)
            column_names = parquet_file.schema.names
        return column_names

    def _check_cat_num_cols(self,
                            ensure_categorical_cols,
                            ensure_numerical_cols):

        assert isinstance(ensure_categorical_cols, list)
        assert isinstance(ensure_numerical_cols, list)

        assert len(ensure_categorical_cols) > 0 or len(ensure_numerical_cols) > 0, \
            "`ensure_categorical_cols`, `ensure_numerical_cols` cannot both be empty. "

        if len(ensure_categorical_cols) == 0:
            ensure_categorical_cols = [
                col for col in self.column_names if col not in ensure_numerical_cols]

        if len(ensure_numerical_cols) == 0:
            ensure_numerical_cols = [
                col for col in self.column_names if col not in ensure_categorical_cols]

        self.ensure_categorical_cols = ensure_categorical_cols
        self.ensure_numerical_cols = ensure_numerical_cols

        assert (len(self.ensure_numerical_cols) == 0
                or all(isinstance(e, str) and len(e.strip()) > 0
                       for e in self.ensure_numerical_cols)), \
            "`ensure_numerical_cols` must be list of column names"

        assert (len(self.ensure_categorical_cols) == 0
                or all(isinstance(e, str) and len(e.strip()) > 0
                       for e in self.ensure_categorical_cols)), \
            "`ensure_categorical_cols` must be list of column names"

        numerical_set = set(self.ensure_numerical_cols)
        categorical_set = set(self.ensure_categorical_cols)
        common_set = numerical_set.intersection(categorical_set)
        assert len(common_set) == 0, \
            f"""{list(common_set)}
                      both in the ensure_numerical_cols and ensure_categorical_cols"""

        assert set(self.ensure_categorical_cols).issubset(set(self.column_names)), \
            f"cols specified in `ensure_categorical_cols` not exist in column_names: \
        {set(self.ensure_categorical_cols) - set(self.column_names)}"

        assert set(self.ensure_numerical_cols).issubset(set(self.column_names)), \
            f"cols specified in `ensure_numerical_cols` not exist in column_names: \
        {set(self.ensure_numerical_cols) - set(self.column_names)}"

        assert set(self.ensure_categorical_cols + self.ensure_numerical_cols) == set(self.column_names), \
            f"all columns must be set either in `ensure_categorical_cols` or `ensure_numerical_cols`, missing cols: \
               {set(self.column_names) - set(self.ensure_categorical_cols + self.ensure_numerical_cols)}"

    def split_data(self, split: Dict[str, float | int],
                   seed: Optional[int] = 1337,
                   override: bool = True,
                   output_path: Optional[Path | str] = None,
                   save_as: Literal['csv', 'csv.gz', 'parquet'] = 'csv') -> Dict[str, Path]:
        """
        Splits the data into multiple parts for validation and test based on the provided ratios or counts.

        Args:
            split (Dict[str, float | int]): Dictionary specifying split names and their corresponding ratios or counts.
                For example, 
                `split={'train': 1_000_000, 'val': 0.2, 'test': -1}`
                will partition the data into:
                - `train`: 1,000,000 samples.
                - `val`: 20% of the total samples.
                - `test`: The remaining samples.

            seed (Optional[int]): Random seed for shuffling the data before splitting. If `None`, no shuffling is performed. Defaults to `1337`.

            override (bool): Whether to override existing split files. Defaults to `True`.

            output_path (Optional[Path | str]): Directory to save the split files. Defaults to the data file's directory.

            save_as (Literal['csv', 'csv.gz', 'parquet']): Format to save the split files. Defaults to `'csv'`.

        Returns:
            Dict[str, Path]: Dictionary mapping split names to their file paths.
        """
        assert isinstance(split, dict), "`split` must be Dict[str, float|int]"
        assert save_as in ['csv', 'csv.gz', 'parquet']

        file_path: Path = self.file_path
        base_stem = file_path.stem.split('.')[0]
        suffix = f".{save_as}"

        output_path = file_path.parent \
            if output_path is None else Path(output_path)

        if not output_path.exists():
            output_path.mkdir(parents=True)

        split_path = {sp: output_path / (f"{base_stem}_{sp}{suffix}")
                      for sp in split.keys()}

        if all(split_path[sp].exists()
               for sp in split.keys()) \
                and not override:
            print("splits already exists, skip split.")
            return split_path

        table = self.read()

        data_size = table.num_rows
        ixs = np.arange(data_size)

        if seed is not None:
            rng = np.random.default_rng(seed)
            rng.shuffle(ixs)

        start = 0

        for sp, ratio in sorted(split.items(), key=lambda kv: -kv[1]):
            assert isinstance(ratio, (float, int))
            assert not isinstance(ratio, int) or ratio == -1 or ratio > 0, \
                "integer split ratio can be -1 or positive intergers, -1 means all the rest of data"
            assert not isinstance(ratio, float) or 1 > ratio > 0, \
                "float split ratio must be interval (0, 1)"
            if isinstance(ratio, int):
                part_len = data_size - start if ratio == -1 else ratio
                assert part_len > 0, f'`no data left for `{sp}` split'
            else:
                part_len = int(data_size * ratio)
                assert part_len > 0, f'`{sp}` split {ratio} two small'
            end = start + part_len
            assert end <= data_size, "bad split: all split sum exceed the data size"
            data_part = table.take(ixs[start: end])
            print(f'split: {sp}, n_samples: {part_len}')

            part_path = split_path[sp]

            if part_path.exists() and override:
                os.remove(part_path)
                print(f"{part_path} *exists*, delete old split `{sp}`")

            if not part_path.exists():
                print(f"save split `{sp}` at path: {part_path}")

                if save_as == 'csv':
                    csv.write_csv(data_part, part_path)
                elif save_as == 'csv.gz':
                    with pa.output_stream(part_path, compression='gzip') as stream:
                        csv.write_csv(data_part, stream)
                elif save_as == 'parquet':
                    parquet.write_table(data_part, part_path)
                else:
                    raise ValueError("bad file type.")
            else:
                print(f"{part_path} *exists*, skip split `{sp}`")

            start = end
        return split_path

    def __repr__(self):
        return (
            f"DataReader(\n"
            f"  file_path = '{self.file_path}',\n"
            f"  ensure_categorical_cols = {self.ensure_categorical_cols},\n"
            f"  ensure_numerical_cols = {self.ensure_numerical_cols},\n"
            f"  label = {repr(self.label)},\n"
            f"  id = {repr(self.id)},\n"
            f"  header = {self.header},\n"
            f"  column_names = {self.column_names}\n"
            f")"
        )
