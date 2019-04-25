
"""
Write a function called compress_dict_keys that takes a dictionary with string keys and returns a new dictionary with
the vowels removed from the keys. For instance, the dictionary {"foo": 1, "bar": 2} should be transformed into
{"f": 1, "br": 2}. The function should use a list comprehension nested inside a dict comprehension.
"""


def compress_dict_keys(dict1):
    vowels = ('a', 'e', 'i', 'o', 'u')
    # "".join(c for c in k if c not in 'aeiou"):v ...
    return {str([k.replace(x, '') for x in vowels if k.count(x) > 1]).strip('[\'\']'): v for k, v in dict1.items()}


dicti = {'beeebebebebethth': 1, 'baaar': 2}
print(compress_dict_keys(dicti))
