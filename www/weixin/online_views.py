# -*- coding:UTF-8 -*-

# created by niuben at 2014-05-01
from django.shortcuts import render_to_response,render,RequestContext
from django.http import StreamingHttpResponse,HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
import simplejson

from api_douban.service import RequestService as RequestService_douban
from models import Article,User

def article_record(request):
    
    return render_to_response('article_record/article_record.html',context_instance=RequestContext(request))

def article_save(request):
    '''
        save article which be sent from article_record page
    '''
    #import time
    #now = time.strftime('%Y-%m-%d %H:%M')
    c={}
    try:
        
        article = Article(title=request.POST.get('title'),author=request.POST.get('author'),\
                    content=request.POST.get('content'))
        article.save()
    
        c = {
             'result':'保存成功！',
             'return_code':0,
        }
    
    except:
        c = {
             'result':'Oops！！！好像出了点差错！点书正在努力反省中~~~',
             'return_code':1,
        }
        
        return render_to_response('article_record/article_save.html',c)

    return render_to_response('article_record/article_save.html',c)

# home page
def online_home_page(request):
    '''
        home web page
    '''
    article_list = Article.objects.all().order_by("-publish_date")[0:10]
    #article_list = Article.objects.raw('select id,title,publish_date from weixin_article limit 10')
    
    for article in article_list:
        article.publish_date = article.publish_date.strftime('%Y年%m月%d日 %H:%M')
    
    
    c = {
         'article_list':article_list,
    }
    
    return render_to_response('online_home_page.html',c,context_instance=RequestContext(request))

def get_article_by_offset(request,offset):
    
    index_start = (int(offset) - 1) * 10;
    index_end = index_start + 10
    
    article_obj = Article.objects.all()
    article_count = article_obj.count()
    article_list = article_obj.order_by("-publish_date")[index_start:index_end]
    #article_list = Article.objects.raw('select id,title,publish_date from weixin_article limit 10')
    
    article_dict = []
    tmp_dict = {}
    
    for article in article_list:
        article.publish_date = article.publish_date.strftime('%Y年%m月%d日 %H:%M')
        tmp_dict = {
                    'id':article.id,
                    'title':article.title,
                    'publish_date':article.publish_date,
                    }
        
        article_dict.append(tmp_dict)
        
    article_json = {
         'article_count':article_count,
         'article_list':article_dict,
         }
    
    return HttpResponse(simplejson.dumps(article_json))

def get_article_by_id(request,article_id):
    
    article = Article.objects.get(id=article_id)

    c = {
         'title':article.title,
         'publish_date':article.publish_date.strftime('%Y年%m月%d日 %H:%M'),
         'content':article.content,
    }
    
    return HttpResponse(simplejson.dumps(c))


def get_user_count(request):
    '''
        get user count
    '''

    try:    
        user_count = User.objects.all().count()
    except:
        return 9999

    return HttpResponse(user_count)

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
         'pages':book_message['pages'],
         'pub_date':book_message['pubdate'],
         'isbn':book_isbn,
         'rating':book_message['rating'],
         'author_intro':book_message['author_intro'],
         'summary':book_message['summary'],
         'id':book_message['id'],
         # get book_message from spider
         'rating_details':1,
         }
    
    response = render_to_response('online_details_page.html',c,context_instance=RequestContext(request))
    set_cookie(request,response,book_isbn,type='view')
    
    return response

def book_gession(request,search_string,is_gession):
    '''
        gession book when type in search box
    '''
    
    book_message_dict = {}
    book_message_json = []
    tmp_dict = {}
    
    book_message_dict = get_books_by_offset(request,search_string=search_string,is_gession=is_gession)
    
    for book_message in book_message_dict['books']:
        
        tmp_dict = {
                    'cover':book_message['images']['small'],
                    'title':book_message['title'],
                    'author':book_message['author'],
                    'publisher':book_message['publisher'],
                    'isbn':str(book_message['isbn13']),
                    }
        
        book_message_json.append(tmp_dict)
    
    return HttpResponse(simplejson.dumps(book_message_json))

def book_search(request):
    '''
        book search page
    '''
    
    return render_to_response('online_search_page.html',context_instance=RequestContext(request))

def search_results(request):
    '''
        search books by offset
    '''
    is_offset = request.GET['is_offset']
    search_string = request.GET['search_string']
    book_message_dict = {}
    book_message_json = []
    tmp_dict = {}
    
    book_message_dict = get_books_by_offset(request,search_string=search_string,is_offset=is_offset)
    
    for book_message in book_message_dict['books']:
        
        tmp_dict = {
                    'cover':book_message['images']['large'],
                    'title':book_message['title'],
                    'author':book_message['author'],
                    'publisher':book_message['publisher'],
                    'pub_date':book_message['pubdate'],
                    'price':book_message['price'],
                    'isbn':str(book_message['isbn13']) if book_message.has_key('isbn13') else book_message['isbn10'],
                    }
        
        book_message_json.append(tmp_dict)
    
    response = HttpResponse(simplejson.dumps(book_message_json))
    
    set_cookie(request,response,search_string)
    
    return response
    
def get_books_by_offset(request,search_string='百年孤独',is_offset=0,is_gession=0):
    '''
        get books by offset
    '''
    if not int(is_offset):
        request.session['next_offset'] = 0
        if int(is_gession):
            limit = 3
        else:
            limit = 10
    else:
        request.session['next_offset'] += 10
        limit = 10
    
    rapi = RequestService_douban()
    book_message_dict = {}

    book_message_dict = rapi.search_books(unicode(search_string).encode('utf-8'),offset=request.session['next_offset'],limit=limit)
    
    return book_message_dict

def get_cookie_key(request,type='search'):
    '''
        get cookie key
        type:
            search: search_history
            view: view history
    '''
    
    cookie_key = {}
    
    max_num = type + '_max_num'
    key_string = '_' + type + '_string'
    
    if request.COOKIES.has_key(max_num):
        current_num = int(request.COOKIES[max_num]) + 1
    else:
        current_num = 1

    cookie_key = {
                  'key':str(current_num) + key_string,
                  max_num:current_num,
                  }
    
    return cookie_key
    
def set_cookie(request,response,value,type='search'):
    '''
        set cookie
        type:
            search: search_history
            view: view history
    '''
    
    cookie_key = get_cookie_key(request,type)
    max_num = type + '_max_num'
    value = unicode(value).encode('UTF-8')
    
    response.set_cookie(cookie_key['key'],value)
    response.set_cookie(max_num,cookie_key[max_num])

def get_history_from_cookie(request,type='search',limit=10):
    '''
        get search/view history from cookie by default 10 items
        type:
            search: search_history
            view: view history
    '''
    
    max_num = type + '_max_num'

    if request.COOKIES.has_key(max_num):
        index_end = request.COOKIES[max_num]
        index_start = int(index_end) - int(limit) if int(index_end) > int(limit) else 1
        key_string = '_' + type + '_string'
        history_list = []
        
        if int(index_end) == 1:
            history_list.append(request.COOKIES['1' + key_string])
        elif int(index_end) < 10:
            start = int(index_start)
        else:
            start = int(index_start) + 1
        end = int(index_end) + 1
        
        for i in xrange(start,end):
            current_key = str(i) + key_string
            history_list.append(request.COOKIES[current_key])
        history_list.reverse()
        return HttpResponse(simplejson.dumps(history_list))
    else:
        return HttpResponse(simplejson.dumps(['error']))

def get_search_history_from_cookie(request):
    
    return get_history_from_cookie(request,type='search',limit=20)

def get_view_history_from_cookie(request):
    
    isbn_list = get_history_from_cookie(request,type='view')
    rapi = RequestService_douban()

    book_message_dict = {}
    book_message_json = []
    tmp_dict = {}

    for book_isbn in simplejson.loads(isbn_list.content):
        book_message_dict = rapi.search_book_by_isbn(book_isbn)

        tmp_dict = {
                    'cover':book_message_dict['images']['large'],
                    'title':book_message_dict['title'],
                    'author':book_message_dict['author'],
                    'publisher':book_message_dict['publisher'],
                    'pub_date':book_message_dict['pubdate'],
                    'price':book_message_dict['price'],
                    'isbn':str(book_message_dict['isbn13']) if book_message_dict.has_key('isbn13') else book_message_dict['isbn10'],
                    }

        book_message_json.append(tmp_dict)

    return  HttpResponse(simplejson.dumps(book_message_json))