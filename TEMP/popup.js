$(function () {
    //script for popups
    $('a.close').live('click', function(){
        $(this).parent().fadeOut(100);
        $('#overlay').remove('#overlay');
        $('#product-detail-container').hide();
        $('#product-detail-container-data').hide();
        $('#social-container').hide();
        return false;
    });

    //script for tabs
    $("#myTabs a").live('click', function(){
        var $redirect_btn = $('#redirect-popup-button');
        $redirect_btn.attr('href', $(this).data('button-url'));
        $redirect_btn.removeClass('submit-coupon-js').removeClass('product-coupon-js');
        $('#id_form_get_coupon').hide();
        if ($(this).data('button-id') == 'id_product_bid') {
            $redirect_btn.text('СРАВНИТЬ ЦЕНЫ');
        } else if ($(this).data('button-id') == 'id_product_cupon') {
            $redirect_btn.text('ПОЛУЧИТЬ КУПОН').addClass('product-coupon-js');
        } else {
            $redirect_btn.text('В МАГАЗИН');
        }
        //$redirect_btn.attr('id', $(this).data('button-id'));

        /*$(".lineTabs li").removeClass("active");
        $(this).parent().addClass("active");
        $(".tab_content div").stop(false,false).hide();
        $(".tab"+$(this).data('tab')).stop(false,false).fadeIn(300);*/
        return false;
    });

    $('.product-coupon-js').live('click', function(e){
        e.preventDefault();
        $('#redirect-popup-button').text('ОТПРАВИТЬ').addClass('submit-coupon-js');
        $('#id_form_get_coupon').show();
        return false;
    });

    $('.submit-coupon-js').live('click', function(e){
        e.preventDefault();
        var $that = $(this);
        $(this).text('Sending...');
        var post_data = $('#id_form_get_coupon').serialize();
        $.ajax({
            "type": "POST",
            "dataType": "json",
            "url": "/w/validate_coupon_form/",
            "data": post_data,
            "success": function(result) {
                $that.text('ОТПРАВИТЬ');
                if (result['status'] == 'ok'){
                    $('#id_form_get_coupon').html('<p>Код купона для покупки товара в магазине «'+result['store_name']+'» был выслан на указанный электронный адрес');
                } else {
                    alert('Wrond data');
                }
            }
        });
        return false;
    })

});
