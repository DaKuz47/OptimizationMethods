import argparse

from methods import methods_dict_help, skalar, substract, t
from methods import methods_dict as meth_dict
from minimize import methods_dict as min_dict
from grafics import f_levels

counter = 0

def f(x1: float, x2: float) -> float:
    """Исходная функтсия"""
    global counter
    counter += 1
    return x1 + x2 + 4 * (1 + 4 * x1**2 + 2 * x2**2)**(1/2) 


def dfx1(x1: float, x2: float) -> float:
    """Частная производная по x1"""
    global counter
    counter += 1
    return 1 + (16 * x1) / (1 + 4 * x1**2 + 2 * x2**2)**(1/2)


def dfx2(x1: float, x2: float) -> float:
    """Частная производная по x2"""
    global counter
    counter += 1
    return 1 + (8 * x2) / (1 + 4 * x1**2 + 2 * x2**2)**(1/2)


def pars_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--method_order', type=str, help='method name')
    parser.add_argument('--step_finder', type=str, help='method for find step for first order method')
    parser.add_argument('--skalar', help="Calulate skalar multiplication", action="store_true")
    parser.add_argument('--list', help='Show list of methods', action="store_true")
    return parser.parse_args()


if __name__ == '__main__':
    arguments = pars_arguments()
    method = None
    step_finder = None
    # вывод списка доступных методов
    if arguments.list:
        print('Method orders:')
        for key in methods_dict_help.keys():
            print(f'-{key}')
            if methods_dict_help[key]:
                print('\tStepfinder methods:')
                for method in methods_dict_help[key].keys():
                    print(f'\t-{method}: {methods_dict_help[key][method]}')        
        exit()

    if arguments.method_order is None:
        print("type --help")
        exit()
    
    if arguments.step_finder is None:
        arguments.step_finder = 'golden'
    

    x = list(map(float, input('Введите начальное приближение: ').split()))
    eps = float(input('Задайте точность: '))


    res = meth_dict[arguments.method_order](x, (f, dfx1, dfx2), min_dict[arguments.step_finder], eps)


    print(f"k = {res[-1][0]}, x_min = {res[-1][1]}")

    print(f"Количество обращений N = {counter}")
    if arguments.skalar:
        for i in range(len(res)-2):
            print("Скалярное произведение %d и %d отрезков = %.4f" % (i+1, i+2, skalar([substract(res[i][1], res[i+1][1]), substract(res[i+2][1], res[i+1][1])])))

    
    f_levels(f, [item[1] for item in res])
