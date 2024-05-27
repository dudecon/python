from os import rename, listdir
from PIL import Image

dir_path = path.dirname(path.realpath(__file__))
chdir(dir_path)
thesefiles = listdir()
# thesefiles = ("Shrouded Brilliance.01.jpg",)
targets = (".png",".jpg")
newformat = ".jpg"
newdir = "./Originals/"
tlen = 4

def save_quadrants(image_path, output_directory):
    # Open the image
    image = Image.open(image_path)

    if newformat == ".jpg":
        # Check if the image has an alpha channel (transparency)
        has_alpha = image.mode.endswith('A')

        # If the image has an alpha channel, convert it to RGB
        if has_alpha:
            image = image.convert('RGB')
    elif newformat == ".png":
        # No alteration needed
        pass

    # Get the size of the image
    width, height = image.size

    # Calculate the width and height of each quadrant
    quadrant_width = width // 2
    quadrant_height = height // 2

    # Iterate over the quadrants
    for i in range(2):
        for j in range(2):
            # Calculate the coordinates of the current quadrant
            left = j * quadrant_width
            top = i * quadrant_height
            right = (j + 1) * quadrant_width
            bottom = (i + 1) * quadrant_height

            # Crop the image to extract the quadrant
            quadrant = image.crop((left, top, right, bottom))

            # Save the quadrant as a separate file
            output_path = f"{output_directory}/{image_path}_{i}{j}{newformat}"
            quadrant.save(output_path)
            # print(f"Quadrant {i}{j} saved as {output_path}")

for f in thesefiles:
    if f[-tlen:] in targets:
        save_quadrants(f, "./")
        m = newdir + f
        rename(f, m)
        print("processed", f)

