import os
import re

"""
Idempotent Metaprogramming build file for static photojournal site :D

Why not go dynamic? I love github pages too much
"""

def delete_photogrid_content(file_path):
    # Read the file content
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Join lines into a single string to use regular expressions
    file_content = ''.join(lines)

    # Define a regex pattern to match the content inside the #photo-grid div
    # The pattern matches everything between <!-- Photogrid --> and </div> <!-- Photogrid -->
    pattern = r'<!-- Photogrid -->\s*(<div id="photo-grid"[^>]*>).*?(</div> <!-- Photogrid -->)'

    # Replace the content inside the photo-grid div with just the div and the comments
    modified_content = re.sub(pattern, r'<!-- Photogrid -->\n\1\n</div>\n<!-- Photogrid -->', file_content, flags=re.DOTALL)

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.write(modified_content)

def buildImageList():
    # Directory containing your images
    images_dir = './static/images/photojournal'
    # Get a list of image files
    image_files = [f for f in os.listdir(images_dir) if f.endswith(('.jpeg', '.jpg', '.JPG', '.png', '.gif'))]

    # Generate a JavaScript array from the list of image files
    with open('./static/javascript/image_list.js', 'w') as js_file:
        js_file.write('const imageFiles = [\n')
        for image in image_files:
            js_file.write(f"    '{image}',\n")
        js_file.write('];\n')
        js_file.write('export default imageFiles;')

def main():
    print("Begin build photojournal image_list.js...")
    buildImageList()
    delete_photogrid_content('test.html')

if __name__ == "__main__":
    main()