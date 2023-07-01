from typing import TypeVar

T = TypeVar("T", str)

# Assuming there are no repeated elements
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

    # Store the larger elements of each pair
    for first, second in zip(to_sort[::2], to_sort[1::2]):
        lower, greater = get_min_max(first, second)
        ans[greater] = lower

    return ans


def is_power_of_2(n: int) -> bool:
    return (n & (n-1) == 0) and n != 0


def make_power_of_to_sort(keys: list[T], pairs: dict[T, T], to_sort: list[T]) -> list[T]:

    unsorted = []

    curr_group = []
    prev_group_len = 0
    # Sort the lower half according to the dictionary keys
    for key in keys[2::]:
        # Add the element to the beginning of its group
        curr_group = [pairs[key]] + curr_group

        # Check if the current group needs to be added to the list
        if is_power_of_2(prev_group_len + len(curr_group)):
            # Add the group to the end of the list
            unsorted.extend(curr_group)
            # Update the last power of 2 found
            prev_group_len = len(curr_group)
            # Empty the current group
            curr_group = []

    # If the length is odd, add the last element
    if (len(to_sort) % 2):
        unsorted.append(to_sort[-1])

    return unsorted


TK = TypeVar('TK')
TV = TypeVar('TV')


def get_key_from_value(dictionary: dict[TK, TV], value: TV) -> TK:
    return next((key for key, v in dictionary.items() if v == value))


def get_rightmost_index(item_to_insert: T, sorted_list: list[T], pairs: dict[T, T]) -> int:

    try:
        # Get the element that is known to be greater than the item to insert
        upper_bound = get_key_from_value(pairs, item_to_insert)
    except StopIteration:
        return len(sorted_list) - 1
    # Get the index of this element
    return next((i for i, item in enumerate(sorted_list) if item == upper_bound)) - 1


def get_index_to_insert(item: T, dest: list[T], left: int, right: int) -> int:

    while left < right:
        # Get the middle element
        mid = (left + right) // 2

        # If the item to insert is less than the middle element,
        # update the upper end
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

        # Get the last element to compare
        rightmost = get_rightmost_index(item, sorted, pairs)
        # Start comparing from the leftmost position
        leftmost = 0

        # Calculate the index to insert the item
        index = get_index_to_insert(item, sorted, leftmost, rightmost)

        # Insert the item at the calculated position
        sorted = sorted[:index] + [item] + sorted[index:]

    return sorted


def merge_insertion(to_sort: list[T]) -> list[T]:

    # Base case when the list is already sorted
    if len(to_sort) <= 1:
        return to_sort

    # Sort all the pairs
    sorted_pairs = get_grater_in_pair(to_sort)

    # Get a list with the sorted keys
    sorted_keys = merge_insertion(list(sorted_pairs.keys()))
    # Add the element whose position is known
    sorted_keys = [sorted_pairs[sorted_keys[0]]] + sorted_keys

    lower = make_power_of_to_sort(sorted_keys, sorted_pairs, to_sort)

    # Apply the bisection algorithm to determine the position of each element
    sorted_keys = insertion(lower, sorted_keys, sorted_pairs)

    return sorted_keys


def sort():

    list_to_sort = LIST

    # Check for repeated elements
    if (len(list_to_sort) != len(set(list_to_sort))):
        return False

    list_to_sort = merge_insertion(list_to_sort)

    for element in list_to_sort:
        print(element)

    input()


if __name__ == '__main__':
    sort()
