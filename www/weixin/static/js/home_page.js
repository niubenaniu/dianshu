$('#bcode-img').pin();
$('#about').tooltip();
$('#article-dialog').on('show.bs.modal', function (e) {
	
	var url = '../get_article_by_id/' + $(e.relatedTarget).attr('article-id');
    
	$.getJSON(url,function(article){
        	$('#article-title').text(article.title);        	
        	$('#publish-date').text(article.publish_date);
        	$('#article-content').text(article.content);
    });
});