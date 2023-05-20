from typing import Callable, Tuple

def golden_ratio(a: float, b: float, func: Callable, eps: float) -> float:
    alpha = (3 - 5**(1/2)) / 2
    lyam = a + alpha * (b - a)
    mu = b - alpha * (b - a)

    f_l = func(lyam)
    f_m = func(mu)
    while b - a >= eps:
        if f_l >= f_m:
            a = lyam
            lyam = mu
            mu = b - alpha*(b - a)
            f_l = f_m
            f_m = func(mu)
        else:
            b = mu
            mu = lyam
            lyam = a + alpha*(b - a)
            f_m = f_l
            f_l = func(lyam)

    return (b+a) / 2


def try_points(a: float, b: float, func: Callable, eps: float) -> float:
    x_mid = (b - a) / 2
    f_mid = func(x_mid)

    while b - a >= eps:
        x_left = (a + x_mid) / 2
        x_right = (x_mid + b) / 2
        f_left = func(x_left)

        if f_left <= f_mid:
            b = x_mid
            x_mid = x_left
            f_mid = f_left
        else:
            f_right = func(x_right)

            if f_mid <= f_right:
                a = x_left
                b = x_right
            else:
                a = x_mid
                x_mid = x_right
                f_mid = f_right

    return (b + a)/2


methods_dict = {
    'golden': golden_ratio,
    'try_points': try_points,
}