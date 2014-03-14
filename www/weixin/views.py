# -*- coding:UTF-8 -*-

# createed by niuben at 2013-12-09
from django.shortcuts import render_to_response,render,RequestContext
from django.http import StreamingHttpResponse,HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from xml.etree import ElementTree 
from time import time
import varify
import hashlib
import os
import pycurl
import cStringIO
import re

from api_douban.service import RequestService
from generate_img.generate_img import generate_image

TOKEN = 'dianshu_weinxin'

@csrf_exempt
def auto_service(request):
    '''
    support the service for 'dianshu'
    '''
    # verify the signature
    if request.method == 'GET':
        varify_flag = varify.is_varified(request,TOKEN)
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
        # histort and help messages
        if content.lower() == 'l':
            reply_xml = generate_text_reply_xml(request,context,type='history')
        elif content.lower() == 'h':
            reply_xml = generate_text_reply_xml(request,context,type='help')
        else:
            context.update({'content':content})
            reply_xml = generate_news_reply_xml(request,context)
    # 预留语音识别接口
    #elif message_type == 'voice':
    #media_id = root.find('MediaId').text
    #content = get_text_from_voice(media_id)
    #context.update({'content':content})
    #reply_xml = generate_news_reply_xml(request,context)
    elif message_type == 'event':
        event_type = root.find('Event').text
        if event_type == 'subscribe':
            reply_xml = generate_text_reply_xml(request,context,type='greet')
    else:
        reply_xml = generate_text_reply_xml(request,context)
    
    return reply_xml

@csrf_exempt
def generate_text_reply_xml(request,context,type='adjust'):
    
    text_xml = '''<xml>
        <ToUserName><![CDATA[%s]]></ToUserName>
        <FromUserName><![CDATA[%s]]></FromUserName>
        <CreateTime>%s</CreateTime>
        <MsgType><![CDATA[%s]]></MsgType>
        <Content><![CDATA[%s]]></Content>
        </xml>
    '''

    message_type = 'text'
    
    if type == 'greet' or type == 'help':
        content = '''
欢迎关注《点书》[微笑]

-------文章推送-------
每周一次精选书评推送
-------图书查询-------
回复书名可自助查询图书信息
只支持回复文本消息
-------历史文章-------
回复“l”
-------帮助信息-------
回复“h”
-------调戏主人[坏笑]----
微信：Benforward
    '''   
    elif type == 'history':
        content = get_old_article()
    else:    
        content = '''
亲~偶只认识文字消息
[撇嘴][撇嘴][撇嘴]
请回复书名获取图书信息
[玫瑰][玫瑰][玫瑰]
查看帮助信息请回复“h”
查看历史文章请回复“l”
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

# 订阅号未认证，语音识别不支持，暂时不做，保留接口
def get_text_from_voice(media_id):
    buf = cStringIO.StringIO()
    c = pycurl.Curl()
    url = 'http://file.api.weixin.qq.com/cgi-bin/media/get?access_token=' + TOKEN + '&media_id=' + media_id

    c.setopt(c.URL,url)
    c.setopt(c.WRITEFUNCTION,buf.write)
    c.perform()

    print buf.getvalue()
    buf.close()
    
    return u'xxxx'
    
def details_page(request,book_isbn):
    '''
    details page of news
    '''
    # judge if use mobile device
    #print request.META['HTTP_USER_AGENT']
    
    # get book messages by book id(ISBN)
    rapi = RequestService()
    book_message = rapi.search_book_by_isbn(book_isbn)
    book_id = book_message['id']
    request.session['book_id'] = book_id

    c = {
         # get book_message from douban API
         'tags':book_message['tags'],
         'cover':book_message['images']['large'],
         'title':book_message['title'],
         'author':book_message['author'],
         'publisher':book_message['publisher'],
         'price':book_message['price'],
         'rating':book_message['rating'],
         'author_intro':book_message['author_intro'],
         'summary':book_message['summary'],
         'id':book_message['id'],
         # get book_message from spider
         'rating_details':1,
         }
    
    return render_to_response('details_page.html',c)

def get_book_reviews_by_offset(request,is_offset=0):
    '''
        get book reviews by offset via use Ajax method
    '''    
    if not is_offset:
        request.session['next_offset'] = 0
    else:
        request.session['next_offset'] += 5    

    book_id = request.session['book_id']

    rapi = RequestService()
    book_reviews = rapi.get_book_reviews(book_id.encode('utf-8'))
    
    reviews = []
    reg_exp = re.compile(r'(\d+\-\d+\-\d+).*?(\d+\:\d+)\:')
    
    for book_review in book_reviews['entry']:
        
        reg_result = reg_exp.match(book_review['published']['texts'])
        published = reg_result.group(1) + '  ' + reg_result.group(2)
        
        author_image = book_review['author']['link'][2]['href'].replace(r'/u',r'/ul')
        
        review = {
                  'author_image' : author_image,
                  'author_name' : book_review['author']['name']['texts'],
                  'title' : book_review['title']['texts'],
                  'rating' : book_review['rating']['value'],
                  'published' : published,
                  'summary' : book_review['summary']['texts'],
                  # 默认头像链接为http://img3.douban.com/icon/uxxx,大图为http://img3.douban.com/icon/ulxxx。
                  'link' : book_review['link'][1]['href'],
                  'votes' : book_review['votes']['value'],
                  'useless' : book_review['useless']['value'],                 
                  }
        
        reviews.append(review)
    print reviews
    
    c = {
         'reviews':reviews,
         }
    
    return render_to_response('book_reviews.html',c)
    
def test_page(request):
    
    return render_to_response('test_page.html')

def get_old_article():
    '''
        return a url of old article
    '''
    url = 'http://115.28.3.240/weixin/history'
    return '点此查看历史文章：' + url


# articles record and history list
def history_list_page(request):
    '''
        list page of history article
    '''
    return render_to_response('history_list_page.html')

def history_article_details(request):
    '''
        list page of history article
    '''
    return render_to_response('history_list_page.html')

def article_record(request):
    
    return render_to_response('article_record.html')