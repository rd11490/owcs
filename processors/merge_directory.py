import pandas as pd
import os

def list_files(directory):
    out = []
    for filename in os.listdir(directory):
        file = os.path.join(directory, filename)
        if os.path.isfile(file) and '.csv' in file:
            out.append(file)
    return out


def merge_directory(source, destination):
    files = list_files(source)
    dfs = []
    for f in files:
        try:
            df = pd.read_csv(f)
            if not df.empty:
                dfs.append(df)
        except:
            pass

    merged = pd.concat(dfs).reset_index(drop=True)
    merged.to_csv(destination, index=False)