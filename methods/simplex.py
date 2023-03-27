from typing import List, Tuple


class TransportTask:
    """Содержит внутри себя состояние задачи"""

    def __init__(self, rec: List[int], dest: List[int], cost: List[List[int]]) -> None:
        """Инитсиализирует задачу исходными данными"""
        self.receptions = rec
        self.destinations = dest
        self.transfer_cost = cost

        self.m_rec = len(self.receptions)
        self.n_dest = len(self.destinations)

        # Матритса перевозок, изначально пустая, количество заполненных клеток 0
        self.transfer_plan = [[None for i in range(self.n_dest)] for i in range(self.m_rec)]
        self.cell_count = 0
        self.cells = []

    def get_solution(self) -> List[List[int]]:
        """Решение транспортной задачи"""

        # Первое приближение
        self._first_iteration()
        # print("First: ", self.transfer_plan)
        self._correct_plan()
        # Пока решение не оптимально приближаем дальше
        while self._check_optimality() is False:
            self._next_iteration()
            # print("Iter: ", self.transfer_plan)
            self._correct_plan()
            # print("Correction: ", self.transfer_plan)
        
        return self.transfer_plan

    def _first_iteration(self) -> None:
        """Метод северо-западного угла для построения первого приближения"""
        i, j = 0, 0
        rec = self.receptions[:]
        dest = self.destinations[:]

        while i != self.m_rec and j != self.n_dest:
            # Сохраняем сведения о заполненных клетках
            self.cell_count += 1
            self.cells.append((i, j))

            val = min(rec[i], dest[j])
            self.transfer_plan[i][j] = val
            rec[i] -= val
            dest[j] -= val
            
            # Выбираем направление следующего шага
            if rec[i] < dest[j]:
                i += 1
            else:
                j += 1
    
    def _correct_plan(self) -> None:
        """Корректировка плана"""

        if self.m_rec + self.n_dest - 1 == self.cell_count:
            return
        
        iter_cells = iter(self.cells)
        # Если заполненных клеток меньше, чем нужно
        while self.m_rec + self.n_dest - 1 > self.cell_count:
            cell = next(iter_cells)
            i, j = cell
            if i < self.m_rec and j < self.n_dest:
                # Ищем диагональные ячейки и добавляем нулевого "соседа"
                if (
                    (i + 1, j) not in self.cells and
                    (i, j + 1) not in self.cells and
                    (i + 1, j + 1) in self.cells
                ):
                    self.cell_count += 1
                    self.cells.append((i + 1, j))
                    self.transfer_plan[i + 1][j] = 0

        # Если заполненных ячеек больше, чем нужно, делаем нулевые пустыми
        while self.m_rec + self.n_dest - 1 < self.cell_count:
            cell = next(iter_cells)
            i, j = cell
            if self.transfer_plan[i][j] == 0:
                if (
                    len([q for q in range(self.m_rec) if self.transfer_plan[q][j]]) != 2 and
                    len([p for p in range(self.n_dest) if self.transfer_plan[i][p]]) != 2
                ):
                    self.transfer_plan[i][j] = None
                    self.cell_count -= 1
                    self.cells.remove((i, j))
    
    def _check_optimality(self) -> bool:
        """Проверка оптимальности пути"""

        v, u = self._find_potentials()

        for i in range(self.m_rec):
            for j in range(self.n_dest):
                if (i, j) not in self.cells and v[j] - u[i] > self.transfer_cost[i][j]:
                    return False

        return True
    
    def _find_potentials(self) -> Tuple[List[int], List[int]]:
        """Нахождение потентсиалов"""

        def get_potentilas_v(v: List[int], u: List[int], u_ind: int, cells: List[Tuple[int]]):
            """Нахождение всех vi, стоящих в паре c заданным u"""

            finded_v = []

            for cell in [cell for cell in cells if cell[0] == u_ind]:
                v[cell[1]] = self.transfer_cost[u_ind][cell[1]] + u[u_ind]
                finded_v.append(cell[1])
                cells.remove(cell)

            for v_ind in finded_v:
                get_potentilas_u(v, u, v_ind, cells)


        def get_potentilas_u(v: List[int], u: List[int], v_ind: int, cells: List[Tuple[int]]):
            """"Нахождение всех ui, стоящих в паре c заданным v"""

            finded_u = []

            for cell in [cell for cell in cells if cell[1] == v_ind]:
                u[cell[0]] = v[v_ind] - self.transfer_cost[cell[0]][v_ind]
                finded_u.append(cell[0])
                cells.remove(cell)

            for u_ind in finded_u:
                get_potentilas_v(v, u, u_ind, cells)
        
        v = [None] * self.n_dest
        u = [None] * self.m_rec
        u[0] = 0

        cells_clone = self.cells[:]

        get_potentilas_v(v, u, 0, cells_clone)

        return v, u
    
    def _get_cycle(self) -> List[Tuple[int]]:
        """Вычисление тсикла"""

        navigation = {
            1: (-1, 0),
            2: (0, 1),
            3: (1, 0),
            4: (0, -1)
        }

        def _forward_cells(cell: Tuple[int], cells: List[Tuple[int]], nav: int) -> List[Tuple[int]]:
            """Доступные на заданном направлении ячейки"""

            di, dj = navigation[nav]
            i, j = cell
            j += dj
            i += di
            available_cells = []
            while (
                j >= 0 and j <= self.n_dest and
                i >= 0 and i <= self.m_rec
                ):
                if (i, j) in cells:
                    available_cells.append((i, j))
                j += dj
                i += di 

            return available_cells
        
        def _get_cycle_recursive(cell: Tuple[int], cells: List[Tuple[int]], nav: int) -> List[Tuple[int]]:
            """Рекурсивная часть вычисления пути"""

            path = []
            
            # В каждой ячейке можем повернуть либо направо, либо налево
            next_nav1 = 1 if nav == 4 else nav + 1
            next_nav2 = 4 if nav == 1 else nav - 1

            available_cells = _forward_cells(cell, cells, nav)
            for available_cell in available_cells:
                if available_cell == self.empty_cell:
                    return [available_cell]
                
                cells.remove(available_cell)
                path1 = _get_cycle_recursive(available_cell, cells, next_nav1)
                path2 = _get_cycle_recursive(available_cell, cells, next_nav2)

                if len(path1) == len(path2):
                    continue

                if len(path1) != 0:
                    path = [available_cell] + path1
                
                if len(path2) != 0:
                    path = [available_cell] + path2
                
                break

            return path
        
        # Поиск пустой ячейки следующей за предыдущей
        if getattr(self, 'empty_cell', None) is None:
            self.empty_cell = self._find_first_empty_cell()
        else:
            self.empty_cell = self._find_next_empty_cell()
            if self.empty_cell is None:
                self.empty_cell = self._find_first_empty_cell()
        print("plan; ", self.transfer_plan)
        print("Empty: ", self.empty_cell)
        # Добавляем пустую ячейку к непустым в качестве вспомогательной
        self.cells.append(self.empty_cell)
        # Ищем путь по всем возможным направлениям
        for nav in range(1, 5):
            path = _get_cycle_recursive(self.empty_cell, self.cells[:], nav)
            if len(path):
                break

        path.pop()
        path = [self.empty_cell] + path

        self.cells.remove(self.empty_cell)

        return path
    
    def _next_iteration(self) -> None:
        """Следующее прилижение плана перевозок"""

        path = self._get_cycle()
        # Элементы пути со знаком минус и плюс
        minus_elements = [path[i] for i in range(len(path)) if i % 2 == 1]
        plus_elements = [path[i] for i in range(len(path)) if i % 2 == 0]
        # Элемент с минимальным значением
        dif = min(self.transfer_plan[i][j] for i, j in minus_elements)

        for i,j in minus_elements:
            if self.transfer_plan[i][j] is None:
                self.transfer_plan[i][j] = -1 * dif
                self.cell_count += 1
                self.cells.append((i, j))
            else:
                self.transfer_plan[i][j] -= dif

        for i,j in plus_elements:
            if self.transfer_plan[i][j] is None:
                self.transfer_plan[i][j] = dif
                self.cell_count += 1
                self.cells.append((i, j))
            else:
                self.transfer_plan[i][j] += dif
    
    def _find_first_empty_cell(self) -> Tuple[int]:
        for i in range(self.m_rec):
            for j in range(self.n_dest):
                if self.transfer_plan[i][j] is None:
                    return i, j

    def _find_next_empty_cell(self) -> Tuple[int]:
        for j in range(self.empty_cell[1], self.n_dest):
            if self.transfer_plan[self.empty_cell[0]][j] is None:
                return self.empty_cell[0], j

        for i in range(self.empty_cell[0] + 1, self.m_rec):
            for j in range(0, self.n_dest):
                if self.transfer_plan[i][j] is None:
                    return i, j





    
