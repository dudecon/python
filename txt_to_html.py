# Converts a plaintext file to an HTML file
# With approximately correct formatting

from collections import OrderedDict

filein = 'Bible_NAB_Clean.txt'
fileout = 'Bible_NAB_Clean.htm'

# open the file and read it into memory as "data"
f = open(filein, 'r', encoding="utf-8")
data = f.read()
f.close()


def tag_heading(text,level = 1):
    # return a string enclosed by <h1> tags
    new_string = f"<h{level}>" + text + f"</h{level}>\n\n"
    return new_string


def tag_paragraph(text):
    # return a string enclosed by <p> tags
    new_string = "<p>" + text + "</p>\n\n"
    return new_string


final_text = '<head><meta charset="UTF-8"></head><html>\n<body>\n'
while "\n\n\n\n" in data:
    data = data.replace("\n\n\n\n","\n\n\n")

# Break into sections
sections = data.split("\n\n\n")
for section in sections:
    # make the first line of each section a title
    title_end = section.find('\n')
    title_text = section[:title_end].strip()
    title_text = tag_heading(title_text,2)
    final_text += title_text
    section_body = section[title_end+1:]
    # break into paragraphs
    paragraphs = section_body.split("\n\n")
    for paragraph in paragraphs:
        # enclose each paragraph in <p> tags
        paragraph_text = ""
        paragraph = paragraph.strip()
        lines = paragraph.split("\n")
        for line in lines:
            line = line.strip()
            if line[:7] == "CHAPTER" or line[:5] == "PSALM":
                paragraph_text += tag_heading(line, 3) + "\n"
            else:
                paragraph_text += line + "<br>\n"
        paragraph_text = tag_paragraph(paragraph_text)
        final_text += paragraph_text


final_text += "</body>\n</html>\n"

# save the file out
f = open(fileout, 'w', encoding="utf-8")
f.write(final_text)
f.close()

print("done!")
