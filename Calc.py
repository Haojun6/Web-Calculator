from decimal import *
import math
OPERATORS = ('+', '-', '*', '/', '^', '(', ')', '.', 'l', 'o', 'g', 'e', 'x', 'p')
DIGITS = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0')
stack = []


# check if input is valid
def is_valid(lst):
    for i in lst:
        if i not in OPERATORS and i not in DIGITS:
            return False
    return True


# main calc part calls bracket to store and load stack
def calc(lst):
    bracket(lst)
    while stack.__len__()>1 or stack.__len__()==0:
        new_list = stack.copy()
        stack.clear()
        bracket(new_list)
    return stack[0]


# classify list into two lists of numbers and operators
def classify(lst):
    number_list=[]
    operator_list = []
    number = ''
    for i in lst:
        if not is_operator(i) or i == '.':
            number = number + i
        else:
            number_list.append(number)
            operator_list.append(i)
            number = ''
    number_list.append(number)
    return number_list, operator_list


# do operation in correct order
def operation(number_list, operator_list):
    try:
        log_exp(number_list, operator_list)
        power(number_list, operator_list)
        mul_div(number_list, operator_list)
        add_sub(number_list, operator_list)
    except ZeroDivisionError:
        print("You cannot divide a number by zero!")
        quit()
    except InvalidOperation:
        print("Invalid input: please type like log3+-5*exp(4.2)/(5+7) or log(3)+(-5)*exp(4.2)/(5+7)")
        quit()
    except ValueError:
        print("Mathematical mistakes: the domain of log must be positive")
        quit()
    return number_list, operator_list


# store the content outside brackets and compute content inside brackets and store the result in stack
def bracket(lst):
    count = 0
    if '(' not in lst:
        number_list = classify(lst)[0]
        operator_list = classify(lst)[1]
        if stack:
            stack.pop()
        stack.append(str(operation(number_list, operator_list)[0][0]))
        if '(' in stack:
            bracket_number = stack.count('(')
            for j in range (0,bracket_number):
                stack.append(')')
        return
    else:
        i = 0
        while i < lst.__len__():
            stack.append(lst[i])
            if str(lst[i]) == '(':
                count = count + 1
                new_list = []
                i += 1
                while  count != 0:
                    if str(lst[i]) == '(':
                        count += 1
                    if str(lst[i]) == ')':
                        count -= 1
                    if count == 0:
                        break
                    new_list.append(lst[i])
                    i += 1
                bracket(new_list)
            i += 1


# do log and exp calculation
def log_exp(number_list, operator_list):
    i = 0
    while i < operator_list.__len__():
        if operator_list[i] == 'l':
            if operator_list.__len__() > i + 2 and operator_list[i+1] == 'o' and operator_list[i+2] == 'g':
                operator_list.pop(i)
                operator_list.pop(i)
                operator_list.pop(i)
                number_list.pop(i)
                number_list.pop(i)
                number_list.pop(i)
                number_list[i] = Decimal(str(math.log(float(number_list[i]))))
            else:
                print("Invalid input: please type like log3+-5*exp(4.2)/(5+7) or log(3)+(-5)*exp(4.2)/(5+7)")
                quit()
            i -= 1
        elif operator_list[i] == 'e':
            if operator_list.__len__() > i + 2 and operator_list[i+1] == 'x' and operator_list[i+2] == 'p':
                operator_list.pop(i)
                operator_list.pop(i)
                operator_list.pop(i)
                number_list.pop(i)
                number_list.pop(i)
                number_list.pop(i)
                number = number_list[i]
                if operator_list.__len__() > i and operator_list[i] == '-' and number == '':
                    operator_list.pop(i)
                    number = '-' + number_list[i + 1]
                    number_list.pop(i)
                number_list[i] = Decimal(str(math.exp(float(number))))
            else:
                print("Invalid input: please type like log3+-5*exp(4.2)/(5+7) or log(3)+(-5)*exp(4.2)/(5+7)")
                break
            i -= 1
        elif operator_list[i] == 'o' or operator_list[i] == 'g' or operator_list[i] == 'x' or operator_list[i] == 'p':
            print("Invalid input: please type like log3+-5*exp(4.2)/(5+7) or log(3)+(-5)*exp(4.2)/(5+7)")
            quit()
        i += 1


# do power calculation
def power(number_list, operator_list):
    i = 0
    while i < operator_list.__len__():
        if operator_list[i] == '^':
            number1 = number_list[i]
            number2 = number_list[i + 1]
            if operator_list.__len__() > i+1 and operator_list[i + 1] == '-' and number2 == '':
                operator_list.pop(i + 1)
                number2 = '-' + number_list[i + 2]
                number_list.pop(i + 1)
            result = Decimal(number1) ** Decimal(number2)
            operator_list.pop(i)
            number_list.pop(i)
            number_list.pop(i)
            number_list.insert(i, result)
            i -= 1
        i += 1


# do multiply and division calculation
def mul_div(number_list, operator_list):
    i = 0
    while i < operator_list.__len__():
        if operator_list[i] == '*' or operator_list[i] == '/':
            number1 = number_list[i]
            number2 = number_list[i + 1]
            if operator_list.__len__() > i+1 and operator_list[i + 1] == '-' and number2 == '':
                operator_list.pop(i + 1)
                number2 = '-' + number_list[i + 2]
                number_list.pop(i + 1)
            if operator_list[i] == '*':
                result = Decimal(number1) * Decimal(number2)
            elif operator_list[i] == '/':
                result = Decimal(number1) / Decimal(number2)
            operator_list.pop(i)
            number_list.pop(i)
            number_list.pop(i)
            number_list.insert(i, result)
            i -= 1
        i += 1


# do addition and subtraction calculation
def add_sub(number_list, operator_list):
    i = 0
    while i < operator_list.__len__():
        if operator_list[i] == '+' or operator_list[i] == '-':
            number1 = number_list[i]
            number2 = number_list[i + 1]
            if operator_list.__len__() > i + 1 and operator_list[i + 1] == '-' and number2 == '':
                operator_list.pop(i + 1)
                number2 = '-' + number_list[i + 2]
                number_list.pop(i + 1)
            if operator_list[i] == '+':
                result = Decimal(number1) + Decimal(number2)
            elif operator_list[i] == '-':
                if number1 == "":
                    number1 = '0'
                result = Decimal(number1) - Decimal(number2)
            operator_list.pop(i)
            number_list.pop(i)
            number_list.pop(i)
            number_list.insert(i, result)
            i -= 1
        i += 1


# check if is operator
def is_operator(op):
    return op in OPERATORS


# remove whitespace in a string
def remove_whitespace(sequence:str):
    return sequence.replace(" ","")


# user input and result output
if __name__ == '__main__':
    while True:
        sequence = input("Please enter a sequence that you want to compute: (q to end)")
        sequence = remove_whitespace((sequence))
        print(sequence)
        lst = list(sequence)
        if sequence == 'q':
            break
        elif is_valid(lst):
            result = calc(lst)
            stack.clear()
            print("The result for", sequence, "is", "%.3f" % float(result))
        else:
            print("Error:The sequence must only include operators and digits")
