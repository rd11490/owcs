import os


def get_file_path(file):
    return os.path.dirname(os.path.realpath(file))


def create_dir_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def prep_dir(config):
    data_dir = config['dir']
    directory = f'{project_home_dir()}/data/{data_dir}'
    create_dir_if_not_exists(directory)


def project_home_dir():
    path = get_file_path(__file__)
    return f'{path}/..'

def data_home_dir():
    path = get_file_path(__file__)
    return f'{path}/../data'