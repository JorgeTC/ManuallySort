from typing import TypeVar

T = TypeVar("T", str)

# Asumimos que no hay elementos repetidos
LIST: list[T] = [
    ...
]


def get_min_max(el1: T, el2: T) -> tuple[T, T]:

    if isinstance(el1, int):
        print(f"Comparing {el1} and {el2}")
        return min(el1, el2), max(el1, el2)

    while True:
        ans = input(f"Choose:\n0. {el1}\n1. {el2} ")
        if ans == '0':
            return (el1, el2)
        elif ans == '1':
            return (el2, el1)

        print("Error.")


def less(el1: str, el2: str) -> bool:
    return (el1, el2) == get_min_max(el1, el2)


def get_grater_in_pair(to_sort: list[T]) -> dict[T, T]:
    ans = {}

    # Guardo cuáles son los elementos más grandes de cada pareja
    for first, second in zip(to_sort[::2], to_sort[1::2]):
        lower, greater = get_min_max(first, second)
        ans[greater] = lower

    return ans


def is_power_of_2(n: int) -> bool:
    return (n & (n-1) == 0) and n != 0


def make_power_of_to_sort(keys: list[T], pairs: dict[T, T], to_sort: list[T]) -> list[T]:

    unsorted = []

    curr_group = []
    prev_grup_len = 0
    # Ordeno la mitad baja atendiendo a las llaves del diccionario
    for key in keys[2::]:
        # Añado el elemento al inicio de su grupo
        curr_group = [pairs[key]] + curr_group

        # Compruebo si tengo que añadir el grupo actual a la lista
        if is_power_of_2(prev_grup_len + len(curr_group)):
            # Añado el grupo al final de la lista
            unsorted.extend(curr_group)
            # Actualizo el último número potencia de 2 encontrado
            prev_grup_len = len(curr_group)
            # Vacío el grupo actual
            curr_group = []

    # Si es impar, añado el último elemento
    if (len(to_sort) % 2):
        unsorted.append(to_sort[-1])

    return unsorted


TK = TypeVar('TK')
TV = TypeVar('TV')


def get_key_from_value(dictionary: dict[TK, TV], value: TV) -> TK:
    return next((key for key, v in dictionary.items() if v == value))


def get_rightmost_index(item_to_insert: T, sorted_list: list[T], pairs: dict[T, T]) -> int:

    try:
        # Obtengo el elemento que sé que es mayor que el item a insertar
        upper_bound = get_key_from_value(pairs, item_to_insert)
    except StopIteration:
        return len(sorted_list) - 1
    # Obtengo el índice de este elemento
    return next((i for i, item in enumerate(sorted_list) if item == upper_bound)) - 1


def get_index_to_insert(item: T, dest: list[T], left: int, right: int) -> int:

    while left < right:
        # Obtengo el elemento medio
        mid = (left + right) // 2

        # Si el elemento a insertar es menor que el elemento del medio,
        # actualizo el extremo superior
        if less(item, dest[mid]):
            right = mid - 1
        else:
            left = mid + 1

    if left > right:
        return left

    if less(item, dest[left]):
        return left
    else:
        return left + 1


def insertion(to_insert: list[T], sorted: list[T], pairs: dict[T, T]) -> list[T]:

    for item in to_insert:

        # Obtengo cuál será el último elemento que compruebe
        rightmost = get_rightmost_index(item, sorted, pairs)
        # Empiezo a comparar desde la izquierda del todo
        leftmost = 0

        # Calculo en qué punto debo introducir el elemento
        index = get_index_to_insert(item, sorted, leftmost, rightmost)

        # Ya tengo la posición donde debo insertarlo
        sorted = sorted[:index] + [item] + sorted[index:]

    return sorted


def merge_insertion(to_sort: list[T]) -> list[T]:

    # Caso base en el que la lista está ya ordenada
    if len(to_sort) <= 1:
        return to_sort

    # Ordeno todas las parejas
    sorted_pairs = get_grater_in_pair(to_sort)

    # Obtengo una lista con las llaves ordenadas
    sorted_keys = merge_insertion(list(sorted_pairs.keys()))
    # Añado el elemento cuya posición conozco
    sorted_keys = [sorted_pairs[sorted_keys[0]]] + sorted_keys

    lower = make_power_of_to_sort(sorted_keys, sorted_pairs, to_sort)

    # Aplico algoritmo de bisección para saber dónde va cada elemento
    sorted_keys = insertion(lower, sorted_keys, sorted_pairs)

    return sorted_keys


def sort():

    list_to_sort = LIST

    # Compruebo que no haya elementos repetidos
    if (len(list_to_sort) != len(set(list_to_sort))):
        return False

    list_to_sort = merge_insertion(list_to_sort)

    for element in list_to_sort:
        print(element)

    input()


if __name__ == '__main__':
    sort()
