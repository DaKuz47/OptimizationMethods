from typing import Callable, List, Tuple

methods_dict_help = {
    'first': {
        'Golden ratio method': 'golden',
        'Try points method': 'try_points',
    },
    'second': {},
}


def first_order(x_prev, derivates: List[Callable], step_finder: Callable, eps: float) -> Tuple[int, Tuple[float]]:
    # начальный этап
    k = 0
    process = [(k, x_prev)]

    # Основной этап
    while True:
        
        alpha_f = alpha_f_generator(derivates[0], [-1*derivates[1](*x_prev), -1*derivates[2](*x_prev)], x_prev)
        alpha = step_finder(0.0, 1, alpha_f, eps)
        x_next = (x_prev[0] - alpha * derivates[1](*x_prev), x_prev[1] - alpha * derivates[2](*x_prev))
        k += 1
        process.append((k, x_next))

        grad_f = _grad(derivates, x_next)
        if abs(skalar((grad_f, grad_f))) < eps:
            break
        x_prev = x_next

    return process


def second_order(x_prev, derivates: List[Callable], step_finder: Callable, eps: float) -> Tuple[int, Tuple[float]]:
    a = [[1, 0], [0, 1]]
    k = 0
    process = [(k, x_prev)]
    omega_prev = [-x for x in _grad(derivates, x_prev)]

    while abs(skalar((omega_prev, omega_prev))) > eps:
        p = mm(a, t([omega_prev]))
        alpha_f = alpha_f_generator(derivates[0], t(p)[0], x_prev)
        alpha = step_finder(0.0, 1, alpha_f, eps)

        x_next = summator(x_prev, [t(p)[0][0]*alpha, t(p)[0][1]*alpha])
        omega_next = [-x for x in _grad(derivates, x_next)]

        d_x = substract(x_next, x_prev)
        d_omega = substract(omega_next, omega_prev)
        a = ms(a, mmc(ms(mmc(mm(t([d_x]), [d_x]), 1/skalar((d_omega, d_x))), mmc(mm(mm(mm(a, t([d_omega])), [d_omega]), t(a)), 1/skalar((mm([d_omega], a)[0], d_omega)))), -1))
        k += 1
        omega_prev = omega_next
        x_prev = x_next
        process.append((k, x_prev))
    
    return process


def alpha_f_generator(func: Callable, direction: List[float], x: Tuple[float]) -> Callable:

    def alpha_f(alpha):
        x1 = x[0] + alpha*direction[0]
        x2 = x[1] + alpha*direction[1]

        return func(x1, x2)
    
    return alpha_f


def skalar(values: List[Tuple[float]]):
    sum = 0
    for i in range(len(values[0])):
        mult = 1
        for j in range(len(values)):
            mult *= values[j][i]
        sum += mult
    
    return sum


def substract(point_a: Tuple[float], point_b: Tuple[float]) -> Tuple[float]:
    """Вычитание векторов-строк"""
    return (point_a[0] - point_b[0], point_a[1] - point_b[1])


def summator(point_a: List[float], point_b: list[float]) -> list[float]:
    """Сложение векторов-строк"""
    return (point_a[0] + point_b[0], point_a[1] + point_b[1])


def _grad(derivates: List[Callable], x: Tuple[float]) -> Tuple[float]:
    """градиент"""
    return (derivates[1](*x), derivates[2](*x))


def t(matrix: list[list[float]]) -> list[list[float]]:
    """Транспонирование матритсы"""
    t_matrix = [[matrix[i][j] for i in range(len(matrix))] for j in range(len(matrix[0]))]

    return t_matrix


def mm(matrix_a: list[list[float]], matrix_b: list[list[float]]) -> list[list[float]]:
    """Матричное умножение"""
    res_matrix = [[sum([matrix_a[j][k]*matrix_b[k][i] for k in range(len(matrix_b))]) for i in range(len(matrix_b[0]))] for j in range(len(matrix_a))]

    return res_matrix


def ms(matrix_a: list[list[float]], matrix_b: list[list[float]]) -> list[list[float]]:
    """Матричное сложение"""
    res = [[matrix_a[i][j] + matrix_b[i][j] for j in range(len(matrix_a[0]))] for i in range(len(matrix_a))]
    return res


def mmc(matrix_a: list[list[float]], const: float) -> list[list[float]]:
    """Умножение матритсы на константу"""
    for i in range(len(matrix_a)):
        for j in range(len(matrix_a[0])):
            matrix_a[i][j] *= const
    
    return matrix_a



methods_dict = {
    'first': first_order,
    'second': second_order,
}
