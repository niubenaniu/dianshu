from django.conf.urls import patterns, include, url


# dianshu for weixin
urlpatterns = patterns('weixin.views',
    url(r'^auto_service/$', 'auto_service'),
)
