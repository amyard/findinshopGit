$(function(){
  getSize();
  toggleFilterHeader();
  setHeaderToFixed();
  thumbSlider();
  // $("#id_phone").mask("+(999)999-99-99");
});

$(window).resize(function(){
  getSize();
  setHeaderToFixed();
});

function getSize() {
  var h = $(window).innerHeight();
  $(".main-search").css({
    height: (h - $(".header").innerHeight()) + "px"
  })
}

function toggleFilterHeader() {
  $(document).on("click", ".filter-header", function(ev){
    ev.preventDefault();
    $(this).addClass("toggled");
    $(this).next().slideUp();
  });

  $(document).on("click", ".toggled", function(ev){
    ev.preventDefault();
    $(this).removeClass("toggled");
    $(this).next().slideDown();
  });
}

function setHeaderToFixed() {
  $(window).scroll(function() {
    var a = $(window).scrollTop();
    if(viewport().width > 767) {
      if (a > $(".header").innerHeight()) {
        $(".header").css({
          position: "fixed",
          boxShadow: "0 1px 3px 0 rgba(42,48,60,.19)"
        },1000);

      }
      else {
        $(".header").css({
          position: "relative",
          boxShadow: "none"
        });
      }
    }

    if(viewport().width < 768) {
      if (a > $(".header").innerHeight()) {
        $(".header").css({
          position: "fixed",
          boxShadow: "0 1px 3px 0 rgba(42,48,60,.19)",
        },1000);
        $(".header_logo").hide();

      }
      else {
        $(".header").css({
          position: "relative",
          boxShadow: "none"
        });
        $(".header_logo").show();
      }
    }

  });
}

function thumbSlider() {
  $(document).on("click", ".thumbs_ul li a", function(){
    $(this).closest(".thumbs_ul").find(".active").removeClass("active");
    $(this).addClass("active");
    var src = $(this).find("img").attr("src");
    $(".compare-original_box .box_img img").attr("src", src);
  });
}

function viewport()
{
  var e = window, a = 'inner';
  if (!('innerWidth' in window))
  {
    a = 'client';
    e = document.documentElement || document.body;
  }
  return {width: e[ a + 'Width' ], height: e[ a + 'Height' ]}
}
