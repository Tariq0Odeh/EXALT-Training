import pytest

# ----------------------------------------------------------------------------


def string_adder(string_input):

    result = 0
    temp_string_input = string_input

    comma_count = string_input.count(",")
    new_lines_count = string_input.count("\n")

    delimiters = [",", "\n"]
    for delimiter in delimiters:
        temp_string_input = " ".join(temp_string_input.split(delimiter))
    nums = temp_string_input.split()

    if string_input.endswith("\n"):
        new_lines_count -= 1

    while "" in nums:
        nums.remove("")

    if len(string_input) == 0:
        return 0

    if (comma_count + new_lines_count + 1) != len(nums):
        raise Exception(f"The {string_input} input is not valid")
    else:
        for num in nums:
            result += int(num)

    return result


# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------


def test_simple():
    assert string_adder("") == 0
    assert string_adder("1") == 1
    assert string_adder("1,2") == 3


def test_unknown_amount_numbers():
    assert string_adder("1,2,5,6,3,8") == 25
    assert string_adder("0,2,6,12,10") == 30
    assert string_adder("1,1,1,2,2,5,80") == 92


def test_new_lines():
    assert string_adder("1\n2,3") == 6
    with pytest.raises(Exception):
        string_adder("1,\n")
    with pytest.raises(Exception):
        string_adder("\n,1,")
