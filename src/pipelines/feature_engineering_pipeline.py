import pandas as pd
import numpy as np
from src.components.feature_engineering import transaction_amt_cents, label_encode_and_memory_reduce, encode_FE, encode_CB, encode_AG


STAGE2 = 'Feature Engineering'


class FeatureEngineeringPipeline:
    def __init__(self):
        pass
        
    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Run feature engineering on the DataFrame.
        
        Args:
            df (pd.DataFrame): Combined DataFrame.
            
        Returns:
            pd.DataFrame: Processed DataFrame.
        """
        df['cents'] = (df['TransactionAmt'] - np.floor(df['TransactionAmt'])).astype('float32')
        freq_encode_columns = ['addr1', 'card1', 'card2', 'card3', 'P_emaildomain']
        transaction_amt_cents(df)
        label_encode_and_memory_reduce(df)
        encode_FE(df, freq_encode_columns)
        encode_CB('card1', 'addr1', df)
        encode_CB('card1_addr1', 'P_emaildomain', df)
        encode_FE(df, ['card1_addr1', 'card1_addr1_P_emaildomain'])
        encode_AG(['TransactionAmt', 'D9', 'D11'], ['card1', 'card1_addr1', 'card1_addr1_P_emaildomain'], ['mean', 'std'], df=df, use_na=True)
        
        return df