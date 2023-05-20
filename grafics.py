from typing import Callable, List, Tuple

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

def f_levels(func: Callable, points: List[Tuple[float]]) -> None:
    points_x = [point[0] for point in points]
    points_y = [point[1] for point in points]
    path = Line2D(points_x, points_y)
    
    ax = plt.subplot(1, 1, 1)
    
    x_min = y_min = -10
    x_max = y_max = 10
    n = 100
    h_x = (x_max - x_min)/(n - 1)
    h_y = (y_max - y_min)/(n - 1)

    x_grid = [[x_min + i*h_x for i in range(n)] for _ in range(n)]
    y_grid = [[y_min + i*h_y]*n for i in range(n)]
    z_grid = [[func(x_grid[i][j], y_grid[i][j]) for j in range(n)] for i in range(n)]

    values = ax.contour(x_grid, y_grid, z_grid, levels=30)
    ax.clabel(values)
    ax.add_line(path)
    ax.scatter(points_x, points_y, marker='*')
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    zoom_factory(ax)
    plt.axis('equal')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Уровни исходной функции\nГрадиентная ломаная')
    plt.show()


def zoom_factory(ax,base_scale = 2.):
        def zoom_fun(event):
            # get the current x and y limits
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()
            cur_xrange = (cur_xlim[1] - cur_xlim[0])*.5
            cur_yrange = (cur_ylim[1] - cur_ylim[0])*.5
            xdata = event.xdata # get event x location
            ydata = event.ydata # get event y location
            if event.button == 'up':
                # deal with zoom in
                scale_factor = 1/base_scale
            elif event.button == 'down':
                # deal with zoom out
                scale_factor = base_scale
            else:
                # deal with something that should never happen
                scale_factor = 1
                print(event.button)
            # set new limits
            ax.set_xlim([xdata - cur_xrange*scale_factor,
                        xdata + cur_xrange*scale_factor])
            ax.set_ylim([ydata - cur_yrange*scale_factor,
                        ydata + cur_yrange*scale_factor])
            plt.draw() # force re-draw

        fig = ax.get_figure() # get the figure of interest
        # attach the call back
        fig.canvas.mpl_connect('scroll_event',zoom_fun)

        #return the function
        return zoom_fun