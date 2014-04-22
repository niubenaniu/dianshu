$('#bcode-img').pin();
$('#about').tooltip();
$('#article-dialog').on('shown.bs.modal', function (e) {
    console.log(jQuery(e.relatedTarget).attr('ttt'));
});