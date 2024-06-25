import gc
import pandas as pd
import numpy as np

from src.components.data_processing import transaction_amt_cents

def label_encode_and_memory_reduce(df: pd.DataFrame) -> None:
    """
    Label encode categorical variables and reduce memory usage by converting to appropriate dtypes.
    
    Args:
        df (pd.DataFrame): Combined DataFrame.
    """
    for col in df.columns:
        if (df[col].dtype == 'category') or (df[col].dtype == 'object'):
            df_comb, _ = df[col].factorize(sort=True)
            if df_comb.max() > 32000:
                df[col] = df_comb.astype('int32')
            else:
                df[col] = df_comb.astype('int16')
        elif col not in ['TransactionAmt', 'TransactionDT']:
            mn = np.min(df[col].min())
            df[col] -= np.float32(mn)
            df[col].fillna(-1, inplace=True)


def encode_FE(df: pd.DataFrame, cols: list) -> None:
    """
    Frequency encode the specified columns.
    
    Args:
        df (pd.DataFrame): Combined DataFrame.
        cols (list): List of column names to frequency encode.
    """
    for col in cols:
        vc = df[col].value_counts(dropna=True, normalize=True).to_dict()
        vc[-1] = -1
        nm = col + '_FE'
        df[nm] = df[col].map(vc).astype('float32')
        print(f"{nm}, ", end='')


def encode_LE(col: str, df: pd.DataFrame, verbose: bool = True) -> None:
    """
    Label encode a single column.
    
    Args:
        col (str): Column name to encode.
        df (pd.DataFrame): Combined DataFrame.
        verbose (bool): If True, prints the column name. Default is True.
    """
    df_comb, _ = df[col].factorize(sort=True)
    if df_comb.max() > 32000:
        df[col] = df_comb.astype('int32')
    else:
        df[col] = df_comb.astype('int16')
    if verbose:
        print(f"{col}, ", end='')
    gc.collect()


def encode_AG(main_columns: list, uids: list, aggregations: list = ['mean'], df: pd.DataFrame = None, fill_na: bool = True, use_na: bool = False) -> None:
    """
    Aggregation of main columns with UID for given statistics.
    
    Args:
        main_columns (list): List of main columns to aggregate.
        uids (list): List of UID columns to group by.
        aggregations (list): List of aggregation functions. Default is ['mean'].
        df (pd.DataFrame): Combined DataFrame.
        fillna (bool): If True, fill NaN values with -1. Default is True.
        use_na (bool): If True, use NaN values in the aggregation. Default is False.
    """
    for main_column in main_columns:
        for col in uids:
            for agg_type in aggregations:
                new_col_name = f"{main_column}_{col}_{agg_type}"
                temp_df = df[[col, main_column]].copy()
                if use_na:
                    temp_df.loc[temp_df[main_column] == -1, main_column] = np.nan
                temp_df = temp_df.groupby([col])[main_column].agg([agg_type]).reset_index().rename(columns={agg_type: new_col_name})
                temp_df.index = list(temp_df[col])
                temp_df = temp_df[new_col_name].to_dict()

                df[new_col_name] = df[col].map(temp_df).astype('float32')

                if fill_na:
                    df[new_col_name].fillna(-1, inplace=True)

                print(f"'{new_col_name}', ", end='')


def encode_CB(col1: str, col2: str, df: pd.DataFrame) -> None:
    """
    Combine two columns into a new column by concatenation and then label encode.
    
    Args:
        col1 (str): First column name.
        col2 (str): Second column name.
        df (pd.DataFrame): Combined DataFrame.
    """
    nm = f"{col1}_{col2}"
    df[nm] = df[col1].astype(str) + '_' + df[col2].astype(str)
    encode_LE(nm, df, verbose=False)
    print(f"{nm}, ", end='')
