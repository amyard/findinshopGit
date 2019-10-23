// HEADER SOCIAL LINKS DISPLAY AFTER CLICKIG ON MAN HEAD
jQuery(document).ready(function(){
    $('#social-links-0').click(function() {
        $('#social-links-1').show();
        $('#social-links-0').hide();
    });
});


// ПОЛНОЕ ОПИСАНИЕ ТОВАРА - НАЖИМАТЬ НА КНОПКУ "ЕЩЕ"
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


// ТАБУЛЯЦИЯ
$(document).on('click', '.nav-tabs li', function (){
    if ($(this).find('a').attr('aria-controls') == 'discount') {
        $('.coupon-btn').css({'display':'block'});
        $('.shop-btn').css({'display':'none'});
    } else {
        $('.coupon-btn').css({'display':'none'});
        $('.shop-btn').css({'display':'block'});
    }
});



// ЗАКРЫТЬ ОПИСАНИЕ ТОВАРА
$(document).on('click', '.full-description__close--btn', function() {
  var windowWidth = $(window).width();
  if(windowWidth <= 1024) {
      $('#descModal').css({'display':'none'});
  } else {
      $('.full-description').css({'display':'none'});
  }
});



// TODO - ПЕРЕЛЕДАТЬ. ПОПАТ ДОЛЖНЕ С ВЫСОТЫ 1024px
$(window).on('resize', function(){
  wdRes = $(window).width()
  if (wdRes <= 480) {
      $('.full-description').css({'display':'none'});
  }
})



// функция возвращает сколько елементов (блоков с продуктами) в строке
function posInline() {
  blockWidth = $('.catalog-block').width();
  // работает
  itemWidth = $('.full-description').length != 0 && $('.full-description').width() != 100 ? $('.full-description').next().width() : $('.product-item').width()
  res =  Math.ceil( blockWidth / itemWidth ) - 1;

  // itemWidth = $('.full-description').length != 0 ? $('.full-description').next().width() : $('.product-item').width()
  // floatPart  = (blockWidth / itemWidth) - Math.round( blockWidth / itemWidth );
  // res = floatPart >=0.5 ? Math.ceil( blockWidth / itemWidth ) - 1 : Math.ceil( blockWidth / itemWidth ) - 2;
  return res
}


function addDescBlock(){
  return `\
    <div class="full-description full-description-desctop">\
      <div class="full-description__content">\
          <div class="full-description__content--img"> <img alt="" src="https://www.ttt.ua/uploads/shop/products/large/c_09ba42aaf4e9b85a2a25349654b47a21.jpg"> </div>\
          <div class="full-description__content--info">\
              <div>\
                  <div class="full-description__close">\
                      <h3>Рюкзак для ноутбука Dell Alienware Vindicator 2.0 17 Bp (460-BCBT)</h3> <span class="full-description__close--btn close">×</span> </div>\
                  <ul class="nav nav-tabs" role="tablist">\
                      <li class="active"><a href="#product" aria-controls="product" role="tab" data-toggle="tab">Продукт</a></li>\
                      <li><a href="#shop" aria-controls="shop" role="tab" data-toggle="tab">Магазин</a></li>\
                      <li class="discount-btn" style="display: block"><a href="#discount" aria-controls="discount" role="tab" data-toggle="tab">Купон на скидку</a></li>\
                  </ul>\
                  <div class="tab-content">\
                      <div role="tabpanel" class="tab-pane tab-pane-new active" id="product" style="height: 220px;">\
                          <h2 class="price-btn no-pad-top">Цена: <span>3599.00</span></h2>\
                          <div class="general-content-here">\
                              <p>Рюкзак для ноутбука Dell Alienware Vindicator 2.0 17 Bp (460-BCBT) Рюкзак для ноутбука Dell Alienware Vindicator 2.0 17 Bp (460-BCBT)Рюкзак для ноутбука Dell Alienware Vindicator 2.0 17 Bp (460-BCBT)Р<span class="lalal hdd" style="display:none">юкзак для ноутбука Dell Alienware Vindicator 2.0 17 Bp (460-BCBT)Рюкзак для ноутбука Dell Alienware Vindicator 2.0 17 Bp (460-BCBT)Рюкзак для ноутбука Dell Alienware Vindicator 2.0 17 Bp (460-BCBT)Рюкзак для ноутбука Dell Alienware Vindicator 2.0 17 Bp (460-BCBT)Рюкзак для ноутбука Dell Alienware Vindicator 2.0 17 Bp (460-BCBT)Рюкзак для ноутбука Dell Alienware Vindicator 2.0 17 Bp (460-BCBT)Рюкзак для ноутбука Dell Alienware Vindicator 2.0 17 Bp (460-BCBT)Рюкзак для ноутбука Dell Alienware Vindicator 2.0 17 Bp (460-BCBT)</span></p> <span class="more-btn" style="display: block">Еще</span>\
                          </div>\
                          <div class="product-item--stars d-flex marg-y-24 d-none">\
                              <div id="delta">0</div>\
                          </div>\
                          <span class="product-item--old-price d-block">1999 грв</span>\
                      </div>\
                      <div role="tabpanel" class="tab-pane tab-pane-new" id="shop" style="height: 220px;">\
                          <h2 class="price-btn no-pad-top">Цена: <span>3599.00</span></h2>\
                          <table>\
                              <tbody>\
                                  <tr>\
                                      <td class="table-grey">Название магазина</td>\
                                      <td class="table-black"><a href="/c/map/stores/70/" target="_blank">Магазины и пункты выдачи</a> | <a href="/bid/transition/1141864/" class="popup-store" rel="nofollow" target="_blank">delmetest</a></td>\
                                  </tr>\
                                  <tr>\
                                      <td class="table-grey">Доставка</td>\
                                      <td class="table-black">Нет</td>\
                                  </tr>\
                                  <tr>\
                                      <td class="table-grey">Способ оплаты</td>\
                                      <td class="table-black">Нет</td>\
                                  </tr>\
                                  <tr>\
                                      <td class="table-grey">Контактный телефон</td>\
                                      <td class="table-black">343434343</td>\
                                  </tr>\
                              </tbody>\
                          </table> <span class="product-item--old-price d-block">1999 грв</span> </div>\
                      <div role="tabpanel" class="tab-pane tab-pane-new" id="discount" style="height: 220px;">\
                          <h2 class="price-btn no-pad-top">Цена: <span>3599.00</span></h2>\
                          <div class="discount">\
                              <p class="orange-color">50%</p>\
                              <p>Действителен до 31.10.2019 14:59</p>\
                          </div>\
                          <form class="header__search-form modal-input-form" method="GET" id="id_form_get_coupon">
                              <div class="input-group">\
                                  <input id="id_name" class="header__search-input modal-input" type="text" placeholder="Введите Ваше имя" name="name">\
                                  <input id="id_email" class="header__search-input modal-input" type="email" placeholder="Введите Вашу почту" name="email">\
                                  <input type="hidden" name="coupon" value="7" id="coupon_id">\
                                  <input type="hidden" name="item" value="1141864" id="product_id">\
                              </div>\
                              <input type="submit" id="check_coupon_form" value="ОТПРАВИТЬ">\
                          </form>\
                      </div>\
                  </div>\
              </div>\
          </div>\
      </div>\
      <div class="full-description__footer"> <img src="" alt="" class="svg-icon d-none" onclick="wishlist( 1141864 )" id="wish" target="_blank"> <img src="" alt="" class="d-none"> <a class="orange-btn-cs orange-btn-padding-cs shop-btn" href="/bid/transition/1141864/" id="redirect-popup-button" target="_blank">В МАГАЗИН</a> <a class="orange-btn-cs orange-btn-padding-cs coupon-btn">ОТПРАВИТЬ</a> </div>\
  </div>\
  `
}


// номер активного дива в списке всех блоков с продуктами
function getPositionOfItemBlock() {
  var allItems = $('.catalog-block_li .item_img').parent().parent()
  $.each(allItems, function(dt, value) {
      var innerBtnClass = jQuery(value).find('.full-desc').attr('class');
      innerBtnClass.includes('active')
          ? correctItem = dt+1
          : null
  })
  return correctItem
}


// кнопка активная и екран меньше 1024px то показываем модал
// function displayModal(){
//   $('.full-desc .active') && $(window).width()<=1024
//     ? $('#descModal').css({'display':'block'})
//     : null
// }

// displayModal()





function allMagicWithAddingDescBlock(){
  allItems = $('.catalog-block_li')
  getPositionInline = posInline()
  var activeBtn = $('.full-desc .active')
  var parentDiv = activeBtn.parent().parent().parent().parent()
  var positionOfItem = getPositionOfItemBlock();

  // после какого елемента нужно вставить наш див
  // жопа с посленим рядом. для него надо делать проверку на количество елементов
  var getDivAfterInsert = Math.ceil(correctItem / getPositionInline) * getPositionInline;


  if(allItems.length < getDivAfterInsert) {
    currDiv = allItems.last()
  } else {
    console.log('getDivAfterInsert', getDivAfterInsert)
    currDiv = allItems[getDivAfterInsert-1];
  }

  jQuery(currDiv).after(addDescBlock())
}



// ПОДРОБНЕЕ - главная фигня
$(document).on('click', '.full-desc', function(event){
    event.preventDefault();

    var windowWidth = $(window).width(),
        allItems = $('.catalog-block_li'),
        getPositionInline = posInline();

    $('.full-desc').removeClass('active');
    
    windowWidth > 1024 ? $('.full-description-desctop').remove() : null

    if(!$(this).attr('class').includes('active')){
        $(this).addClass('active')

        // показываем простой блок или модалку
        if (windowWidth > 1024) {
          allMagicWithAddingDescBlock()
        } else {
          $('body').css({'overflow':'hidden'})
          $('#descModal').css({'display':'block'})
        }
        
    }
});



$('body').on('click', '#descModal .close', function(){
  $('body').css({'overflow':'auto'})
  $('.filter__item').css({'display':'none'})
  $('#descModal').css({'display':'none'})
});


// TODO - ПЕРЕЛЕДАТЬ. ПОПАТ ДОЛЖНЕ С ВЫСОТЫ 1024px
oldPos = posInline()

$(window).on('resize', function(){

  allItems = $('.product-item')
  currPos = posInline();
  var windowWidth = $(window).width();

  // FIRST DESCTOP VERSION.     SECOND - MODAL
  if(windowWidth > 1024){

    // from modal to desctop
    if($('#descModal').css('display')=='block'){

      console.log('REMOVE MODAL FROM RESIZE')
      $('#descModal').css({'display':'none'});
      // allMagicWithAddingDescBlock();

      $('body').css({'overflow':'auto'})
      $('.full-description-desctop').css({'display':'block'})

    } else {
      if (oldPos != currPos) {
        // мы уменьшаем размер екрана
        if ($('.full-desc .active') && oldPos > currPos && oldPos != Infinity) {
    
          console.log('Уменьшили')
          prevElementHtml = $('.full-description-desctop').prev().html()
          jQuery($('.full-description-desctop')).after('<div class="catalog-block_li product-item inserted_js"></div>')
          $('.inserted_js').html(prevElementHtml)
          $('.inserted_js').removeClass('inserted_js')
          $('.full-description-desctop').prev().remove()
        } else if ($('.full-desc .active') && oldPos < currPos && oldPos != Infinity) {

          console.log('Увеличили')
          beforeElementHtml = $('.full-description-desctop').next().html()       
          jQuery($('.full-description-desctop')).before('<div class="catalog-block_li product-item inserted_js"></div>')
          $('.inserted_js').html(beforeElementHtml)
          $('.inserted_js').removeClass('inserted_js')
          $('.full-description-desctop').next().remove()
        }
        
        oldPos = currPos;
      }
    }

    

    // при переходе из модала в норм состояние
    // if ($('.full-desc .active')) {
    //   $('body').css({'overflow':'auto'})
    //   $('.full-description-desctop').css({'display':'block'})
    //   allMagicWithAddingDescBlock();
    // }
  } else {
    if ($('.full-desc.active').length == 1) {
      console.log('MODAL FROM RESIZE')
      $('.full-description-desctop').css({'display':'none'})
      $('#descModal').css({'display':'block'})
      $('.full-description-modal').css({'display':'block'})
    }
    
    oldPos = currPos;
  }  
  
})























// ФУЙНЯ ДЛЯ TOOGLE В ФИЛЬТРАХ - СПИЗДИЛ С САЙТА ПОЛНОСТЬЮ
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