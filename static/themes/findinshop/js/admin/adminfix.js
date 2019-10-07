(function ($) {
    $(document).ready(function ($) {
        var disable_id = document.location.href.match(/\/(\d+)\//);
        if (disable_id) {
            $('.save-box').append('<button href="/c/im/d/' +
                disable_id[1] +
                '" class="btn btn-high btn-danger disable_parse">Приостановить</button>');
        }
        var tr = $("#result_list").find('tr');
        for (i = 1; i < tr.length; i++) {
            var id = $($(tr[i]).find('a')[0]).attr('href').match(/\/(\d+)\//)[1];
            var status = $($(tr[i]).find('td')[4]).text();
            if (status == 'Выполнен' || status == 'Ошибка выполнения') {
                $(tr[i]).append('<td><button href="/c/im/r/' + id + '/" class="addlink">Перезапуск</button></td>');
            }
            if (status == 'Обрабатывается' || status == 'Принят') {
                $(tr[i]).append('<td><button href="/c/im/s/' + id + '/" class="stopParser">Остановить</button></td>');
            }

        }
        $('button.addlink').click(function (e) {
            var _this = $(this);
            var url = _this.attr('href');
            $.get(url, id, function (data) {
                alert("Парсер перезапущен");
                $(_this).attr("disabled", "disabled");
                var tds = $(_this).parent().parent().find('td');
                $(tds[2]).text(data.start);
                $(tds[3]).text(data.end);
                $(tds[4]).text(data.status);
            });
            return false
        })
        $('button.stopParser').click(function (e) {
            var _this = $(this);
            var url = _this.attr('href');
            $.get(url, id, function (data) {
                alert("Парсер перезапущен");
                $(_this).attr("disabled", "disabled");
                var tds = $(_this).parent().parent().find('td');
                $(tds[2]).text(data.start);
                $(tds[3]).text(data.end);
                $(tds[4]).text(data.status);
            });
            return false
        })
        $('button.disable_parse').click(function (e) {
            var _this = $(this);
            var url = _this.attr('href');
            $.get(url, id, function (data) {
                alert("Парсер приостановлен");
                $("#id_status").val(4);
            });
            return false
        })
    });
})(django.jQuery);