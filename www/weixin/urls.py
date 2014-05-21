from django.conf.urls import patterns, include, url

# dianshu for weixin
urlpatterns = patterns('weixin.views',
    url(r'^auto_service/$', 'auto_service'),
    url(r'^cover_for_news/(?P<cover_name>\S+)$', 'get_cover'),
    url(r'^details_page/(?P<book_isbn>\w+)$', 'details_page'),
    url(r'^get_book_reviews_by_offset/(?P<is_offset>(1?))$', 'get_book_reviews_by_offset'),
    url(r'^get_ratings/$', 'get_ratings'),  
)

# article history page
urlpatterns += patterns('weixin.views',
    url(r'^history/$', 'history_list_page'),
)

# article record page
urlpatterns += patterns('weixin.online_views',
    url(r'^article_record/$', 'article_record'),
    url(r'^article_save/$', 'article_save'),
)

# online home page
urlpatterns += patterns('weixin.online_views',
    url(r'^$/?', 'index'),
    url(r'^home/$', 'online_home_page'),
    url(r'^get_article_by_id/(?P<article_id>\d+)$', 'get_article_by_id'),
    url(r'^get_user_count/$', 'get_user_count'),
    url(r'^book_gession/(?P<search_string>.+)/(?P<is_gession>\d)$', 'book_gession'),
    url(r'^get_article_by_offset/(?P<offset>.+)$', 'get_article_by_offset'),
    url(r'^get_search_history/$', 'get_search_history_from_cookie'),
    url(r'^get_view_history/$', 'get_view_history_from_cookie'),
)

# online book page
urlpatterns += patterns('weixin.online_views',
    url(r'^search/$', 'book_search'),
    url(r'^search_results/$', 'search_results'),
    url(r'^book/(?P<book_isbn>\w+)$', 'details_page'),
)
