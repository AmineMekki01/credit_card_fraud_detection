import gc
import pandas as pd
import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform

def group_columns_by_nan_count(df : pd.DataFrame) -> dict:
    """
    Groups columns in a DataFrame by the number of NaN values they contain.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        dict: A dictionary where keys are the number of NaNs and values are lists of tuples,
              each containing a column name and the number of NaNs.
    """
    NAN_df = df.isna()
    
    groups_by_NAN = {}
    
    for col in df.columns:
        cur_group = NAN_df[col].sum()
        
        if cur_group in groups_by_NAN:
            groups_by_NAN[cur_group].append(col)
        else:
            groups_by_NAN[cur_group] = [col]
    
    del NAN_df
    gc.collect()
    
    return groups_by_NAN


def calculate_correlation_matrix(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Calculates the correlation matrix for the given columns in the DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame.
        columns (list): List of column names to include in the correlation matrix.

    Returns:
        pd.DataFrame: The correlation matrix.
    """
    return df[columns].corr()

def cluster_columns(corr_matrix: pd.DataFrame, threshold=0.9) -> list:
    """
    Clusters columns based on their correlation matrix.

    Args:
        corr_matrix (pd.DataFrame): The correlation matrix.
        threshold (float): The correlation threshold for clustering. Defaults to 0.9.

    Returns:
        list: List of clusters, where each cluster is a list of column names.
    """
    dist_matrix = 1 - np.abs(corr_matrix)
    linkage_matrix = linkage(squareform(dist_matrix), method='average')
    cluster_labels = fcluster(linkage_matrix, threshold, criterion='distance')
    clusters = {}
    for col, cluster in zip(corr_matrix.columns, cluster_labels):
        if cluster not in clusters:
            clusters[cluster] = []
        clusters[cluster].append(col)
    
    return list(clusters.values())

def select_representative_columns(df: pd.DataFrame, clusters: list) -> list:
    """
    Selects the representative column from each cluster.

    Args:
        df (pd.DataFrame): The input DataFrame.
        clusters (list): List of clusters, where each cluster is a list of column names.

    Returns:
        list: List of selected representative column names.
    """
    selected_columns = []
    for cluster in clusters:
        max_unique = 0
        selected_col = cluster[0]
        for col in cluster:
            num_unique = df[col].nunique()
            if num_unique > max_unique:
                max_unique = num_unique
                selected_col = col
        selected_columns.append(selected_col)
    
    return selected_columns

def feature_dimensionality_reduction(df: pd.DataFrame, columns: list, threshold=0.9) -> list:
    """
    Reduces the dimensionality of the feature set by selecting representative columns 
    from clusters based on their correlations.

    Args:
        df (pd.DataFrame): The input DataFrame.
        columns (list): List of column names to include in the reduction.
        threshold (float): The correlation threshold for clustering. Defaults to 0.9.

    Returns:
        list: List of selected representative column names.
    """
    corr_matrix = calculate_correlation_matrix(df, columns)
    clusters = cluster_columns(corr_matrix, threshold)
    representative_columns = select_representative_columns(df, clusters)
    return representative_columns, clusters, corr_matrix


def process_v_columns(df: pd.DataFrame, threshold: float = 0.3) -> list:
    """
    Processes V columns by selecting representative columns based on correlation clusters
    and combines them with non-V columns.

    Args:
        df (pd.DataFrame): The input DataFrame.
        nan_groups (dict): A dictionary where keys are the number of NaNs and values are lists of columns.
        threshold (float): The correlation threshold for clustering. Defaults to 0.3.

    Returns:
        list: List of columns to keep.
    """
    nan_groups = group_columns_by_nan_count(df)

    nan_groups_with_only_v_columns = {}
    nan_groups_with_v_columns = {k: v for k, v in nan_groups.items() if any(col.startswith('V') for col in v)} 

    for key in list(nan_groups_with_v_columns.keys()):
        nan_groups_with_only_v_columns[key] = [col for col in nan_groups_with_v_columns[key] if col.startswith('V')]

    v_columns_to_keep = []
    for nan_count, columns in nan_groups_with_only_v_columns.items():
        representative_columns, clusters, corr_matrix = feature_dimensionality_reduction(df, columns, threshold)
        v_columns_to_keep.extend(representative_columns)

    non_v_columns = [col for col in df.columns if not col.startswith('V')]
    columns_to_keep = non_v_columns + v_columns_to_keep
    columns_to_keep.remove("isFraud")
    return columns_to_keep

def transaction_amt_cents(df: pd.DataFrame) -> None:
    """
    Create a new feature for the fractional part of the transaction amount.
    
    Args:
        train_df (pd.DataFrame): Training DataFrame.
        valid_df (pd.DataFrame): Validation DataFrame.
    """
    df['cents'] = (df['TransactionAmt'] - np.floor(df['TransactionAmt'])).astype('float32')
