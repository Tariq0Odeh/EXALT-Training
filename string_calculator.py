
def string_adder(string_input):
    result = 0

    if string_input.endswith('\n'):
        print("The input is NOT valid")
        return
    else:
        for char in string_input:
            if char.isdigit():
                result += int(char)

    print(result)


print("---------------")
first_input = ""
print("first_input")
string_adder(first_input)

print("---------------")
second_input = "1,6,2"
print("second_input")
string_adder(second_input)

print("---------------")
third_input = "1,6\n,2"
print("third_input")
string_adder(third_input)

print("---------------")
forth_input = "1,6,2\n"
print("forth_input")
string_adder(forth_input)

print("---------------")
