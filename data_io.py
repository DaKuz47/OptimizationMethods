from typing import List, Tuple


def get_task_data(file: str) -> Tuple[List[int], List[int], List[List[int]]]:
    """Считывание данных"""

    with open(file) as f:
        # Данные о пунктах приёма и назначения
        receptions = f.readline().strip().split(sep=' ')
        receptions = list(map(int, receptions))
        destinations = f.readline().strip().split(sep=' ')
        destinations = list(map(int, destinations))
        # Стоимость перевозок, проверка на корректность размерностей
        try:
            transfer_cost = []
            for line in f.readlines():
                form_line = line.strip().split(sep=" ")
                assert len(form_line) == len(destinations)
                transfer_cost.append(list(map(int, form_line)))
            assert len(transfer_cost) == len(receptions)
        except AssertionError:
            print("Неправильная размерность входных данных")
            exit()

        return receptions, destinations, transfer_cost


def get_task_table_data(file: str) -> Tuple[List[int], List[int], List[List[int]]]:
    """Считывание данных в табличном виде"""

    with open(file) as f:
        transfer_cost = []
        for line in f.readlines():
            transfer_cost.append(list(map(int, line.strip().split(sep=" "))))
        
        destinations = transfer_cost.pop()
        receptions = []

        for row in transfer_cost:
            receptions.append(row.pop(0))
        
        try:
            assert len(receptions) == len(transfer_cost)
            assert len(max(transfer_cost, key=len)) == len(destinations)
        except AssertionError:
            print("Неправильная размерность входных данных")
            exit()

        return receptions, destinations, transfer_cost
        
