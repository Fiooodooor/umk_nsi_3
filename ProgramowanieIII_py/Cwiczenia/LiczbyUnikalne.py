
def get_unique_numbers(numbers: str):
    unique_numbers = []

    if isinstance(numbers, str):
        numbers = numbers.split(' ')

    while numbers:
        single = numbers.pop()
        if single in numbers:
            while single in numbers:
                numbers.remove(single)
        elif single.isdecimal():
            unique_numbers.append(int(single))
    return unique_numbers


if __name__ == "__main__":
    inputText = input("Type list of integer numbers: ")
    uniqueNumbers = get_unique_numbers(inputText)
    print("Your unique numbers: ", uniqueNumbers)
