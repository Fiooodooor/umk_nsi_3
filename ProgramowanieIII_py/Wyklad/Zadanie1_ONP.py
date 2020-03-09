def print_error_msg(error_str: str):
    print("Error! " + error_str)
    return []


def load_expressions_from_file(temp_file_input: str) -> []:
    onp_equation_list = []
    try:
        with open(temp_file_input) as onp_data_file:
            number_of_lines = onp_data_file.readline().rstrip()
            if number_of_lines.isdecimal():
                for it in range(0, int(number_of_lines)):
                    onp_equation_list.append(onp_data_file.readline().rstrip().split(" "))
            else:
                return onp_equation_list
    except FileNotFoundError:
        print_error_msg("load_zadanie_1_onp method. File not found!")
        exit(1)
    except Exception as e:
        print_error_msg("load_zadanie_1_onp method. Error " + str(e))
        exit(2)
    return onp_equation_list


def save_experssions_to_file(temp_file_output: str, expressions_results: []) -> bool:
    try:
        with open(temp_file_output, 'w') as onp_data_file:
            for it in expressions_results:
                onp_data_file.write(str(it) + '\n')
    except IOError:
        print_error_msg("save_experssions_to_file method. File input/output error")
        return False
    return True


def calculate_all_expressions(expressions_list: []) -> []:
    expressions_results = []
    for it in expressions_list:
        expressions_results.append(calculate_single_expression(it))
    return expressions_results


def calculate_single_expression(expression: []) -> float:
    stack = []              # pop() and append() methods makes every list a stack.
    expression.reverse()    # reversing the list makes it an queue-like
    try:
        while expression:
            it = expression.pop()
            if it in ['*', '/', '+', '-']:
                first_value = stack.pop()
                second_value = stack.pop()
                if it == '*':
                    stack.append(second_value * first_value)
                elif it == '/':
                    try:
                        stack.append(second_value / first_value)
                    except ZeroDivisionError:
                        print_error_msg("Division by 0 error " + str(second_value) + " " + str(it) + " " + str(first_value))
                elif it == '+':
                    stack.append(second_value + first_value)
                elif it == '-':
                    stack.append(second_value - first_value)
            else:
                if it.isnumeric():
                    stack.append(float(it))
                else:
                    try:
                        stack.append(float(it))
                    except ValueError:
                        print_error_msg("Conversion error, unknown value/type " + it)
    except IndexError:
        print_error_msg("calculate_single_expression error. Given expression caused Pop() on empty stack was called.")
        return 0
    return stack.pop()


def zadanie_1_onp(file_in: str, file_out: str) -> bool:
    final_result = calculate_all_expressions(load_expressions_from_file(file_in))
    return save_experssions_to_file(file_out, final_result)


if __name__ == "__main__":
    if zadanie_1_onp("onp.txt", "wynik_onp.txt"):
        print("Pomyslnie wykonano")
    else:
        print("Nie wszystko poszlo po naszej mysli")
    exit(0)