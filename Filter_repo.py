import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

PATH = './data/my_data_characteristic.csv'


def load_data(path):
    data = pd.read_csv(path)
    return data


def cumul_plot_stars(data):
    plt.yticks(np.arange(0, 1500, 100))
    plt.xticks(np.arange(0, 50, 2))
    sns.ecdfplot(x='num_stars', data=data, stat='count', complementary=True)
    plt.xlim(0, 50)
    plt.grid()
    plt.show()


def cumul_plot_forks(data):
    plt.yticks(np.arange(0, 1500, 100))
    plt.xticks(np.arange(0, 50, 2))
    sns.ecdfplot(x='num_forks', data=data, stat='count', complementary=True)
    plt.xlim(0, 50)
    plt.grid()
    plt.show()


def cumul_plot_contributor(data):
    plt.yticks(np.arange(0, 1500, 100))
    plt.xticks(np.arange(0, 50, 2))
    sns.ecdfplot(x='num_contributor', data=data, stat='count', complementary=True)
    plt.xlim(0, 50)
    plt.grid()
    plt.show()


def cumul_plot_commit(data):
    plt.yticks(np.arange(0, 1500, 50))
    plt.xticks(np.arange(0, 2000, 100))
    sns.ecdfplot(x='num_commit', data=data, stat='count', complementary=True)
    plt.xlim(0, 2000)
    plt.grid()
    plt.show()


if __name__ == '__main__':
    my_data = load_data(PATH)
    cumul_plot_stars(my_data)
    cumul_plot_forks(my_data)
    cumul_plot_contributor(my_data)
    cumul_plot_commit(my_data)
