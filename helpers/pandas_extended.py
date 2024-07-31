import os
import pandas as pd


def read_csv_if_exists(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    return None


def delete_if_exists(path):
    if os.path.exists(path):
        os.remove(path)