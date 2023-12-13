"""
Module containing a dichotomy function for quick seach in sorted lists.
"""


def dichotomy(word, dictionnary):
    a = 0
    b = len(dictionnary) - 1
    c = (a + b) // 2
    if word > dictionnary[b]:
        return None
    while dictionnary[c] != word and b - a > 1:
        if dictionnary[c] > word:
            b = c
        else:
            a = c
        c = (a + b) // 2
    if dictionnary[c] == word:
        return c
    return None
