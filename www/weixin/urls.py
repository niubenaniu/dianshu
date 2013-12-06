from django.conf.urls import patterns, include, url


# dianshu for weixin
urlpatterns = patterns('weixin.views',
    url(r'^check_signature/?$', 'check_signature'),
)
