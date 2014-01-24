# -*- coding:UTF-8 -*-

# createed by niuben at 2013-12-09
from django.shortcuts import render_to_response,render,RequestContext
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from xml.etree import ElementTree 
from time import time
import varify
import hashlib
import os

from api_douban.service import RequestService
from generate_img.generate_img import generate_image

@csrf_exempt
def auto_service(request):
    '''
    support the service for 'dianshu'
    '''
    # verify the signature
    if request.method == 'GET':
        token = 'dianshu_weinxin'
        varify_flag = varify.is_varified(request,token)
        return HttpResponse(varify_flag) if varify_flag else HttpResponse('signature verify failed!')
    else:
        # service
        reply_msg = auto_reply_service(request)

        return reply_msg
    
@csrf_exempt
def auto_reply_service(request):
    '''
     
    '''
    '''
    # used to received text message xml
    from_user_name_regexp = re.compile(r'<FromUserName><!\[CDATA\[(.+)\]\]></FromUserName>')
    message_type_regexp = re.compile(r'<MsgType><!\[CDATA\[(.+)\]\]></MsgType>')
    content_regexp = re.compile(r'<Content><!\[CDATA\[(.+)\]\]></Content>')
    
    message_str = ''
    print request._get_post
    if request.method == 'POST':
        fileData=request.FILES.values()[0]
        print fileData
        for chunk in fileData.chunks():
            message_str += chunk
    print message_str
    form_user_name = from_user_name_regexp.search(message_str)
    form_user_name = form_user_name.group(1)
    message_type = message_type_regexp.search(message_str)
    message_type = message_type.group(1)
    content = content_regexp.search(message_str)
    content = content.group(1)
    '''
    
    # change to etree method
    message_str =  request.read()

    root = ElementTree.fromstring(message_str)
    form_user_name = root.find('FromUserName').text
    to_user_name = root.find('ToUserName').text
    message_type = root.find('MsgType').text
    
    context = {'to_user_name':form_user_name,'from_user_name':to_user_name}

    if message_type == 'text':
        content = root.find('Content').text
        context.update({'content':content})
        reply_xml = generate_news_reply_xml(request,context)
    else:
        reply_xml = generate_text_reply_xml(request,context)
    
    return reply_xml

@csrf_exempt
def generate_text_reply_xml(request,context):
    
    text_xml = '''<xml>
        <ToUserName><![CDATA[%s]]></ToUserName>
        <FromUserName><![CDATA[%s]]></FromUserName>
        <CreateTime>%s</CreateTime>
        <MsgType><![CDATA[%s]]></MsgType>
        <Content><![CDATA[%s]]></Content>
        </xml>
    '''

    message_type = 'text'
    content = '''
亲~偶只能接受文字消息哦
[撇嘴][撇嘴][撇嘴]
请回复书名获取图书信息
[玫瑰][玫瑰][玫瑰]
    '''
    create_time = int(time())
    
    c = {
         'to_user_name':context['to_user_name'],
         'from_user_name':context['from_user_name'],
         'create_time':create_time,
         'message_type':message_type,
         'content':content
        }
    
    text_reply_xml = text_xml % (c['to_user_name'],c['from_user_name'],c['create_time'],c['message_type'],c['content'])    
    response = HttpResponse(text_reply_xml,content_type='application/xml; charset=utf-8')   
    
    return response
@csrf_exempt
def generate_news_reply_xml(request,context):
    
    book_name = context['content']
    book_message_for_xml = get_book_message(request,book_name)
    
    news_xml = '''<xml>
        <ToUserName><![CDATA[%s]]></ToUserName>
        <FromUserName><![CDATA[%s]]></FromUserName>
        <CreateTime>%s</CreateTime>
        <MsgType><![CDATA[%s]]></MsgType>
        <ArticleCount>%s</ArticleCount>
        <Articles>
        <item>
        <Title><![CDATA[%s]]></Title> 
        <Description><![CDATA[%s]]></Description>
        <PicUrl><![CDATA[%s]]></PicUrl>
        <Url><![CDATA[%s]]></Url>
        </item>
        </Articles>
        </xml>
   '''
    
    create_time = int(time())
    message_type = 'news'
    article_count = 1
    title = book_message_for_xml['title']
    description = book_message_for_xml['description']
    
    rating = '''
很棒：☆☆☆☆☆  81%
不错：☆☆☆☆      7%
凑合：☆☆☆         4%
不好：☆☆             3%
烂书：☆                3%
    '''
    picture_url_douban = book_message_for_xml['picture_url']
    
    gi = generate_image(picture_url_douban)
    picture_url = gi.get_image_url()
    
    # 1111 for test
    book_id = book_message_for_xml['book_id']
    jump_url_base = r'http://115.28.3.240/weixin/details_page/'
    jump_url = jump_url_base + book_id

    item = [
            {
            'title':title,
            'description':description,
            'picture_url':picture_url,
            'jump_url':jump_url
             }
            ]
    
    c = {
         'to_user_name':context['to_user_name'],
         'from_user_name':context['from_user_name'],
         'create_time':create_time,
         'message_type':message_type,
         'article_count':article_count,
         'item':item
           }
    
    news_reply_xml = news_xml % (c['to_user_name'],c['from_user_name'],c['create_time'],c['message_type'],c['article_count'],c['item'][0]['title'],c['item'][0]['description'],c['item'][0]['picture_url'],c['item'][0]['jump_url'])
    response = HttpResponse(news_reply_xml,content_type='application/xml; charset=utf-8')
    
    return response

def get_book_message(request,book_name):
    '''
    get book message from douban api
    '''
    rapi = RequestService()
    book_message_dict = {}
    book_message_for_xml = {}

    book_message_dict = rapi.search_books(unicode(book_name).encode('utf-8'))
    
    book_message_for_xml.update({'title':book_message_dict['books'][0]['title']})
    book_message_for_xml.update({'description':book_message_dict['books'][0]['summary']})
    book_message_for_xml.update({'picture_url':book_message_dict['books'][0]['images']['large']})
    # book id now is ISBN
    book_message_for_xml.update({'book_id':str(book_message_dict['books'][0]['isbn13'])})

    return book_message_for_xml

def get_cover(request,cover_name):    
    '''
    address for book cover
    '''
    img_path = os.path.dirname(__file__) + '/static/douban_image/' + cover_name
    img_f = open(img_path,'rb')
    img_content = img_f.read() 
    img_f.close()
    response = HttpResponse(img_content,content_type='image/jpeg')
    #response = HttpResponse('ok')
    return response
    
def details_page(request,book_id):
    '''
    details page of news
    '''
    # judge if use mobile device
    #print request.META['HTTP_USER_AGENT']
    
    # get book messages by book id(ISBN)
    rapi = RequestService()
    book_message = rapi.search_book_by_isbn(book_id)

    c = {
         'c':book_message
         }
    
    return render_to_response('details_page.html',c)