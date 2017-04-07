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

#TODO --load_system_dawg =0  #Disables dictionary matching

img = Image.open(sys.argv[1])

#Using english
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
    if abs(t.position[0][1] -curY) < errorMargin:
        curLine = curLine+" "+t.content
    else:
        lines.append( (curY,curLine))
        curY=t.position[0][1]
        curLine=t.content

for l in lines:
    print l
    priceRegex= r'[$]*[ ]*([0-9]*)[\.]*([0-9]*)'
    itemLineRegex =r'([A-z ]*)[ ]* ([0-9]*)[ ]*[$]*[ ]*([0-9]*)[\.]*([0-9]*)'
    unitLineRegex =r'([0-9]+)([lbgkgLmL]+) @ ([0-9]*)[\.]*([0-9]*)/[lbgkgLmL]* [$]*[ ]*([0-9]*)[\.]*([0-9]*)'
    
    #Tesserect can't distinguish between 1 and L very well. so sanitize the pounds unit
    tesseractSantized = l[1].replace("1b","lb")

    searchUnit = re.search( unitLineRegex,tesseractSantized , re.M|re.I)
    searchItem = re.search( itemLineRegex, tesseractSantized, re.M|re.I)
    if searchUnit:
        
        print "searchObj.group():", searchItem.group()
        print "Unit quantity:", searchItem.group(1)
        print "Units:", searchItem.group(2)
        print "Unit Dollars: ", searchItem.group(2)
        print "Unit Cents : ", searchItem.group(3)
        print "Total Dollars: ", searchItem.group(4)
        #print "Total Cents : ", searchItem.group(5)
    elif searchItem:
        print "searchObj.group():", searchItem.group()
        print "Item label:", searchItem.group(1)
        print "SKU (optional):", searchItem.group(2)
        print "Dollars: ", searchItem.group(3)
        print "Cents : ", searchItem.group(4)
    else:
        print "Nothing found!!"

    