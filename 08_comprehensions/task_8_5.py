
"""
Write a function called dedup_surnamesthat takes a list of surnames names and returns a set of surnames with the
case normalized to uppercase. For instance, the list ["smith", "Jones", "Smith", "BROWN"]should be transformed into
 the set {"SMITH", "JONES", "BROWN"}.
"""


def dedup_surnames(list1):
    return set([name.upper() for name in list1])


LIST = {"smith", "Jones", "Smith", "BROWN"}
print(dedup_surnames(LIST))
