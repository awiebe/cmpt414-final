from PIL import Image
import sys

import pyocr
import pyocr.builders

tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
# The tools are returned in the recommended order of usage
tool = tools[0]
print("Will use tool '%s'" % (tool.get_name()))

line_and_word_boxes = tool.image_to_string(
    Image.open('synthesizedreceipt.jpg'), lang="eng",
    builder=pyocr.builders.LineBoxBuilder()
)
for line in line_and_word_boxes:
    print line.content
    print line.position[0][0]
