"""
Write a function called make_mapping that takes two lists of equal length and returns a dictionary that maps the
values in the first list to the values in the second. The function should also take an optional keyword argument
called exclude, which expects a list. Values in the list passed as excludeshould be omitted as keys in the resulting
dictionary.
"""


def make_mapping(list1, list2, exclude):
    dict_result = {k: i for (k, i) in zip(list1, list2) if exclude.count(k) == 0}
    # if k not in exclude
    return dict_result


l1 = [5, 6, 7]
l2 = [2, 2, 2]
ex = [5, 6]

print(make_mapping(l1, l2, ex))
