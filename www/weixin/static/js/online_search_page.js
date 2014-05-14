var search_string = decodeURIComponent(location.search.substr(6));
if(search_string.length >=10){
    sub_search_string = search_string.substr(0,10) + '...';
}else{
	sub_search_string = search_string;
}
var html_dt = '<dt><h4><span class="glyphicon glyphicon-list"></span> <span id="search-string"><em>' + sub_search_string + '</span></em> 的搜索结果</h4></dt>';
jq('#book dl').prepend(html_dt);

// 获取第一页的搜索结果
exe_search_ajax(0);
jq("#book-search").focus();
jq("#book-search").val(search_string);
var search_button = '<button id="search-button" type="submit" class="btn btn-default"><i class="icon-search"></i></button>';
jq("#book-search").after(search_button);

var spin_html = '<span class="icon-spinner icon-spin"></span>';

jq('#search-more a').click(
		function(){
			jq('#search-more').prepend(spin_html);
			jq('#search-more a').text(' 哎哟~~~');
			exe_search_ajax(1);
		}
);

function exe_search_ajax(is_offset){
	url = '../search_results/';
	data = {'search_string':search_string,"is_offset":is_offset};
		
	jq.ajax({
	    url:url,
	    data:data,
	    dataType:"json",
 	    success:function(data){
 	    		
 	    	    jq('#search-more a').text(' 查看更多...');

 	    	    if(!data){
 	    	    	    jq('#search-more a').text('好了，就这些啦~~~');
 	    	    }
 	    	    var books = eval(data);
 	    	    	
 	    	    for(i in books){

	 	    	    	var html_li = '<li class="media">';
	 	    	    	html_li += '<a class="pull-left" href="../book/' + books[i]['isbn'] + '">';
	 	    	    	html_li += '  <img id="cover" class="media-object" src="' + books[i]['cover'] + '" alt="封面不存在" href="#">';
	 	    	    	html_li += ' </a>';
	 	    	    	html_li += '<div class="media-body">';
	 	    	    	html_li += '  <h4 class="media-heading"><a href="../book/' + books[i]['isbn'] + '">' + books[i]['title'] + '</a></h4>';
	 	    	    	html_li += '  <p><span>作者：</span>' + books[i]['author'] + '</p>';
	 	    	    	html_li += '  <p><span>出版社：</span>' + books[i]['publisher'] + '</p>';
	 	    	    	html_li += '  <p><span>出版年：</span>' + books[i]['pub_date'] + '</p>';
	 	    	    	if(!books[i]['price']){
	 	    	    		books[i]['price'] = '暂无';
	 	    	    	}
	 	    	    	html_li += '  <p><span>定价：</span>' + books[i]['price'] + '</p>';
	 	    	    	html_li += '</div>';
	 	    	    	html_li += '</li>';
 	    	    	
 	    	    	    jq('#search-results').append(html_li);
 	    	    }
 	    		// 请求完成之后去掉旋转图标
 	    		jq('.icon-spinner').remove();
 	    		
                if(!is_offset){
	 	    		get_search_history();
	 	    		get_view_history();
                }
	    },
        error:function(XHRObj,msg,e){
        	    jq('#search-more a').text('好了，就这些啦~~~');
        	    jq('.icon-spinner').remove();
        	    
                if(!is_offset){
	 	    		get_search_history();
	 	    		get_view_history();
                }
	    } 
	});
}

function get_search_history(){
	var url = '../get_search_history/';
	jq.ajax({
	    url:url,
	    dataType:"json",
        success:function(data){
            var historys = eval(data);

        	if (data == 'error'){
        		jq('#search-history').append('<li><p>随便看看吧~~~</p></li>');
        	}else{
        		    var html_li ='<li>';
                for(i in historys){
                	
                	if(historys[i].length >=10){
                	    history = historys[i].substr(0,18) + '...';
                	}else{
                		history = historys[i];
                	}
    	 		    html_li += '<a href="../search?name=' + history + '"><span class="label label-default">' + history + '</span></a>';
        	    }
                html_li += '</li>';
                jq('#search-history').append(html_li);
            }
 	    },
	});
}

function get_view_history(){
	var url = '../get_view_history/';
	jq.ajax({
	    url:url,
	    dataType:"json",
        success:function(data){
            var books = eval(data);
        	if (data == 'error'){
        		jq('#view-history').append('<li><p>随便看看吧~~~</p></li>');
        	}else{
                for(i in books){
                	
/*                	if(historys[i].length >=10){
                	    history = historys[i].substr(0,15) + '...';
                	}else{
                		history = historys[i];
                	}*/
                	
                	
 	    	    	var html_li = '<li class="media">';
 	    	    	html_li += '<a class="pull-left" href="../book/' + books[i]['isbn'] + '">';
 	    	    	html_li += '  <img id="cover" class="media-object" src="' + books[i]['cover'] + '" alt="封面不存在" href="#">';
 	    	    	html_li += ' </a>';
 	    	    	html_li += '<div class="media-body">';
 	    	    	html_li += '  <h5 class="media-heading"><a href="../book/' + books[i]['isbn'] + '">' + books[i]['title'] + '</a></h5>';
 	    	    	html_li += '  <small><span>作者：</span>' + books[i]['author'] + '</small>';
 	    	    	html_li += '  <small><span>出版社：</span>' + books[i]['publisher'] + '</small>';
 	    	    	html_li += '  <small><span>出版年：</span>' + books[i]['pub_date'] + '</small>';
 	    	    	if(!books[i]['price']){
 	    	    		books[i]['price'] = '暂无';
 	    	    	}
 	    	    	html_li += '  <small><span>定价：</span>' + books[i]['price'] + '</small>';
 	    	    	html_li += '</div>';
 	    	    	html_li += '</li>';

    	 		    jq('#view-history').append(html_li);
        	    }
            }
 	    },
	});
}
