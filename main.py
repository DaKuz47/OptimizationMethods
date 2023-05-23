import argparse

from methods import methods_dict_help, skalar, substract, t
from methods import methods_dict as meth_dict
from minimize import methods_dict as min_dict
from grafics import f_levels


def pars_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--method', type=str, help='method name')
    parser.add_argument('--list', help='Show list of methods', action="store_true")
    return parser.parse_args()


if __name__ == '__main__':
    arguments = pars_arguments()
    method = None
    step_finder = None
    # вывод списка доступных методов
    if arguments.list:
        print('Methods')
        for method in methods_dict_help:
            print(f"\t-{method}")
        exit()
    

    x = list(map(float, input('Введите начальное приближение: ').split()))
    eps = float(input('Задайте точность: '))


    res = meth_dict[arguments.method_order](x, (f, dfx1, dfx2), min_dict[arguments.step_finder], eps)


    print(f"k = {res[-1][0]}, x_min = {res[-1][1]}")

    print(counter)
    # for i in range(len(res)-2):
    #     print("Скалярное произведение %d и %d отрезков = %.4f" % (i+1, i+2, skalar([substract(res[i][1], res[i+1][1]), substract(res[i+2][1], res[i+1][1])])))

    
    f_levels(f, [item[1] for item in res])
