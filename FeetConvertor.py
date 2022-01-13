# Feet translator
# Take a string and convert it into Feet
# This is like 1337, only instead of changing it to numbers
# You change the first letter of all words into the letter "f"

# Code by Paul Spooner
# Released to the public domain

def feet(s):
    old_words = s.split()
    new_words = []
    for word in old_words:
        first = word[0]
        
        if first.lower() != first:
            CapFirst = "F"
        else: CapFirst = "f"

        if len(word) <= 2: offset = 0
        else: offset = 1
            
        new_words += [CapFirst + word[offset:]]
    new_string = " ".join(new_words)
    # print(new_string)
    return new_string
    
print(feet(input("enter the mangle string")))
