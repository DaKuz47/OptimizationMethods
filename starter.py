import argparse

import data_io as dio
from methods.simplex import TransportTask

FILE = 'data.txt'


def pars_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--table', action='store_true')
    return parser.parse_args()


if __name__ == '__main__':
    arguments = pars_arguments()

    receptions, destinations, transfer_cost = dio.get_task_table_data(FILE) if arguments.table else dio.get_task_data(FILE)
    
    task = TransportTask(receptions, destinations, transfer_cost)
    print(task.get_solution())