
"""
Write a function called generate_matrixthat takes two positional arguments – m and n – and a keyword argument default
that specifies the value for each position. It should use a nested list comprehension to generate a list of lists with
the given dimensions.
If default is provided, each position should have the given value, otherwise the matrix should be populated with zeroes
"""


def generate_matrix(m, n, default=0):
    return [[default for x in range(n)]for y in range(m)]


print(generate_matrix(3, 5, 0))

