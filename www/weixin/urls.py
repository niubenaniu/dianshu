from django.conf.urls import patterns, include, url


# dianshu for weixin
urlpatterns = patterns('weixin.views',
    url(r'^auto_service/$', 'auto_service'),
    url(r'^cover_for_news/(?P<cover_name>\S+)$', 'get_cover'),
    url(r'^details_page/(?P<book_id>\w+)$', 'details_page'),
    url(r'^test_page/$', 'test_page'),
    url(r'^history/$', 'history_list_page'),
    url(r'^article_record/$', 'article_record')
)