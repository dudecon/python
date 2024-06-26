# Converts a plaintext file to an HTML file
# With approximately correct formatting

from collections import OrderedDict

filein = '[contact].txt'
fileout = '[contact].html'

# open the file and read it into memory as "data"
f = open(filein, 'r')
data = f.read()
f.close()


def tag_title(text):
    # return a string enclosed by <h1> tags
    new_string = "<h1>" + text + "</h1>\n\n"
    return new_string


def tag_paragraph(text):
    # return a string enclosed by <p> tags
    new_string = "<p>" + text + "</p>\n\n"
    return new_string


final_text = "This file generated by script.\n<html>\n<body>\n"
# Break into sections
sections = data.split("\n\n\n")
for section in sections:
    # make the first line of each section a title
    title_end = section.find('\n')
    title_text = section[:title_end].strip()
    title_text = tag_title(title_text)
    final_text += title_text
    section_body = section[title_end+1:]
    # break into paragraphs
    paragraphs = section_body.split("\n\n")
    for paragraph in paragraphs:
        # enclose each paragraph in <p> tags
        paragraph_text = tag_paragraph(paragraph.strip())
        final_text += paragraph_text


final_text += "</body>\n</html>"

# save the file out
f = open(fileout, 'w')
f.write(final_text)
f.close()

print("done!")
