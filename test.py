def return_target_num(string):
    for char in string:
        num_str = ''.join(filter(str.isdigit, char))
        if num_str:
            return int(num_str)
        
print(return_target_num('TA1'))
print(return_target_num('TAB2'))