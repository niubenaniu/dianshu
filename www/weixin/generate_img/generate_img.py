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
    
    def __init__(self,cover_url,canvas_size = (200,133),cover_thumbnail_size = (100,133)):
        self.__canvas_size = canvas_size
        self.__cover_thumbnail_size = cover_thumbnail_size
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
        # thumbnail
        __im_cover.thumbnail(self.__cover_thumbnail_size,Image.ANTIALIAS)
        # canvas
        __im_canvas = Image.new('RGBA',self.__canvas_size,'red')
        
        __cover_size = __im_cover.size
        
        __left_distance = (self.__canvas_size[0] - __cover_size[0])/2
        __im_canvas.paste(__im_cover,(__left_distance,10))
        
        __image = self.__img_dir + self.__img_name
        
        __im_canvas.save(__image)
        
        return self.__img_name if os.path.exists(__image) else r'0000000.jpg'
            
    def get_image_url(self):
        '''
        generate image for news,return an image url if success
        '''
        __image = self.__generate_image()
        
        __img_url = r'http://115.28.3.240/weixin/cover_for_news/' + self.__img_name
        
        return __img_url
        
        