import os


def is_exist_path(path):
    return os.path.exists(path) and os.path.isdir(path)


def is_exist_file(full_path_filename):
    return os.path.exists(full_path_filename) and os.path.isfile(full_path_filename)


def create_path_if_not_exits(path):
    if not is_exist_path(path):
        os.makedirs(path)


def get_enviroment_variable(variable):
    return os.getenv(variable)


def list_files(path, filter_extension):
    if filter_extension:
        return list(
            filter(lambda file: file.endswith(filter_extension), os.listdir(path))
        )
    else:
        return list(os.listdir(path))
