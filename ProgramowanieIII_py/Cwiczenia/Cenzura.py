def cenzuruj(input_text: str, unwanted_words: [], replacement_sign: str):
    result_text = []
    # If string or unwanted words are empty, just return the input
    if not unwanted_words or not input_text:
        return input_text

    # Want to be case insensitive, so lower case all unwanted words
    for it in range(0, len(unwanted_words)):
        unwanted_words[it] = (unwanted_words[it].lower())

    # Making sure to use only single sign or empty character
    if len(replacement_sign) > 1:
        replacement_sign = replacement_sign[0]

    # It is easy to operate on single words so split the input
    input_text = input_text.split(" ")

    # End for every word from split input do
    for word in input_text:
        if word.lower() in unwanted_words:
            replace_word = ""
            for it in range(0, len(word)):
                replace_word += replacement_sign
            word = replace_word
        result_text.append(word)
    return ' '.join(result_text)


if __name__ == "__main__":
    text = 'Dzisiaj jest brzydka pogoda i pada deszcz'
    words = ["dzisiaj", "Pada"]
    sign = "-"
    print(text)
    print(cenzuruj(text, words, sign))
    exit(0)
