#exercises: http://www.practicepython.org/

# 1. Create a program that asks the user to enter their name and their age. Print out a message addressed to them that tells them the year that they will turn 100 years old.
def one():
    import datetime
    name = input("Enter your name:\n")
    age = int(input("Enter your age:"))
    years_left = 100 - age
    now = datetime.datetime.now()
    year = now.year
    year = year + years_left
    print("Hi " + name + "! You will turn 100 years old in the year " + str(year) + "!")

# 3. list numbers elements if less than 5
def three():
    example_list = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
    for element in example_list:
        if int(element) < 5:
            print(element)

# 5.  compare lists, return list with common values
def five():
    a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
    b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    new_list = []
    for X in a:
        if X in b and X not in new_list:
            new_list.append(X)
    print(new_list)



#launch the function you want using dictionary
function_dict = {
    'one': one,
    'three': three,
    'five': five
}
print('Available functions::')
for x in function_dict:
    print(x)
method_input = input("\nWhich fucntion would you like to run? ")
if method_input in function_dict:
    function_dict[method_input]()