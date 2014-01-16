# -*- coding:UTF-8 -*-
#!/usr/bin/python

from PIL import Image,ImageDraw #,ImageFont

size = 200,198

im_book = Image.open('test.jpg')
im_book.thumbnail(size,Image.ANTIALIAS)

im_new = Image.new('RGBA',(360,200),'white')
book_size = im_book.size
left = (360 - book_size[0])/2 
im_new.paste(im_book,(left,1))
# 中文字体弄不出来，只能把图片放到白色背景中间了，干干干！
#draw = ImageDraw.Draw(im_new)
#font = ImageFont.truetype('arial.ttf',24)
#string = u'百年孤独'
#draw.text((165,5),string,fill='green',font=font)
im_new.save('xxx.jpg')

