
var jq = $.noConflict();

//jq('#about').tooltip();

function change_search_box(){
	jq(".form-control").animate({width:'600px'},300);
	if(!jq("#search-button").html()){
		var search_button = '<button id="search-button" type="submit" class="btn btn-default"><i class="icon-search"></i></button>';
		jq("#book-search").after(search_button);
	}
}
	
jq("#book-search").focus(function(){
	if(jq("#book-search").val()){
		gession();
	}else{
		jq(".form-control").animate({width:'600px'},300);
	}
}	
);

jq("#book-search").blur(function(){
	setTimeout('jq("#gession").empty()',100);
	jq("#book-search").addClass('book-search-blur');
	if(!jq("#book-search").val()){
		jq(".form-control").animate({width:'258px'},300);
		jq(".navbar-form").animate({right:'10%'},300);
		if(jq("#search-button").html()){
			jq("#search-button").remove();
		}
	}	
}
);

jq("#book-search").keydown(function(){
	if(!jq("#search-button").html()){
		var search_button = '<button id="search-button" type="submit" class="btn btn-default"><i class="icon-search"></i></button>';
		jq("#book-search").after(search_button);
	}
}
);

jq("#book-search").keyup(function(){
	jq("#gession").empty();
	if(jq("#book-search").val()){
		gession();
	}
}
);

function gession(){
	var p = jq("#book-search").val();
	var url = '../book_gession/' + p + '/1';
	
	jq.ajax({
	    url:url,
	    dataType:"json",
 	    success:function(data){
            var books = eval(data);
            
            var html_book_gession = '<div id="book-gession">';
            html_book_gession += '<ul class="media-list" id="book-gession-list">';
            html_book_gession += '</ul>';
            html_book_gession += '</div>';
            jq("#gession").append(html_book_gession);
            
            for(i in books){               	    
            	    var html_li = '<li class="media">';
            	    html_li += '<a class="pull-left" href="../book/' + books[i]['isbn'] + '">';
            	    	html_li += '  <img class="media-object" src=' + books[i]['cover'] + ' alt="封面不存在" href="#">';
            	    html_li += '</a>';
            	    	html_li += '<div class="media-body">';
            	    	html_li += '  <h4 class="media-heading"><a href="../book/' + books[i]['isbn'] + '">' + books[i]['title'].replace(p,'<span style="color:red">'+p+'</span>') + '</a></h4>';
            	    	html_li += '  <p>作者：' + books[i]['author'].toString().replace(p,'<span style="color:red">'+p+'</span>') + '</p>';
            	    	html_li += '  <p>出版社：' + books[i]['publisher'] + '</p>';
            	    	html_li += '</div>';
            	    	html_li += '</li>';
            	    jq("#book-gession-list").append(html_li);
            }
	    },

	});
}
