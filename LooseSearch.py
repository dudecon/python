# Search all the text files, loosely, with a scored search

from os import listdir, path, chdir
from collections import defaultdict

PRINT_MARGIN = 20
THRESHOLD = 14
REPEAT_PENALTY = 0.5
SECTION_LIMIT = 7

words_to_find = {"twelve": 12, "three": 3, "gate": 6, "city": 3, "hand": 4}
target_extension = ".txt"

dir_path = path.dirname(path.realpath(__file__))
chdir(dir_path)
all_files = listdir()

def calculate_word_score(raw_word, search_words, partial_penalty=1.618):
    '''return the float value for the word score'''
    word_text = raw_word.lower()
    for char in ('"', '"', ',', '.', '!', '?', ';', ':', '“', '”'):
        word_text = word_text.replace(char, '')
    base_length = len(word_text)
    total_score = 0
    for word in search_words:
        word_score = 0
        if word in word_text:
            penalty = (len(word) / base_length) ** partial_penalty
            word_score = search_words[word] * penalty
        total_score += word_score
    return total_score


def find_relevant_sections(text, search_words, threshold=115, partial_penalty=1.618):
    '''returns a sorted list of all the text that scores above the threshold'''
    split_text = text.split()
    score = 0
    found = False
    start_index = 0
    sections = []
    word_count = defaultdict(int)

    for i, word in enumerate(split_text):
        # Calculate word score
        word_score = calculate_word_score(word, search_words, partial_penalty=partial_penalty)
        
        # Apply repeat penalty if the word has been seen before in the current section
        word_lower = word.lower().strip('"",.!?;:“”')
        if word_score > 0:
            word_count[word_lower] += 1
            if word_count[word_lower] > 1:
                word_score *= REPEAT_PENALTY ** (word_count[word_lower] - 1)
        
        # Add word score to current score
        score += word_score
        
        # Check if we are starting a new section
        if score > 0 and not found:
            start_index = max(0, i - int(THRESHOLD))  # Expand backward
            found = True
        
        # Ensure consistent score decay
        score = max(0, score - 1)
        if score == 0:
            if found:
                # Finalize the section if score drops to zero and check against the threshold
                end_index = i
                section_score = sum([calculate_word_score(split_text[j], search_words, partial_penalty=partial_penalty) for j in range(start_index, end_index)])
                if section_score >= threshold:
                    # Combine overlapping sections
                    if sections and sections[-1][2] >= start_index:
                        old_score, old_start, old_end, old_text = sections.pop()
                        start_index = min(start_index, old_start)
                        end_index = max(end_index, old_end)
                        section_score = max(section_score, old_score)
                    sections.append((section_score, start_index, end_index, text))
                word_count.clear()  # Clear word count when ending a section
                found = False

    # Check for any remaining open section
    if found:
        end_index = len(split_text)
        section_score = sum([calculate_word_score(split_text[j], search_words, partial_penalty=partial_penalty) for j in range(start_index, end_index)])
        if section_score >= threshold:
            # Combine overlapping sections
            if sections and sections[-1][2] >= start_index:
                old_score, old_start, old_end, old_text = sections.pop()
                start_index = min(start_index, old_start)
                end_index = max(end_index, old_end)
                section_score = max(section_score, old_score)
            sections.append((section_score, start_index, end_index, text))

    return sections

def process_files(all_files, words_to_find, threshold, section_limit, print_margin, target_extension):
    '''Accumulate all relevant sections from all files and print them'''
    all_found_sections = []

    for file_name in all_files:
        if file_name.endswith(target_extension):
            with open(file_name, encoding="utf-8") as file:
                contents = file.read()
            found_sections = find_relevant_sections(contents, words_to_find, threshold)
            if found_sections:
                all_found_sections.extend([(score, start, end, file_name, contents) for (score, start, end, contents) in found_sections])

    # Sort all found sections by score in descending order
    all_found_sections.sort(reverse=True, key=lambda x: x[0])

    # Print all found sections, limited to section_limit
    for section in all_found_sections[:section_limit]:
        score, start, end, file_name, contents = section
        title = contents.split(sep="\n")[0].strip()
        split_text = contents.split()
        begin = max(start - print_margin, 0)
        final_end = end + print_margin
        print(f"=== {title} ({file_name}) ===")
        print(f"\nScore: {score:.2f} | Range: ({begin}, {final_end})")
        print(' '.join(split_text[begin:final_end]))
        print('\n' + '='*40 + '\n')

if __name__ == '__main__':
    process_files(all_files, words_to_find, THRESHOLD, SECTION_LIMIT, PRINT_MARGIN, target_extension)
    input("Enter to Exit")
