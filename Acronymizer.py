# Acronymizer
def acronymize(input_string):
    output_string = ""
    words = input_string.split()
    for word in words:
        output_string += word[0]
    return output_string.upper()
