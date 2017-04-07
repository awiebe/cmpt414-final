from PIL import Image
import sys
import re

import pyocr
import pyocr.builders

tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
# The tools are returned in the recommended order of usage
tool = tools[0]
print("Will use tool '%s'" % (tool.get_name()))

img = Image.open(sys.argv[1])
line_and_word_boxes = tool.image_to_string(
    img, lang="eng",
    builder=pyocr.builders.LineBoxBuilder()
)

# for line in line_and_word_boxes:
#     print line.content
#     print line.position[0][0]

#Sort on the top right corner of the contenr
ysort = sorted(line_and_word_boxes, key=lambda l: l.position[0][1])


for l in ysort:
    print l.position[0][1] , l.content

if(len(ysort) ==0):
    print "No text found in image"

#Error margin in pixels
errorMargin=5
curY= ysort[0].position[0][1]
curLine=""
lines=[]

print "grouping"
for t in ysort:
    print "e=",abs(t.position[0][1] -curY)
    if abs(t.position[0][1] -curY) < errorMargin:
        curLine = curLine+" "+t.content
        print curLine
    else:
        print "\n"
        lines.append( (curY,curLine))
        curY=t.position[0][1]
        curLine=t.content

for l in lines:
    print l

    itemLineRegex =r'([A-z ]*)[ ]* ([0-9]*)[ ]*[$]*[ ]*([0-9]*)[\.]([0-9]*)'
    searchObj = re.search( itemLineRegex, l[1], re.M|re.I)

    if searchObj:
        print "searchObj.group():", searchObj.group()
        print "Item label:", searchObj.group(1)
        print "SKU (optional):", searchObj.group(2)
        print "Dollars: ", searchObj.group(3)
        print "Cents : ", searchObj.group(4)
    else:
        print "Nothing found!!"

    