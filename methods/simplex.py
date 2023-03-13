from typing import List, Tuple

def _get_first_iteration(rec: List[int], dest: List[int]) -> Tuple[List[int], List[int], List[List[int]]]:
    """Метод северо-западного угла для построения первого приближения"""
    m = len(rec)
    n = len(dest)

    # Матритса m на n с пустыми значениями
    first_iteration = [[None for i in range(n)] for i in range(m)]
    i, j = 0, 0
    cell_count = 0 # Число заполненных клеток

    while i != m and j != n:
        cell_count += 1
        val = min(rec[i], dest[j])
        first_iteration[i][j] = val
        rec[i] -= val
        dest[j] -= val
        
        # Выбираем направление следующего шага
        if rec[i] < dest[j]:
            i += 1
        else:
            j += 1
    
    assert cell_count == m + n -1

    return rec, dest, first_iteration
