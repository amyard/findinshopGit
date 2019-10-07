$(function(){
    $("#id_name").keyup(function(){
        var e = $("#id_slug");
        e.val(URLify($(this).val(), 200));
    });
});
