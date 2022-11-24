from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


import os

font = os.path.join('c:/Windows/Fonts', 'arial.ttf')

arialFont = ImageFont.truetype(font, 128)

base_img = Image.open('color_cube.jpg')
bw, bh = base_img.size
print(bw, bh)

for y in range(3):
    for x in range(3):
        cx = x * 800 + 100
        cy = (2-y) * 600 + 100
        timage = base_img.crop((cx, cy, cx+800, cy+600))
        draw = ImageDraw.Draw(timage)
        draw.text((200, 200), '(%d, %d)' % (x, y), font=arialFont)
        timage.save('cube%d%d.png' % (x, y))

        print(x,y,cx,cy)



# base_img.show()
