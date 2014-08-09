# Jamie Harvey - 13105960
# 159.172 Practical Test

# Problem Set 1

# Q1

# variable list was renamed to list_of_strings to avoid confict with builtins
def join_list(list_of_strings):
    return "".join(list_of_strings)

list_of_strings = ["learn ", "computer ", "science,", "at ", "Massey "]
print join_list(list_of_strings)

# Q2

def get_user_choice():
    while true:
        command = raw_input("Command: ")
        valid_commands = ["f", "m", "s", "d", "q"]
        if command in valid_commands:
            return command
        print "Hey, that's not a command. Here are your options:"
        print "f - Full speed ahead"
        print "m - Moderate speed"
        print "s - Status"
        print "d - Drink"
        print "q - Quit"

user_command = get_user_choice()
print "You entered:", user_command

