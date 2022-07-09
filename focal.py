# Imports
import re
import sys
from tracemalloc import start
lines = []
variables = [("ab", "hey there"), ("bc", "hello"), ("c", "hi"), ("d", "how are you?")]
lists  = [("example_list", ["value1", "value2"])]
line = 0


functions = [("examplefunction", ["line1", "line2", "line3"])]


is_Passing_Condition = True
is_Declaring_Function = False


def error(message):
    print("        \033[1m\033[91m   Focal Error  \033[0m        ")
    print("At \033[1m\033[92mline "+str(line)+"\033[0m ↓")
    print('\033[1m'+str(message)+'\033[0m')
    exit()


def get_var_value(name):
    try:
        return variables[[x for x, y in enumerate(variables) if y[0] == name][0]][1]
    except:
        return name


def get_var_name(value):
    try:
        return variables[[x for x, y in enumerate(variables) if y[1] == value][0]][0]
    except:
        return value


def process_content(value):
    # Checking if the variable value corresponds to a variable name. If it does, it will use the
    # corresponding variable's value as the declared variable's value.
    try:
        value = [x.replace(x, process_property(x.split(".")[0], x.split(".")[1])) for x in re.findall(r'[^ ]*\.[^ ]*', value) if not " " in x][0]
    except:
        pass
    try:
        if any([value in tup for tup in variables]):
            value = get_var_value(value)
    except:
        pass
    # Checking if there is a plus sign in the variable value. If there is, it will split the
    # variable value by the plus sign and then replace each variable name with its value. Then it
    # will try to evaluate the expression. If it can't, it will just concatenate the values.
    try:
        value = eval(value)
    except:
        if "+" in value:
            for var in value.split("+"):
                var = var.lstrip().rstrip()
                print(var)
                try:
                    value = value.replace(var, eval(var))
                except:
                    value = value.replace(var, str(get_var_value(var)))
            try:
                value = eval(value)
            except:
                final_val = ""
                for elem in value.split("+"):
                    final_val = final_val + str(elem)
                value = final_val
    return value


def process_property(obj, property):
    if "uppercase" == property:
        return obj.upper()
    elif "lowercase" == property:
        return obj.lower()
    elif "isnumbers" == property:
        return str(any(char.isdigit() for char in obj))
    elif "isletters" == property:
        return str(any(char.isalpha() for char in obj))
    elif "capitalize" == property:
        return obj.capitalize()
    elif "isuppercase" == property:
        return str(obj.isupper())
    elif "islowercase" == property:
        return str(obj.islower())
    elif "leftstrip" == property:
        return obj.lstrip()
    elif "rightstrip" == property:
        return obj.rstrip()
    elif "title" == property:
        return obj.title()
    elif "replace" == property[0]+property[1]+property[2]+property[3]+property[4]+property[5]+property[6]:
        property = property.replace("replace","").replace("[","").replace("]","").split("->")
        return obj.replace(property[0].rstrip(), replaced = property[1].lstrip())
    else:
        return obj+"."+property


def execute(lines):
    global is_Passing_Condition
    global is_Declaring_Function
    global line
    for input in [s.lstrip().rstrip() for s in lines]:
        
        line += 1
        """
        Declaring variables

        To-do:
        - Variable concatenation with evaluated argument
        """
        if input:
            if is_Declaring_Function == False or "}" == input[0]:
                if is_Passing_Condition == True or "}" == input[0]:
                    if "declare" in input.split(" ")[0]:
                        try:
                            assert "=" in input.split(" ")[2]
                        except:
                            error("Invalid syntax when declaring variable (missing '=')")
                        # Getting the variable name and value from the input.
                        input = input.replace("declare", "").lstrip()
                        temp_var_name = input.split(" ")[0]
                        temp_var_value = input.replace(input.split(" ")[0], "").replace("=","", 1).lstrip()
                        # Checking if the variable name already exists. If it does, it will overwrite the value.
                        if any([temp_var_name in tup for tup in variables]):
                            variables[[x for x, y in enumerate(variables) if y[0] == temp_var_name][0]] = (temp_var_name, temp_var_value)
                        else:
                            variables.append((temp_var_name, process_content(temp_var_value)))
                    elif "print" in input.split(" ")[0]:
                        try:
                            assert "->" in input.split(" ")[1]
                        except:
                            error("Invalid syntax when printing")
                        print(process_content(input.split("->")[1].lstrip()))
                    elif "debug" in input.split(" ")[0]:
                        try:
                            assert "->" in input.split(" ")[1]
                        except:
                            error("Invalid syntax when printing")
                        print("\33[31m[DEBUG] "+str(process_content(input.split("->")[1].lstrip()))+"\33[0m")
                    # Closing brackets
                    # To-Do: - Recognize wether the closing bracket closes a function declaration or a condition
                    elif "}" == input[0]:
                        if is_Declaring_Function == True:
                            is_Declaring_Function = False
                        else:
                            is_Passing_Condition = True
                    # Conditions
                    # To-do: - Execute (or not if the condition is false) the next conditional lines
                    elif "if" == input.split(" ")[0]:
                        try:
                            assert "(" in input and ")" in input and "{" in input
                        except:
                            error("Invalid conditional statement")
                        if not "!=" in input:
                            # Getting the condition and the code to execute if the condition is true.
                            args = input.replace("if","").replace("(","").replace(")","").replace("{","").lstrip().rstrip().split("=")
                            if str(process_content(args[0].lstrip().rstrip())) == str(process_content(args[1].lstrip().rstrip())):
                                is_Passing_Condition = True
                            else:
                                is_Passing_Condition = False
                        else:
                            # Getting the condition and the code to execute if the condition is true.
                            args = input.replace("if","").replace("(","").replace(")","").replace("{","").lstrip().rstrip().split("!=")
                            if str(process_content(args[0].lstrip().rstrip())) != str(process_content(args[1].lstrip().rstrip())):
                                is_Passing_Condition = True
                            else:
                                is_Passing_Condition = False
                    elif "function" == input.split(" ")[0]:
                        try:
                            assert "(" in input and ")" in input and "{" in input
                        except:
                            error("Invalid syntax when declaring function")
                        function_name = input.replace("function", "").replace("(", " ").replace(")","").replace("{","").lstrip().rstrip().split(" ")[0]
                        is_Declaring_Function = True


def record_exec_time():
    import time
    start_time = time.time_ns() / (10 ** 9)
    execute(["declare a = Hey there", "print -> a","if (a = Hey there) {","print -> 5*7/7*10*67.65*7/7*10*67.6*7/7*10*67.6","}","declare b = testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttest", "print -> b"])
    print("--- %s seconds ---" % (time.time_ns() / (10 ** 9) - start_time))


if len(sys.argv) > 1:
    if sys.argv[1] == "--test":
        record_exec_time()
    else:
        file = open(sys.argv[1], 'r')
        execute(file.readlines())
else:
    print("Focal ALPHA")
    while True:
        execute(input(">> ").split("||"))
