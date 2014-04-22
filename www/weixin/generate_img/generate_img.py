# -*- coding:UTF-8 -*-
#!/usr/bin/python

from PIL import Image,ImageDraw
import re
import pycurl
import os
import logging

class generate_image():
    '''
    generate image for news
    '''
    __tmp_dir = '/tmp/tmp_douban_image/'
    __img_dir = os.path.dirname(os.path.dirname(__file__)) + '/static/douban_image/'
    # default image
    __img_name = '0000000.jpg'
    
    def __init__(self,cover_url,canvas_size = (360,200),cover_new_size = None):
        self.__canvas_size = canvas_size
        self.__cover_new_size = cover_new_size
        self.__cover_url = cover_url
        
        __regExp = re.compile(r's(\d+\.\w+)')
        __search_result = __regExp.search(cover_url)
        self.__img_name = __search_result.group(1)            
        
    def __save_original_image(self):
        '''
        save original image for news
        '''
        if not os.path.isdir(self.__tmp_dir):
            os.mkdir(self.__tmp_dir)
        
        __image = self.__tmp_dir + self.__img_name
        __image_file = file(__image,'wb')
        
        try:
            __curl = pycurl.Curl()
            __curl.setopt(__curl.URL, self.__cover_url)
            __curl.setopt(__curl.WRITEFUNCTION, __image_file.write)
            __curl.setopt(__curl.HEADER, False)
            __curl.perform()
            __image_file.close()
            __curl.close()
            logging.debug('GET COVER URL:%s' % self.__cover_url)
        except BaseException as e:
            logging.error('GET COVER URL ERROR:%s' % self.__cover_url)
            logging.exception(traceback.format_exc())
 
        return __image
    
    def __generate_image(self):
        '''
        generate image for news
        '''
        __original_image = self.__save_original_image()
       
        __im_cover = Image.open(__original_image)
        __cover_size = __im_cover.size

        if not self.__cover_new_size:
             self.__cover_new_size = (int((float(__cover_size[0]) / float(__cover_size[1])) * (self.__canvas_size[1] - 2)),self.__canvas_size[1] - 2)

        # thumbnail
        #__im_cover.thumbnail(self.__cover_new_size,Image.ANTIALIAS)
        # resize
        __im_cover = __im_cover.resize(self.__cover_new_size,Image.ANTIALIAS )
        # canvas
        color_list = [(255,255,255),(255,255,204),(204,255,204),(102,102,102),(204,202,102),(204,102,255),(204,204,153)]
        color_list.__len__()
        from random import random
        
        i = int(random() * 10) % 7
        
        __im_canvas = Image.new('RGB',self.__canvas_size,color_list[i])
        
        __left_distance = (self.__canvas_size[0] - self.__cover_new_size[0])/2
        __im_canvas.paste(__im_cover,(__left_distance,1))
        
        __image = self.__img_dir + self.__img_name
        
        __im_canvas.save(__image)
        
        # delete temp image fille
        __tmp_image = self.__tmp_dir + self.__img_name
        os.remove(__tmp_image)
        
        return self.__img_name if os.path.exists(__image) else r'0000000.jpg'
            
    def get_image_url(self):
        '''
        generate image for news,return an image url if success
        '''
        __image = self.__generate_image()
        
        __img_url = r'http://115.28.3.240/weixin/cover_for_news/' + self.__img_name
        
        return __img_url
        
if __name__ == '__main__':
    ge = generate_image(cover_url='http://img5.douban.com/lpic/s2785398.jpg')
    giu = ge.get_image_url()
    print giu