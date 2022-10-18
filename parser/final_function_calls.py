import ast
import pandas as pd
import os
from collections import deque

ROOD_DIR = os.path.abspath(os.getcwd())
PROJECT_DIR = r'C:\Users\fpatr\PycharmProjects\GitHub\data\outputs\clones'
OUT_TARGET = r'C:\Users\fpatr\PycharmProjects\GitHub\data\outputs'


class FuncCallVisitor(ast.NodeVisitor):
    def __init__(self):
        self._name = deque()

    @property
    def name(self):
        return '.'.join(self._name)

    @name.deleter
    def name(self):
        self._name.clear()

    def visit_Name(self, node):
        self._name.appendleft(node.id)

    def visit_Attribute(self, node):
        try:
            self._name.appendleft(node.attr)
            self._name.appendleft(node.value.id)
        except AttributeError:
            self.generic_visit(node)


def get_func_calls(tree):
    func_calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            callvisitor = FuncCallVisitor()
            callvisitor.visit(node.func)
            func_calls.append(callvisitor.name)

    return func_calls


def get_project_python_files(directory):
    list_of_files = list()
    for (dirpath, dirnames, filenames) in os.walk(directory):
        py_files = list()
        for file in filenames:
            if file.endswith('.py') or file.endswith('.ipynb'):
                py_files.append(os.path.join(dirpath, file))
        list_of_files.extend(py_files)
    return list_of_files


def get_folder(folder_path):
    all_path = []
    folder = os.listdir(folder_path)
    print(folder)
    for project_name in folder:
        project_path = folder_path + f'\{project_name}'
        all_path.append(project_path)
    print(all_path)
    return all_path


def main():
    name_repo = []
    path_repo = []
    state_log = []
    occurance = []
    log_common = dict()
    final_data = pd.DataFrame()
    df_data = pd.read_csv(r"C:\Users\fpatr\PycharmProjects\GitHub\RQ1\ML-logging.csv", sep=";")
    list_logging = df_data["logging_statement"].to_list()
    list_project = df_data["project_name"].to_list()
    if os.path.exists(OUT_TARGET + '/logging_.csv'):
        os.remove(OUT_TARGET + '/logging_.csv')
    all_project_folder = get_folder(PROJECT_DIR)
    for fold in all_project_folder:
        project_name = fold.split('\\')[8]
        if project_name in list_project:
            list_file = get_project_python_files(fold)
            for file in list_file:
                try:
                    tree = ast.parse(open(file, encoding="utf8").read())
                except Exception as e:
                    print("Error on {}: {}".format(file, e))
                logg = list(set(get_func_calls(tree)) & set(list_logging))
                if len(logg):
                    log_common = dict((x, get_func_calls(tree).count(x)) for x in set(logg))
                    print(log_common)
                    print(logg, file)
                    for statement in logg:
                        name_repo.append(project_name)
                        path_repo.append(file)
                        state_log.append(statement)
                        occurance.append(log_common[statement])
    final_data['project'] = name_repo
    final_data['path'] = path_repo
    final_data['statement'] = state_log
    final_data['occurrence'] = occurance
    final_data.to_csv(OUT_TARGET + '/logging_.csv', mode='w', index=False, sep=',')


if __name__ == '__main__':
    main()
