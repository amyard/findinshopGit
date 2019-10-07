$(function () {

    $(".button").click(function(){
        $.get("/w/filter-setting/");
        if($("#filter_check").hasClass("check")){
            $(".banners").hide();
            $(".main").addClass('full_width');
            $("#filter_check").removeClass("check");
        } else {
            $("#filter_check").addClass("check");
            $(".banners").show();
            $(".main").removeClass('full_width');
        }
    });

    $("#spoiler_check").click(function(){
        if($("#spoiler_check").hasClass("check"))
        {
            $(".sp_check").attr("src", "/static/themes/findinshop/red/img/bottom_arrow.png");
            $("#spoiler_check").removeClass("check");
        } else {
            $(".sp_check").attr("src", "/static/themes/findinshop/red/img/top_arrow.png");
            $("#spoiler_check").addClass("check");
        }
    });

    $("#spoiler_check_shop").click(function(){
        if($("#spoiler_check_shop").hasClass("check"))
        {
            $(".minus").attr("src", "/static/themes/findinshop/red/img/plus.png");
            $("#spoiler_check_shop").removeClass("check");
            $("#spoiler_check_shop").next().hide();
        } else {
            $(".minus").attr("src", "/static/themes/findinshop/red/img/minus.png");
            $("#spoiler_check_shop").addClass("check");
            $("#spoiler_check_shop").next().show();
        }
    });

    $("#spoiler_check_brend").click(function(){
        if($("#spoiler_check_brend").hasClass("check"))
        {
            $(".minus2").attr("src", "/static/themes/findinshop/red/img/plus.png");
            $("#spoiler_check_brend").removeClass("check");
            $("#spoiler_check_brend").next().hide();
        } else {
            $(".minus2").attr("src", "/static/themes/findinshop/red/img/minus.png");
            $("#spoiler_check_brend").addClass("check");
            $("#spoiler_check_brend").next().show();
        }
    });

    $("#spoiler_check_type").click(function(){
        if($("#spoiler_check_type").hasClass("check"))
        {
            $(".minus3").attr("src", "/static/themes/findinshop/red/img/plus.png");
            $("#spoiler_check_type").removeClass("check");
            $("#spoiler_check_type").next().hide();
        } else {
            $(".minus3").attr("src", "/static/themes/findinshop/red/img/minus.png");
            $("#spoiler_check_type").addClass("check");
            $("#spoiler_check_type").next().show();
        }
    });

    $("#spoiler_check_condition").click(function(){
        if($("#spoiler_check_condition").hasClass("check"))
        {
            $(".minus4").attr("src", "/static/themes/findinshop/red/img/plus.png");
            $("#spoiler_check_condition").removeClass("check");
            $("#spoiler_check_condition").next().hide();
        } else {
            $(".minus4").attr("src", "/static/themes/findinshop/red/img/minus.png");
            $("#spoiler_check_condition").addClass("check");
            $("#spoiler_check_condition").next().show();
        }
    });

    $("#spoiler_check_color").click(function(){
        if($("#spoiler_check_color").hasClass("check"))
        {
            $(".minus5").attr("src", "/static/themes/findinshop/red/img/plus.png");
            $("#spoiler_check_color").removeClass("check");
            $("#spoiler_check_color").next().hide();
        } else {
            $(".minus5").attr("src", "/static/themes/findinshop/red/img/minus.png");
            $("#spoiler_check_color").addClass("check");
            $("#spoiler_check_color").next().show();
        }
    });

     $("#spoiler_check_gender").click(function(){
        if($("#spoiler_check_gender").hasClass("check"))
        {
            $(".minus5").attr("src", "/static/themes/findinshop/red/img/plus.png");
            $("#spoiler_check_gender").removeClass("check");
            $("#spoiler_check_gender").next().hide();
        } else {
            $(".minus5").attr("src", "/static/themes/findinshop/red/img/minus.png");
            $("#spoiler_check_gender").addClass("check");
            $("#spoiler_check_gender").next().show();
        }
    });

    $(".one_of_filter").click(function(){
        var self = $(this);
        if(self.hasClass("check"))
        {
            self.prev().children().attr("src", "/static/themes/findinshop/red/img/plus.png");
            self.removeClass("check");
            self.next().hide();
        } else {
            self.prev().children().attr("src", "/static/themes/findinshop/red/img/minus.png");
            self.addClass("check");
            self.next().show();
        }
    });



});
