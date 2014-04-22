//<![CDATA[       
 
 $(document).ready(function () { 
	 // 初始化cleditor
	 var editor = $("#content").cleditor();
	 //console.log(editor.blurred());
	 /*editor.blurred(function(){
		 alert(0);
	 }
	 );*/
	 // 表单字段空验证
	 $("#title").blur(function(){
	     if($('#title').val() == ''){
	         $('#title').parent().parent().addClass('has-error');
         }else{
        	 $('#title').parent().parent().removeClass('has-error');
         }
	 }
	 );
	 
/* 	 $("#content").blur(function(){        
	     if($('#content').val() == ''){
	         $('#content-area').addClass('has-error');
	     }else{
	    	 $('#content-area').removeClass('has-error');
	     }
     }
     ); */
	 
	 // 文章预览
	 $('#preview-button').click(function(e){
		 e.preventDefault();

	     var date = new Date();
	     var publish_date = date.getFullYear() + '年' + date.getMonth() + '月' + date.getDay() + '日 ' + 
	                    date.getHours() + ':' + date.getMinutes();
         
	     // 表单字段空验证
	     if($('#title').val() == ''){
	    	 $('#title').parent().parent().addClass('has-error');
	     }
	     
	     if($('#content').val() == ''){   
	    	 $('#content-area').addClass('has-error');
	         }
	               
	     $('#preview-title').text($('#title').val());
	     $('#preview-date').text(publish_date);
	     $('#preview-content').html(editor[0].$area[0].value);
	     
	     if($('#title').val() != '' && $('#content').val() != ''){
	    	 $('#article-dialog').modal('show');
	     }
	 }		 
	 );
	 
	 // 文章发布
	 $('form').submit(function(e){
	     // 表单字段空验证
         if($('#title').val() == ''){
             $('#title').parent().parent().addClass('has-error');
         }
         
         if($('#content').val() == ''){   
             $('#content-area').addClass('has-error');
             }
         if($('#title').val() == '' || $('#content').val() == ''){
        	 // 如果发现表单必选字段有空，则停止提交
        	 e.preventDefault();
         }     
	 }		 
	 );
 });
//]]>