from django.conf.urls import patterns, include, url

# dianshu for weixin
urlpatterns = patterns('weixin.views',
    url(r'^auto_service/$', 'auto_service'),
    url(r'^cover_for_news/(?P<cover_name>\S+)$', 'get_cover'),
    url(r'^details_page/(?P<book_isbn>\w+)$', 'details_page'),
    #url(r'^test_page/$', 'test_page'),
    url(r'^get_book_reviews_by_offset/(?P<is_offset>(1?))$', 'get_book_reviews_by_offset'),
    url(r'^get_ratings/$', 'get_ratings'),  
)


urlpatterns += patterns('weixin.views',
    url(r'^home/$', 'online_home_page'),
)

urlpatterns += patterns('weixin.views',
    url(r'^history/$', 'history_list_page'),
    url(r'^article_record/$', 'article_record'),
    url(r'^article_save/$', 'article_save'),
)