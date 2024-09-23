"""
    This is the standard way to
    include a multiple-line comment in
    your code.
"""


def print_lol(the_list: list, indent=False, level=1):
    """
    :param indent:
    :param level:
    :param the_list:
    :return: 解析List列表并显示所有子项
    """
    for item in the_list:
        if isinstance(item, list):
            print_lol(item, indent, level + 1)
        else:
            if indent:
                for _ in range(level):
                    print("\t", end="")
            print(item)
