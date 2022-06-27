import re, sys
lines = []
variables = [("a", "hey there"), ("b", "hello"), ("c", "hi"), ("d", "how are you?")]
lists  = [("example_list", ["value1", "value2"])]

if len(sys.argv) > 1:
    file = open(sys.argv[1], 'r')
    lines = file.readlines()
else:
    exit()
line = 0

is_Passing_Condition = True

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
    for obj in re.findall(r'[^ ]*\.[^ ]*', value):
        if not " " in obj:
            value = value.replace(obj, process_property(obj.split(".")[0], obj.split(".")[1]))
    try:
        if any([value in tup for tup in variables]):
            value = variables[[x for x, y in enumerate(variables) if y[0] == value][0]][1]
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
    else:
        return obj+"."+property


for input in lines:
    line += 1
    """
    Declaring variables

    To-do:
    - Variable concatenation with evaluated argument
    """
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
                temp_var_value = process_content(temp_var_value)
                variables.append((temp_var_name, temp_var_value))
        elif "print" in input.split(" ")[0]:
            try:
                assert "->" in input.split(" ")[1]
            except:
                error("Invalid syntax when printing")
            print_val = input.split("->")[1].lstrip()
            print(process_content(print_val))
        elif "}" == input[0]:
            global is_passing_condition
            is_Passing_Condition = True
        # Conditions
        # To-do: - Execute (or not if the condition is false) the next conditional lines
        elif "if" in input.split(" ")[0]:
            try:
                assert "(" in input and ")" in input and "{" in input
            except:
                error("Invalid conditional statement")
            # Getting the condition and the code to execute if the condition is true.
            args = []
            for arg in input.replace("if","").replace("(","").replace(")","").replace("{","").lstrip().rstrip().split("="):
                if arg:
                    args.append(process_content(arg.lstrip().rstrip()))
            if str(args[0]) == str(args[1]):
                is_passing_condition = False
            else:
                is_Passing_Condition = False