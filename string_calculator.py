

def string_adder(string_input):
    result = 0
    nums = string_input.split(",")
    for num in nums:
        result += int(num)
    return result

def test_simple():
    assert string_adder("") == 0
    assert string_adder("1") == 1
    assert string_adder("1,2") == 3

def test_unknown_amount_numbers():
    assert string_adder("1,2,5,6,3,8") == 25
    assert string_adder("0,2,6,12,10") == 30
    assert string_adder("1,1,1,2,2,5,80") == 92
