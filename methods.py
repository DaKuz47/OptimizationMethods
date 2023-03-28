# from abc import ABC
from typing import Callable, Tuple

class Method():
    def __init__(self, func: Callable, method_name: str) -> None:
        self._set_tracable_func(func)
        self._name = method_name
    
    def _set_tracable_func(self, func: Callable) -> None:
        # функция со счётчиком
        def tracable_func(x: float) -> float:
            if getattr(tracable_func, 'count', None):
                tracable_func.count += 1
            else:
                tracable_func.count = 1
            return func(x)
        
        self._trace_func = tracable_func
    
    def calculate(self, a: float, b: float, eps: float, *args) -> Tuple[float, float]:
        self._trace_func.count = 0
        a, b = methods_name[self._name](a, b, self._trace_func, eps, *args)
        return a, b
    
    def get_call_function_count(self) -> int:
        return getattr(self._trace_func, 'count', 0)

# метод равномерного поиска
def _uniform_search(a: float, b: float, func: Callable, eps: float, n: int = 10) -> Tuple[float, float]:
    while b - a >= eps:
        h = (b - a) / n # шаг сетки
        grid_x = [a + i * h for i in range(0, n + 1)] # сама сетка
        grid_f = [func(x) for x in grid_x]

        min_f = min(grid_f)
        a = grid_x[grid_f.index(min_f, 1) - 1]
        b = grid_x[grid_f.index(min_f) + 1]

    return a, b

# метод золотого сечения
def _golden_ratio(a: float, b: float, func: Callable, eps: float) -> Tuple[float, float]:
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
    return a, b
 
# метод пробных точек
def _try_points(a: float, b: float, func: Callable, eps: float) -> Tuple[float, float]:
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

    return a, b

methods_name = {
    "golden": _golden_ratio,
    "trypts": _try_points,
    "search": _uniform_search,
}

methods_disc = {
    "golden": "Golden ratio method",
    "trypts": "Try points method",
    "search": "Uniform search method",
}
