# -*- coding:UTF-8 -*-

# createed by niuben at 2013-12-09

from django.shortcuts import render_to_response,render,RequestContext
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
import hashlib
import re


@csrf_exempt
def auto_service(request):
    '''
    support the service for 'dianshu'
    '''
    # verify the signature
    '''
    varify_flag = is_varified()
    return HttpResponse(varify_flag) if varify_flag else HttpResponse('signature verify failed!')
    '''
    
    # service
    reply_msg = auto_reply_service(request)   
    return reply_msg
    
def is_varified(request):
    '''
    function: check if the signature verified successful
    '''
    echostr = request.GET['echostr']
    if (check_signature(request)):
        return HttpResponse(echostr)
    else:
        return None
def check_signature(request):
    '''
    function: verify the signature
    '''
    signature = unicode(str(request.GET['signature']))
    timestamp = unicode(str(request.GET['timestamp']))
    nonce = unicode(str(request.GET['nonce']))
    
    token = 'dianshu_weinxin'
 
    # step 1: get a srot list   
    sig_array = [token,timestamp,nonce]
    sig_array.sort()
    
    # step 2: get a string
    sig_str = ''.join(sig_array)
    
    # step 3: encrypt by sha1 
    hash_new = hashlib.sha1()
    hash_new.update(sig_str)
    hash_value = hash_new.hexdigest()
    
    if (hash_value == signature):
        return True
    else:
        return False

def auto_reply_service(request):
    '''
     
    '''
    
    # used to received text message xml
    from_user_name_regexp = re.compile(r'<FromUserName><!\[CDATA\[(.+)\]\]></FromUserName>')
    message_type_regexp = re.compile(r'<MsgType><!\[CDATA\[(.+)\]\]></MsgType>')
    content_regexp = re.compile(r'<Content><!\[CDATA\[(.+)\]\]></Content>')
    
    if request.method == 'POST':
        fileData=request.FILES.values()[0]
        for chunk in fileData.chunks():
            chunk += chunk
    
    form_user_name = from_user_name_regexp.search(chunk)
    form_user_name = form_user_name.group(1)
    message_type = message_type_regexp.search(chunk)
    message_type = message_type.group(1)
    content = content_regexp.search(chunk)
    content = content.group(1)
    
    c = {'from_user_name':form_user_name,'message_type':message_type,'content':content}
    print c
        #   fp.write(chunk)
        #fp.close()

    return HttpResponse('ok')

def generate_reply_xml(request):
    generate_content(request)
    c = {}
    return render_to_response('book_messages.xml',c)

def generate_book_content(request):
    
    return HttpResponse('ok')

def receive_xml(request):
    
    return HttpResponse('ok')