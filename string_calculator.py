def string_adder(string_input):
    result = 0
    for char in string_input:
        if char.isdigit():
            result += int(char)
    return result


def test_simple():
    assert string_adder("") == 0
    assert string_adder("1") == 1
    assert string_adder("1,2") == 3


