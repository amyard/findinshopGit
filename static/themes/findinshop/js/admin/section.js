(function ($) {
    $(document).ready(function ($) {
        $('#id_parse_url').parent().append('<button class="addlink btn btn-high" style="margin-left: 10px;">Спарсить</button>');
        $('button.addlink').click(function (e) {
            var _this = $(this);
            var url = '/section/parse-section/parse';
            var parse_url = {parse:$('#id_parse_url').val(),
            section_id: document.location.pathname.replace('/admin/section/section/', '').replace('/', '')};
            $(_this).attr("disabled", "disabled");
            $.get(url, parse_url, function (data) {
                if(data=='failure'){
                    $(_this).removeAttr("disabled");
                }else{
                    alert("Парсер запущен");
                }

            });
            return false;
        });
    });
})(django.jQuery);