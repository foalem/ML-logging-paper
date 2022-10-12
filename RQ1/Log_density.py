import pandas as pd


def log_density():
    sloc = pd.read_csv('RQ1project_size.csv')
    nl = pd.read_csv(r'C:\Users\fpatr\PycharmProjects\GitHub\data\outputs\AI_logging_data.csv', sep=';')
    nl_new = nl.groupby('project_name', as_index=False)['occurrence'].sum()
    print(nl_new)
    # data = pd.DataFrame()
    # data['project_name'] = sloc['project_name']
    # data['num_logging'] = nl_new["logging_statement"]
    # print(data)
    # df = nl_new.drop('type', 1)
    # print(df)
    final_data = sloc.merge(nl_new, how='left')
    print(final_data)
    final_data['occurrence'] = final_data['occurrence']
    final_data['log_density'] = final_data.apply(
        lambda row: row.LOC / row.occurrence, axis=1)
    # final_data['log_density'].mask(final_data['log_density'] == final_data['LOC'], 0, inplace=True)
    # final_data.loc[final_data["occurrence"] == 1.0, "occurrence"] = 0
    final_data.to_csv('log_density.csv', mode='w', index=False, header=True)

    print(final_data)


if __name__ == '__main__':
    log_density()
