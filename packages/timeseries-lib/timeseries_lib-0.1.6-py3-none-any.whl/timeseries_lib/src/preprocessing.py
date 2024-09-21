import numpy as np
import pandas as pd


def prepare_data_tm(df, date_col, target_col):
    """
    Преобразовывает данные для TimeMixer

    df: DataFrame с данными
    date_col: название столбца с датами
    target_col: название столбца с целевой переменной

    return: измененные данные
    """
    df = df.copy()
    df = df.reset_index()
    df.rename(columns={date_col: 'ds', target_col: 'y'}, inplace=True)
    df['unique_id'] = 'series'
    df = df.sort_values('ds')
    columns_to_keep = ['unique_id', 'ds', 'y']

    exog_cols = [col for col in df.columns if col not in ['unique_id', 'ds', 'y']]
    columns_to_keep.extend(exog_cols)

    df = df[columns_to_keep]

    return df