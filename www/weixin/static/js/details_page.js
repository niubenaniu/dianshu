// 生成星评
jq(function(){
	var rating_value = jq('#rating_value').text();
	var star_num = Math.floor(rating_value/2);
	var star_half_num = Math.ceil(rating_value/2 - star_num);
	var star_empty_num = 5 - star_num - star_half_num;
	
	star_html = '<span class="icon-star"></span>';
	star_half_html = '<span class="icon-star-half"></span>';
	star_empty_html = '<span class="icon-star-empty"></span>';
	
	for (i=0; i<star_num; i++){
		jq('#stars').append(star_html);
	}

    for (i=0; i<star_half_num; i++){
        jq('#stars').append(star_half_html);
    }
    
    for (i=0; i<star_empty_num; i++){
        jq('#stars').append(star_empty_html);
    }
    
    jq('#ratings').removeAttr('style');
	
});

// 生成饼图
jq(function(){
	
	var url = 'http://115.28.3.240/weixin/get_ratings/';
	
    jq.ajax({
        url:url,
        dataType:"json",
        success:function(data){
        	chart_pie(data);
        },
        error:function(XHRObj,msg,e){
            //error_msg = '<p class="error">' +　msg + ": " +　e + '</p>'
            //error_msg = '<p class="error">' + '抱歉！没有找到相关内容~' + '</p>';
        } 
    });
});

function chart_pie(data) {
	jq('#container').highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false
        },
        title: {
            text: ''
        },
        tooltip: {
            pointFormat: '比例: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    color: '#000000',
                    connectorColor: '#000000',
                    style: {
                    	fontSize : '200%',
                    	fontWeight: 'bold'
                    },
                    format: '<span class="ratings_text"><b>{point.name}: </b>{point.percentage:.1f} %</span>'
                }
            }
        },
        series: [{
            type: 'pie',
            name: ' ',
            data:data
        }]
    });
}

// 初始化
jq(function(){
		jq('#reviewsTab a:first').tab('show');
    }
	);
  
// 全局数据
var url_nooffset = 'http://115.28.3.240/weixin/get_book_reviews_by_offset/';
var url_offset = url_nooffset + '1';

var data_param = 'source='
var data_douban = data_param + 'douban'
var data_sina = data_param + 'sina'
var data_tencent = data_param + 'tencent'
var data_renren = data_param + 'renren'

var flags = {'flag_sina':0,'flag_tencent':0,'flag_renren':0};

// 界面请求逻辑
jq(document).ready(
		function(){
			get_reviews(data_douban);
		}
		);	
	
jq('#sina-tab').click(
		function(){
 			if (!flags['flag_sina']){
				get_reviews(data_sina);
			}
		}
		);

jq('#tencent-tab').click(
        function(){
        	if (!flags['flag_tencent']){
        		get_reviews(data_tencent);
        	}  
        }
        );
     
jq('#renren-tab').click(
        function(){
        	if (!flags['flag_renren']){
        		get_reviews(data_renren);
        	}
        }
        );

// 请求开始之前添加旋转图标
var spin_html = '<i class="icon-spinner icon-spin"></i>';

jq('#more-reviews-douban').click(
		function(){
			jq('#more-reviews-douban').prepend(spin_html);
			var reviews = get_reviews_by_offset(data_douban);
		}
		);

jq('#more-reviews-sina').click(
        function(){
        	jq('#more-reviews-sina').prepend(spin_html);
            var reviews = get_reviews_by_offset(data_sina);
        }
        );
        
jq('#more-reviews-tencent').click(
        function(){
        	jq('#more-reviews-tencent').prepend(spin_html);
            var reviews = get_reviews_by_offset(data_tencent);
        }
        );
        
jq('#more-reviews-_renren').click(
        function(){
        	jq('#more-reviews-_renren').prepend(spin_html);
            var reviews = get_reviews_by_offset(data_renren);
        }
        );

// 界面请求处理逻辑
function get_reviews(data){

	return exe_ajax(url_nooffset,data);

}

function get_reviews_by_offset(data){
	
	return exe_ajax(url_offset,data);

}

function exe_ajax(url,data){
	
	// 四个标签页需要分开处理，所以在这里匹配出data参数中的关键字以作为识别标识。
	var reg_exp = RegExp('source\=(\\S+)')
	reg_result = reg_exp.exec(data);
	id = '#' +　reg_result[1] +　'-list-group';
	flag = 'flag_' + reg_result[1];

	jq.ajax({
	    url:url,
	    data:data,
	    dataType:"html",
 	    success:function(data){
 	    		jq(id).append(data);
 	    		// 请求完成之后去掉旋转图标
 	    		jq('.icon-spinner').remove();
 	    		// 设置标志位，只在第一次点开标签页的时候加载初始数据。
 	    		flags[flag] = 1;	
	    },
        error:function(XHRObj,msg,e){
	    	//error_msg = '<p class="error">' +　msg + ": " +　e + '</p>'
	    	error_msg = '<p class="error">' + '抱歉！没有找到相关评论~' + '</p>';
	    	jq(id).append(error_msg);
            // 设置标志位，没有加载出评论时，也不再在每次点开标签时加载数据。
            flags[flag] = 1;
	    } 
	});

}

// 生成评论部分星评
function generate_review_rating(){
    jq('.review_rating').each(
            function(){
                
                var star_num = jq(this).text();
                var star_empty_num = 5 - star_num;

                var star_html = '<span class="icon-star"></span>';
                var star_empty_html = '<span class="icon-star-empty"></span>';
                var tmp_html = ''

                for (i=0; i<star_num; i++){
                    tmp_html += star_html;
                }
                
                for (i=0; i<star_empty_num; i++){
                    tmp_html += star_empty_html;
                }
                
                jq(this).html(tmp_html);
                jq('.review_rating').removeAttr('style');
                jq('.review_rating').removeClass('review_rating');
                
            });
}