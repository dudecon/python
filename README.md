# python
A bunch of miscellaneous Python code. Mostly stand-alone scripts

# Miscellaneous Python Utility Programs

This repository contains a collection of miscellaneous Python utility programs that can be handy for various tasks. Each program is designed to solve a specific problem or provide a specific functionality, making it easier for you to accomplish common tasks in your Python projects, or do simple tasks with stand-alone scripts.

## Table of Contents

- [Getting Started](#getting-started)
- [Programs](#programs)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

To get started with these utility programs, you'll need to have Python installed on your machine. You can download the latest version of Python from the official Python website: [python.org](https://www.python.org/)

Once you have Python installed, you can clone this repository to your local machine using the following command:

```bash
git clone https://github.com/dudecon/python.git
```

After cloning the repository, you can navigate to the program's directory and run it using the Python interpreter. For example:

```bash
cd python
python program_name.py
```

Replace `program_name.py` with the actual name of the program you want to run.

## Programs

Here's a list of the utility programs included in this repository:

### Ancestor Pedigree Processing
See this [YouTube video for more details](https://youtube.com/live/JZTbO9isvXI).
- **Ancestor_Compiler_WikiPedia.py**: Grabs ancestor data from WikiPedia in a semi-automated fashion.
- **Pedigree_Paul Daniel Spooner.txt**: My pedigree.
- **Pedigree_Vladimir the Great.txt**: The rather limited available pedigree of Saint Vladimir the Great.
- **Ancestor_Visualizer - Paul.blend**: A Blender file that visualizes my ancestors.
- **Ancestor_Visualizer.blend**: A Blender file template for visualizing ancestors.

### Text Processing
- **Acronymizer.py**: Converts text to an acronym.
- **NatoPhoneticAlphabetConvertor.py**: Emits the NATO phonetic alphabet representation of a text input.
- **AwStatEdit.py**: For reducing the size of the AwStats log files.
- **FeetConvertor.py**: Take a string and convert it into Feet. This is like 1337, only instead of changing it to numbers, you change the first letter of all words into the letter "f".
- **OddTextGen.py**: Prints out an endless stream of rather odd looking text.
- **Oddifier.py**: Converts input text to rather odd looking text using unicode character substitution.
- **TextOddifier.py**: Same as Oddifier, but adds diacritics as well.

### HTML Processing and Generation
- **HTML Text Cleaner.py**: Cleans up HTML files and attempts to strip them down to only barebones text.
- **ffts_ps_cleanup.py**: Cleans up HTML, focused on stripping out extraneous formatting from Microsoft Word HTML exports.
- **GVK_Source_cleanup.py**: Does some text replacement on an obscure GVK file. Easy to repurpose for general text replacement.
- **PeripheralArborPageGen.py**: Generates HTML for my website image gallery.
- **txt_to_html.py**: Converts plain text to minimally formatted HTML.

### Number Processing (maths)
- **BaseConverter_py.py**: Converts numbers between arbitrary radix and conventional base 10.
- **InfiniteMaths.py**: Prints out an endless stream of maths problems.
- **semiprimesum_ps.py**: Calculates semiprime sums. Works best with a set of [pre-calculated primes](https://github.com/dudecon/PyPrimes).
- **WedgeShapes.py**: Calculate all the unique configurations of "waffle wedge" circle quadrant shapes. [Blender file of the output available here](https://github.com/dudecon/Blender-Scripts/blob/main/Wedge%20Configurations.blend). [Image available here](https://blenderartists.org/t/paul-spooner-sketchbook/1136797/27?u=dudecon).

### Blender Processing 
See my [Blender-Scripts repository](https://github.com/dudecon/Blender-Scripts) for more of this kind of stuff.
- **Blender EXP Export.py**: An exporter from Blender to the EXP embroidery file format.
- **Blender EXP Import.py**: Same as above, but imports.
- **Diecast_Setup.py**: Video blog setup Blender script. [How to use video](https://youtu.be/xo_9FG6gEZU). [Blender file](https://github.com/dudecon/Blender-Scripts/raw/main/Diecast%20Edit.blend).

### Image Processing
- **ImageFormatConverter.py**: Converts all the .png files in a directory into .jpg files.
- **ImageQuadrantBreak.py**: Splits every image in the directory into four quadrant images of equal size.

### Random Content Selection and Generation
- **Grimm Fairy Tale Choose.py**: Chooses one of Grimms Fairy Tales at random. Great for bedtime stories.
- **FantasyGenesis_Default.py**: An implementation of the Fantasy Genesis book by Chuck Lukacs.
- **FantasyGenesis_Deep.py**: Same as above, but I've added more depth and details to the options tree.
- **InfiniteMaths.py**: Prints out an endless stream of maths problems.
- **InfiniteMathsGPT.py**: Same as above, but rewritten by ChatGPT.
- **rand_mcm.py**: Brings up a random page from the McMaster Carr online catalog.
- **mcm_page.py**: Same as above, but also allows logging so you can draw from a specific set of pages, or work through the whole catalog over a long time period.
- **rand_name.py**: Generates a random name from a list of phonemes. Results in vaguely fantasy names.
- **OddTextGen.py**: Prints out an endless stream of rather odd looking text.
- **Pick_a_thing.py**: Randomly pick an item from a list.
- **rand_chr.py**: Open the UTF info page for a random UTF-8 character.
- **Rand_HeroForge.py**: Open the page for a random HeroForge character.
- **Rand_Wiki.py**: Opens a random featured Wikipedia page.
- **Rand_Wiki_Text.py**: Prints out an endless stream of text from random featured Wikipedia pages.
- **wiki_pages.txt**: The save file that caches featured wikipedia pages. Generated if not present.
- **ShamusHeadlineGen.py**: Headline generator based on DOGHOUSEDIARIES and Shamus Young.

### Misc IDK
- **Descriptor.py**: An experimental implementation of sentence structure and description generation.
- **Dorfromantik Helper.py**: Dorfromantik spot finder and logger thing. [How to use video](https://youtube.com/live/2UYUu4IP974)
- **NC Engrave Optimize.py**: Optimizes a G-Code .nc file designed for engraving.
- **NC Outline Optimize.py**: Optimizes a G-Code .nc file designed for drawing outlines.
- **Once Upon A Time.py**: A program which is also a short story.
- **Once Upon A Time_functional.py**: The above short story program stripped down to only the functional code.
- **Renamer.py**: Rename and move files and directories.
- **Wood Round Label Exporter.py**: Exports text files for a laser engraver control program.
- **glyphguesser.py**: A small guessing game.
- **glyphguesser Py2.7.py**: The above game, but in Python 2.7.
- **linkcull.py**: Recursively delete windows shortcuts associated with the "Harry potter" virus.
- **serializeTime.py**: Some time serialization code.
- **sounds.py**: Python 2 sound generation.

## Contributing

Contributions to this repository are welcome! If you have a utility program that you think would be a valuable addition to this collection, follow these steps:

1. Fork the repository.
2. Create a new branch for your feature: `git checkout -b new-feature`
3. Add your utility program to the repository.
4. Commit your changes: `git commit -m 'Add new feature'`
5. Push to the branch: `git push origin new-feature`
6. Submit a pull request.

Please ensure that your code follows the repository's (nearly non-existent) coding conventions and includes appropriate documentation.

## License

This repository is licensed as Public Domain. You are free to use, modify, and distribute the utility programs in this repository for both personal and commercial purposes.
