# -*- coding:UTF-8 -*-

# createed by niuben at 2013-12-09

from django.shortcuts import render_to_response,render,RequestContext
from django.http import HttpResponse,Http404
import hashlib

def auto_service(request):
    '''
    support the service for 'dianshu'
    '''
    # verify the signature
    is_access(requet)

    # service
    #auto_reply_service(request)   
    
def is_access(request):
    '''
    function: check if the signature verified successful
    '''
    echostr = request.GET['echostr']
    if (check_signature(request)):
        return HttpResponse(echostr)
    else:
        return HttpResponse('signature verify failed!')

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
    
    return HtteResponse('ok')
