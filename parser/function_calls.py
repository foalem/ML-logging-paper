import ast
import argparse
import pandas as pd
import os
from itertools import repeat
from collections import deque
import csv

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
    ct = 0
    i = 0
    log_list = ["warnings","logging","logger","_log.info","EarlyStopping", "callbacks"]
    if os.path.exists(OUT_TARGET + '/logging_statement.csv'):
        os.remove(OUT_TARGET + '/logging_statement.csv')
    all_project_folder = get_folder(PROJECT_DIR)
    for fold in all_project_folder:
        project_name = fold.split('\\')[8]
        # i+=1
        # if i == 3:
        #     break
        print("Project name:", project_name)
        list_file = get_project_python_files(fold)
        for file in list_file:
            try:
                tree = ast.parse(open(file, encoding="utf8").read())
            except Exception as e:
                print("Error on {}: {}".format(file, e))
            # print(get_func_calls(tree))
            for log in get_func_calls(tree):
                for exp in log_list:
                    if exp in log:
                        ct += 1
                        data = [project_name, log]
                        with open(OUT_TARGET + '/logging_statement5.csv', 'a', newline='') as f:
                            writer = csv.writer(f)
                            writer.writerow(data)
                    # print(log)
    #                 logging_call.append(log)
    #     print(logging_call)
    #     res = dict(zip(repeat(project_name), logging_call))
    #     data.append(res)
    #     print(data)
    # df = pd.DataFrame.from_dict(data)
    # df.to_csv(OUT_TARGET+'/logging_statement.csv', index=False, header=False)


if __name__ == '__main__':
    main()
