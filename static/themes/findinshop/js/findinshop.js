$(document).ajaxComplete(function(){
    // Facebook like button fix
    try{
        FB.XFBML.parse();
    }catch(ex){}
    // End Facebook like button fix

    // Installment processing
    $("a.installment_btn").each(function(event){
        $(this).click(function(){
            get_installment(partner='1', product_id=$(this).attr('product_id'), product_name=$(this).attr('product_name'), product_price=$(this).attr('product_price'), product_url=$(this).attr('product_url'));
        });
    });    
    // End installment processing    
});

$(function() {
    // Django endless pagination
    $.endlessPaginate({
        paginateOnScroll: true,
        paginateOnScrollMargin: 300
    });
    // End Django endless pagination

    // Popup with item info
    $(".close").click(function(){
        $("body").removeClass("noscroll");
        $(".b-popup-overlay").removeClass("active");
        $("#wrapper-info").removeClass("active");
        //window.location.hash="";
        history.pushState("", document.title, window.location.pathname + window.location.search);
    });

    $("a[data-toggle='tab']").click(function(){
        sel = $(this).attr('href');
        $("div[id^='tab_']").hide();
        $(sel).show();
        $("ul.nav.nav-tabs").children('li').removeClass('active');
        $(this).parent('li').addClass('active');
    });
    // End Popup with item info
});

function fallback_image(image){
    image.src = '/static/img/img404.jpg';
}

function get_installment_custom(partner, product_id, product_name, product_price) {
    if (product_price.indexOf(',') != -1) {
        product_price=product_price.replace(",", ".");
    }
    get_installment(partner=partner, product_id=product_id, product_name=product_name, product_price=product_price);
}

var SEARCH = SEARCH || (function(){
    var options = {};
    return {
        init : function(args) {
            options = args;
        },
        display_box: function(item) {
            $.get(options.get_item_info_url,{'item':item}, function(data){
                directives = {
                    image_url: {
                      html: function() {
                        return '<img class="info-image" title="' + this.name + '" alt="' + this.name + '" src="' + this.image_url + '" onError="fallback_image(this);">';
                      }
                    },
                    price: {
                        html: function() {
                        return this.price + ' ' + this.currency + '.';
                      }
                    },
                    url: {
                        html: function() {
                        return '<a href="' + this.url +'" target="_blank" class="btn" onclick="yaCounter21259801.reachGoal('+"'GO_TO_SELLER'"+'); return true;">На сайт продавца</a>';
                      }
                    },
                    installment: {
                        html: function() {
                        return "<a href='javascript:void(0);' onclick="+'"yaCounter21259801.reachGoal('+"'INSTALLMENT'"+'); return true;"' + " product_id='" + this.id + "' product_name='" + this.name + "' product_price='" + this.price + "' product_url='" + this.url + "' class='installment_btn green'>Взять в рассрочку</a>";
                      }
                    },
                    fb: {
                        html: function() {
                        return '<div class="fb-like" style="" data-href="' + this.url +'" data-send="false" data-layout="button_count" data-width="450" data-show-faces="true"></div>';
                      }
                    },
                };
                $("#wrapper-info").render(data, directives);
                $("body").addClass("noscroll");
                $(".b-popup-overlay").addClass("active");
                $("#wrapper-info").addClass("active");
            })
            return false;
        },
    };
}());
