"""
Write a function called initcap that replicates the functionality of the string.title method, except better.
 Given a string, it should split the string on whitespace, capitalize each element of the resulting list and join them
 back into a string. Your implementation should use a list comprehension.
"""


def initcap(string):
    string_list = string.split()
    string_result = str()
    return string_result.join((s.capitalize()+' ') for s in string_list)


print(initcap("ku ku ku ku"))
