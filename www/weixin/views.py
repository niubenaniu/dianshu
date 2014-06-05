# -*- coding:UTF-8 -*-

# created by niuben at 2013-12-09

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
import simplejson

from api_douban.service import RequestService as RequestService_douban
from api_sina.service import RequestService as RequestService_sina
#from api_tencent.service import RequestService as RequestService_tencent
from api_renren.service import RequestService as RequestService_renren
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
            user_subscribe(form_user_name)
            reply_xml = generate_text_reply_xml(request,context,type='greet')
        elif event_type == 'unsubscribe':
            user_unsubscribe(form_user_name)
            
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
    rapi = RequestService_douban()
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
    rapi = RequestService_douban()
    book_message = rapi.search_book_by_isbn(book_isbn)
    book_id = book_message['id']
    request.session['book_id'] = book_id
    request.session['book_title'] = book_message['title']

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
    
    return render_to_response('details_page.html',c,context_instance=RequestContext(request))

def get_ratings(request):
    '''
        get book ratings via spider
    '''
    book_id = request.session['book_id']
    
    rapi = RequestService_douban()
    ratings = rapi.get_ratings(book_id)

    return HttpResponse(ratings,content_type='application/javascript')

def get_book_reviews_by_offset(request,is_offset=0):
    '''
        get book reviews by offset via use Ajax method
    '''
    reviews_source = request.GET.get('source')
        
    if reviews_source == 'douban':
        return get_book_reviews_by_offset_douban(request,is_offset)
    elif reviews_source == 'sina':
        return get_book_reviews_by_offset_sina(request,is_offset)
    elif reviews_source == 'tencent':
        return get_book_reviews_by_offset_tencent(request,is_offset)
    elif reviews_source == 'renren':
        return get_book_reviews_by_offset_renren(request,is_offset)
    
def get_book_reviews_by_offset_douban(request,is_offset=0):
    
    if not is_offset:
        request.session['next_offset_douban'] = 1
    else:
        request.session['next_offset_douban'] += 5    

    book_id = request.session['book_id']

    rapi = RequestService_douban()
    book_reviews = rapi.get_book_reviews(book_id.encode('utf-8'),offset=request.session['next_offset_douban'])

    reviews = []
    reg_exp = re.compile(r'(\d+\-\d+\-\d+).*?(\d+\:\d+)\:')
    
    for book_review in book_reviews['entry']:
        
        reg_result = reg_exp.match(book_review['published']['texts'])
        published = reg_result.group(1) + '  ' + reg_result.group(2)

        author_image = book_review['author']['link'][2]['href']#.replace(r'/u',r'/ul')
 
        review = {
                  'author_image' : author_image,
                  'author_name' : book_review['author']['name']['texts'],
                  'title' : book_review['title']['texts'],
                  # 用户可能没有星评，所以给个默认值5
                  'rating' : (book_review['rating']['value'] if book_review.has_key('rating') else 5),
                  'published' : published,
                  'summary' : book_review['summary']['texts'],
                  # 默认头像链接为http://img3.douban.com/icon/uxxx,大图为http://img3.douban.com/icon/ulxxx
                  'link' : book_review['link'][1]['href'],
                  'votes' : book_review['votes']['value'],
                  'useless' : book_review['useless']['value'],                 
                  }
        
        reviews.append(review)
    
    c = {
         'reviews':reviews,
         }
    
    return render_to_response('third_party_content/book_reviews_douban.html',c)

def get_book_reviews_by_offset_sina(request,is_offset):
    
    rapi = RequestService_sina()
    keyword = unicode(request.session['book_title']).encode('utf-8')
    book_reviews = rapi.search_comment(keyword)
    
    reviews = []

    for book_review in book_reviews:
        review = {
                  'image':book_review['img'],#.decode('unicode-escape'),
                  'user':book_review['user'].decode('unicode-escape'),
                  # 时间比较新，所以微博的数据实时性还是很高的。
                  'time':book_review['time'].decode('unicode-escape'),
                  'comment':book_review['comment'].decode('unicode-escape').replace(r'\/',r'/'),
                  'judge':book_review['num'],
                  }
        
        reviews.append(review)
    
    c = {
         'reviews':reviews,
         }    
    #return render_to_response('third_party_content/book_reviews_sina.html',simplejson.dumps(c))
    return HttpResponse(simplejson.dumps(c))

def get_book_reviews_by_offset_tencent(request,is_offset):

    return HttpResponse('<div class="list-group-item">tencent</div>')

def get_book_reviews_by_offset_renren(request,is_offset):

    rapi = RequestService_renren()
    keyword = unicode(request.session['book_title']).encode('utf-8')
    book_reviews = rapi.search_comment(keyword)

    reviews = []

    for book_review in book_reviews:
        review = {
                  'image':book_review['img'],
                  'user':book_review['user'],
                  # 有比较久远的时间，所以人人的数据实时性不是很高。
                  'time':book_review['time'],
                  'comment':book_review['comment'],
                  }
        
        reviews.append(review)

    c = {
         'reviews':reviews,
         }

    #return render_to_response('third_party_content/book_reviews_renren.html',c)
    return HttpResponse(simplejson.dumps(c))

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

def user_subscribe(open_id):
    '''
        save user which subscribe
    '''

    try:    
        article = User(open_id=open_id)
        article.save()
    except:
        return 'failed'

    return 'success'

def user_unsubscribe(open_id):
    '''
        remove user which unsubscribe
    '''

    try:    
        user = User.objects.get(open_id=open_id)
        if user:
            user.delete()
    except:
        return 'failed'

    return 'success'
