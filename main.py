import argparse

from methods import Method, methods_disc
from utils import nice_print

# исходная функция
def func(x: float) -> float:
    return (x + 5)*x + 6

def pars_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--method', type=str, help='method name')
    parser.add_argument('--list', help='Show list of methods', action="store_true")
    return parser.parse_args()

if __name__ == '__main__':
    arguments = pars_arguments()
    if arguments.list:
        for key, value in methods_disc.items():
            print(f"{key} - {value}")
        
        exit()
    
    if arguments.method:
        a, b = map(float, input('Введите границы интервала: ').split())
        eps = float(input('Задайте точность: '))

        method = Method(func, arguments.method)
        a, b = method.calculate(a, b, 0.1)
        count = method.get_call_function_count()

        nice_print(a, b, count)
