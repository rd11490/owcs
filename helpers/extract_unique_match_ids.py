from helpers.pandas_extended import read_csv_if_exists


def extract_unique_match_ids(filename):
    frame = read_csv_if_exists(filename)
    if frame is None:
        return [], None
    else:
        return list(frame['match_id'].unique()), frame
