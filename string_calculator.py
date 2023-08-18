import pytest

# ----------------------------------------------------------------------------


def string_adder(string_input):

    result = 0

    comma_count = string_input.count(",")
    new_lines_count = string_input.count("\n")

    delimiters = [",", "\n"]

    if string_input.startswith("//"):
        start_index = string_input.find("//")
        end_index = string_input.find("\n")

        if start_index != -1 and end_index != -1:
            new_delimiter = (string_input[start_index + len("//"):end_index]
                             .strip())
            delimiters.append(new_delimiter)
            string_input = string_input.split("\n", 1)[1]

    for delimiter in delimiters:
        string_input = " ".join(string_input.split(delimiter))
    nums = string_input.split()

    if string_input.endswith("\n"):
        new_lines_count -= 1

    while "" in nums:
        nums.remove("")

    if len(string_input) == 0:
        return 0

    neg_nums = []

    if (comma_count + new_lines_count + 1) != len(nums):
        raise Exception(f"The {string_input} input is not valid")
    else:
        for num in nums:
            if int(num) < 0:
                neg_nums.append(num)

        for num in nums:
            if int(num) < 0:
                raise Exception(f"Negatives not allowed {neg_nums}")
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


def test_different_delimiters():
    assert string_adder("//;\n1;2") == 3


def test_negatives_nums():
    with pytest.raises(Exception):
        string_adder("-1,-2,7,9,-6")
    with pytest.raises(Exception):
        string_adder("//;\n1;-2")
