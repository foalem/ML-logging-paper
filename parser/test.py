import os
import pandas as pd
import csv
from parser.parser_info import ModuleInfo

PROJECT_DIR = r'C:\Users\fpatr\PycharmProjects\GitHub\data\outputs\clones'
OUT_TARGET = r'C:\Users\fpatr\PycharmProjects\GitHub\data\outputs'


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
    final_data = pd.DataFrame()
    data = pd.read_csv(r'C:\Users\fpatr\PycharmProjects\GitHub\RQ1\ML-logging.csv', sep=';')
    column = data['project_name'].drop_duplicates().values.tolist()
    print(column)
    all_project_folder = get_folder(PROJECT_DIR)
    for fold in all_project_folder:
        project_name = fold.split('\\')[8]
        if project_name in column:
            print("Project name:", project_name)
            final_data['project_name'] = project_name
            list_file = get_project_python_files(fold)
            for file in list_file:
                try:
                    print(file)
                    m = ModuleInfo(r'C:\Users\fpatr\PycharmProjects\GitHub\data\outputs\clones\Air-Pollution\app\app.py')
                    print(m)
                except Exception as e:
                    print("Error on {}: {}".format(file, e))
                ft = m.get_funcs_info()
                # cl = m.get_classes_info()
                for index in range(0, len(list(ft.keys())) - 1):
                    logging_list = set(data['logging_statement']).intersection(list(ft.values())[index]['calls'])
                    if len(logging_list):
                        data_match = [project_name, file, list(ft.keys())[index], logging_list]
                        with open(OUT_TARGET + '/logging_localisation.csv', 'a', newline='') as f:
                            writer = csv.writer(f)
                            writer.writerow(data_match)


# m = ModuleInfo(r"C:\Users\fpatr\PycharmProjects\GitHub\data\outputs\clones\Air-Pollution\app\app.py")
# imports = m.get_imports()
# print(imports.get_imported_names())
# print(m.get_funcs_info())
# p = m.get_funcs_info()
# print(type(p))
# print(len(list(p.keys())))
# print(len(list(p.values())[0]['calls']))
# print(list(p.keys())[0])
# print(list(p.values())[0]['calls'])
# print(m.get_classes_info())
# output

# in order to get the alias names used
# print(imports.get_imported_names(use_alias=True))
# output
if __name__ == '__main__':
    main()
