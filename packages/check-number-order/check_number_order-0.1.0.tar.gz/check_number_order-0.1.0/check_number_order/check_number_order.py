def check_number_order(number, increasing_string, decreasing_string):
    num_str = str(number)

    is_increasing = all(num_str[i] <= num_str[i + 1] for i in range(len(num_str) - 1))
    
    is_decreasing = all(num_str[i] >= num_str[i + 1] for i in range(len(num_str) - 1))
    
    if is_increasing or is_decreasing:
        return increasing_string
    else:
        return decreasing_string