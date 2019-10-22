
jQuery(document).ready(function(){
    $('#social-links-0').click(function() {
        $('#social-links-1').show();
        $('#social-links-0').hide();
    });
});


$(document).on('click', '.more-btn', function(){
    cls = $('.general-content-here span').attr('class')
    if(cls.includes('hdd')) {
        $('.general-content-here span').removeClass('hdd')
        $('.general-content-here span').addClass('shwd')
        $('.general-content-here .more-btn').html('Cвернуть')
        $('.general-content-here .lalal').css({'display':'inline'})
    } else {
        $('.general-content-here span').removeClass('shwd')
        $('.general-content-here span').addClass('hdd')
        $('.general-content-here .more-btn').html('Еще')
        $('.general-content-here .lalal').css({'display':'none'})
    }
})


$(document).on('click', '.nav-tabs li', function (){
    if ($(this).find('a').attr('aria-controls') == 'discount') {
        $('.coupon-btn').css({'display':'block'});
        $('.shop-btn').css({'display':'none'});
    } else {
        $('.coupon-btn').css({'display':'none'});
        $('.shop-btn').css({'display':'block'});
    }
});