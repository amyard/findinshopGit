$.fn.typeahead.Constructor.prototype.render = function (items) {
    var that = this;
    items = $(items).map(function (i, item) {
      i = $(that.options.item).attr('data-value', item);
      i.find('a').html(that.highlighter(item));
      return i[0];
    });
    this.$menu.html(items);
    return this;
};

$(document).ajaxComplete(function(){
    try{
        FB.XFBML.parse();
    }catch(ex){}
});

$(document).ready(function(){
    $('.discount_btn').popover({
        html : true,
        title: function() {
            return $(".discount_title").html();
            },
        content: function() {
            return $(".discount_form").html();
            },
        placement: 'top',
    });

    $('#myCarousel').carousel({
        interval: 6000,
        cycle: true
    });

    $('#myCarousel2').carousel({
        interval: 999000,
        cycle: true
    });

    $('#myCarousel3').carousel({
        interval: 16000,
        cycle: true
    });

    $('.autocomplete_moved').typeahead({
        items: 20,
        source: function (query, process) {
            return $.get(options.search_autocomplete_url, { 'q': $("#autocompleteForm input:last").val() }, function (data) {
                return process(data.options);
            });
        }
    });

    $.endlessPaginate({
        paginateOnScroll: true,
        paginateOnScrollMargin: 300
    });
});

function add_subscriber(){
       $.ajax({
            type:"POST",
            url: options.add_subscriber_url,
            data: {
                'csrfmiddlewaretoken': $("#subscribeForm input:first").val(),
                'email': $("#subscribeForm input[name='email']").val(),
            },
            success: function(answer){
                $(".answer").val('')
                $(".answer").attr('placeholder', answer)
            }
        });
    }

function get_installment_custom(partner, product_id, product_name, product_price) {
    if (product_price.indexOf(',') != -1) {
            product_price=product_price.replace(",", ".");
    }
    get_installment(partner=partner, product_id=product_id, product_name=product_name, product_price=product_price);
}

var OPTIONS = OPTIONS || (function(){
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
                        return "<img title=" + this.name + " alt=" + this.name + " src=" + this.image_url + ">";
                      }
                    },
                    price: {
                        html: function() {
                        return "Цена: " + Math.round(this.price*100)/100 + " грн.";
                      }
                    },
                    url: {
                        html: function() {
                        return "<a href=" + this.url + " class='btn btn-inverse' target='_blank'>На сайт продавца</a>";
                      }
                    },
                    installment: {
                        html: function() {
                        return "<a href='javascript:void(0);' product_id='" + this.id + "' product_name='" + this.name + "' product_price='" + this.price + "' class='btn installment_btn'>Купить в рассрочку</a>";
                      }
                    },
                };
                $(".modal").render(data, directives);
                $(".installment_btn").click(function(){
                    get_installment(partner='1', product_id=$(this).attr('product_id'), product_name=$(this).attr('product_name'), product_price=$(this).attr('product_price'));
                });
                $(".modal").modal({backdrop: false, show:true}).css({
                    width: '800',
                    'margin-left': function () {
                        return -($(this).width() / 2);
                    }
                });
            })
            return false;
        },
        init_slider: function () {
            min_price = 1500
            max_price = 15000
            if ($("input[name=min_price]").val()) {min_price = $("input[name=min_price]").val()};
            if ($("input[name=max_price]").val()) {max_price = $("input[name=max_price]").val()};
            $('#slider').rangeSlider({
                bounds:{min: options.bound_min, max: options.bound_max},
                defaultValues:{min: min_price, max: max_price},
            });
            $("#slider").on("valuesChanging", function(e, data){
                $("input[name=min_price]").val(Math.round(data.values.min))
                $("input[name=max_price]").val(Math.round(data.values.max))
            });
        },
    };
}());
