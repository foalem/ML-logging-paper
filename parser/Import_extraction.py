import os
import ast
import pandas as pd
from collections import namedtuple

ROOT_DIR = r'C:\Users\fpatr\PycharmProjects\GitHub\data\outputs\clones'
PATH = r'C:\Users\fpatr\PycharmProjects\GitHub'


def get_project_python_files(directory):
    # directory = os.path.abspath(directory)
    # print(directory)
    list_of_files = list()
    for (dirpath, dirnames, filenames) in os.walk(directory):
        py_files = list()
        for file in filenames:
            if file.endswith('.py'):
                py_files.append(os.path.join(dirpath, file))
        list_of_files.extend(py_files)
    return list_of_files


file_contents = []


class FuncParser(ast.NodeVisitor):
    def visit_Import(self, node):
        tempImpo = node.names
        if (tempImpo != None):
            listImpo = tempImpo[0]
            Impo = listImpo.name
            file_contents.append(Impo)
            ast.NodeVisitor.generic_visit(self, node)

    def visit_ImportFrom(self, node):
        module = node.module
        file_contents.append(module)
        ast.NodeVisitor.generic_visit(self, node)

    def generic_visit(self, node):
        ast.NodeVisitor.generic_visit(self, node)


def scanForImports(file):
    try:
        with open(f'{file}', 'r', encoding="utf8") as r_file:
            source_file = r_file.read()
    except Exception as e:
        print("Error on {}:{}".format(r_file, e))
        pass
    try:
        ast_commit = ast.parse(source_file)
        bf_obj = FuncParser()
        bf_tree = ast.parse(ast_commit)
        bf_obj.visit(bf_tree)
    except Exception as e:
        print("Error on {}: {}".format(r_file, e))
        pass
    return file_contents



def main():
    dir_list = os.listdir(ROOT_DIR)
    import_path = PATH + '/data/outputs/import'
    all_import_ = list()
    # print(dir_list)
    i = 0
    j = 0
    for project_name in dir_list:
        project_path = ROOT_DIR + f'/{project_name}'
        print(project_path)
        i += 1
        list_of_py_file = get_project_python_files(project_path)
        list_of_import = list()
        # if i == 10:
        #     break
        for file in list_of_py_file:
            j += 1
            list_of_import.extend(scanForImports(file))
            # if j == 10:
            #     break
        all_import_ = list_of_import
        # print(all_import_)
    single_import = list(dict.fromkeys(all_import_))
    print(single_import)
    df = pd.DataFrame(single_import, columns=["Import"])
    if not os.path.exists(PATH + '/data/outputs/import'):
        os.mkdir(PATH + '/data/outputs/import')
    df.to_csv(import_path + '.csv', index=False)


if __name__ == '__main__':
    main()
