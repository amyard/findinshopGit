
// ПОЛНОЕ ОПИСАНИЕ ТОВАРА - НАЖИМАТЬ НА КНОПКУ "ЕЩЕ"
$(document).on('click', '.more-btn', function(event){
  event.stopPropagation()
  parentName = $(this).parent().parent().parent();
  cls = jQuery(parentName).find('.general-content-here span').attr('class')
  if(cls.includes('hdd')) {
      jQuery(parentName).find('.general-content-here span').removeClass('hdd')
      jQuery(parentName).find('.general-content-here span').addClass('shwd')
      jQuery(parentName).find('.general-content-here .more-btn').html('Cвернуть')
      jQuery(parentName).find('.general-content-here .lalal').css({'display':'inline'})
  } else {
      jQuery(parentName).find('.general-content-here span').removeClass('shwd')
      jQuery(parentName).find('.general-content-here span').addClass('hdd')
      jQuery(parentName).find('.general-content-here .more-btn').html('Еще')
      jQuery(parentName).find('.general-content-here .lalal').css({'display':'none'})
  }
})


//////////////////////////////////////////////////////////////////////////////////////
//            tabulation
//////////////////////////////////////////////////////////////////////////////////////
$(document).on('click', '.nav-tabs li', function (event){
  event.preventDefault();

  var couponSettUrl = $('.catalog-block').attr('data-id'),
      couponSettings = getAjaxData(couponSettUrl).res;
  choosePhoneEmailFieldForCouponSystem(couponSettings)

  $('.nav-tabs li').removeClass('active');
  $('.tab-pane').removeClass('active');
  var newId = $(this).find('a').attr('aria-controls')
  $(this).addClass('active');
  $(`#${newId}`).addClass('active');
  $('.modal-footer .orange-btn').html('В магазин');

  var trWidth = $('.tab-content').width() / 2;
  $('.full-description table td').css({'width': trWidth})

  if ($(this).find('a').attr('aria-controls') == 'discount') {
      $('#id_phone').mask('+(999)99-99-99?99')
      $('.coupon-btn').css({'display':'block'});
      $('.shop-btn').css({'display':'none'});
  } else {
      $('.coupon-btn').css({'display':'none'});
      $('.shop-btn').css({'display':'block'});
  }
});

$(document).on('click', '.coupon-btn', function(event){
    event.preventDefault();
    $('#check_coupon_form').click();
});

function choosePhoneEmailFieldForCouponSystem(couponSettings) {
  if(couponSettings) {
      $('.modal-input-form #id_phone').css({'display':'block'})
      $('.modal-input-form #id_email').css({'display':'none'})
  } else {
      $('.modal-input-form #id_phone').css({'display':'none'})
      $('.modal-input-form #id_email').css({'display':'block'})
  }
}


function getAjaxData(url) {
  var result="";
  $.ajax({
      url:url, async: false, success:function(data) {  result = data;  }
  });
  return result;
}


// ЗАКРЫТЬ ОПИСАНИЕ ТОВАРА
$(document).on('click', '.full-description__close--btn', function() {
  var windowWidth = $(window).width();
  if(windowWidth <= 1024) {
      $('#descModal').css({'display':'none'});
  } else {
      $('.full-description').css({'display':'none'});
  }
  removeActiveCssStyles($('.full-desc.active'));

  // псле с большего екрана где есть актив на мелкий, то появляется попут и после закрытия фигня остается на бывшем активном. чистка  
  if($('.icon.active').attr('class').includes('inline') && $('.product-item--inline-bigger').length != 0) {
    $('.product-item--inline-bigger').find('.full-description__close--btn').remove();
    $('.product-item--inline-bigger').find('.more-btn').remove();
    $('.product-item--inline-bigger').find('.full-description__footer').remove();
    $('.product-item--inline-bigger').remove();
  }
});



// функция возвращает сколько елементов (блоков с продуктами) в строке
function posInline() {
  blockWidth = $('.catalog-block').width();
  // работает
  itemWidth = $('.full-description').length != 0 && $('.full-description').width() != 100 ? $('.full-description').next().width() : $('.product-item').width()
  res =  Math.ceil( blockWidth / itemWidth ) - 1;

  // когда количество елентов в строке 11, то показует результат через функцию 12. убираем на 1
  corrRes = res > 10 ? res - 1 : res
  return corrRes
}


function addDescBlock(data, couponExists, moreBtnDisplay){
  return `\
    <div class="full-description full-description-desctop">\
      <div class="full-description__content">\

          <div class="full-description__content--img"> \
            <img alt="" src="${data.image_url}"> \
          </div>\

          <div class="full-description__content--info">\
              <div>\
                  <div class="full-description__close">\
                      <h3>${data.name}</h3> \
                      <span class="full-description__close--btn close">×</span>\
                  </div>\
                  <ul class="nav nav-tabs" role="tablist">\
                      <li class="active"><a href="#product" aria-controls="product" role="tab" data-toggle="tab">Продукт</a></li>\
                      <li><a href="#shop" aria-controls="shop" role="tab" data-toggle="tab">Магазин</a></li>\
                      <li class="discount-btn" style="display: ${couponExists}"><a href="#discount" aria-controls="discount" role="tab" data-toggle="tab">Купон на скидку</a></li>\
                  </ul>\
                  <div class="tab-content">\
                      <div role="tabpanel" class="tab-pane tab-pane-new active" id="product" style="height: 220px;">\
                          <h2 class="price-btn no-pad-top">Цена: <span>${data.price}</span></h2>\
                          
                          <div class="general-content-here">\
                            <p>${data.description_short}<span class='lalal hdd' style='display:none'>${data.description_full}</span></p>\
                            <span class='more-btn' style="display: ${moreBtnDisplay}">Еще</span>
                          </div>\
                          
                          <div class="product-item--stars d-flex marg-y-24 d-none">\
                              <div id="delta">0</div>\
                          </div>\
                          <span class="product-item--old-price d-block">1999 грв</span>\
                      </div>\
                      <div role="tabpanel" class="tab-pane tab-pane-new" id="shop" style="height: 220px;">\
                          <h2 class="price-btn no-pad-top">Цена: <span>${data.price}</span></h2>\
                          <table>\
                              <tbody>\
                                  <tr>\
                                      <td class="table-grey">Название магазина</td>\
                                      <td class="table-black"><a href="${data.map_stores_url}" target="_blank">Магазины и пункты выдачи</a> | <a href="/bid/transition/${data.id}/" class="popup-store" rel="nofollow" target="_blank">${data.store_name}</a></td>\
                                  </tr>\
                                  <tr>\
                                      <td class="table-grey">Доставка</td>\
                                      <td class="table-black">${data.delivery}</td>\
                                  </tr>\
                                  <tr>\
                                      <td class="table-grey">Способ оплаты</td>\
                                      <td class="table-black">${data.payment_methods}</td>\
                                  </tr>\
                                  <tr>\
                                      <td class="table-grey">Контактный телефон</td>\
                                      <td class="table-black">${data.phone}</td>\
                                  </tr>\
                              </tbody>\
                          </table> <span class="product-item--old-price d-block">1999 грв</span> </div>\
                      <div role="tabpanel" class="tab-pane tab-pane-new" id="discount" style="height: 220px;">\
                          <h2 class="price-btn no-pad-top">Цена: <span>${data.price}</span></h2>\
                          <div class="discount">\
                              <p class="orange-color">${data.coupon_size}</p>\
                              <p>Действителен до ${data.coupon_expire}</p>\
                          </div>\

                          <form class="header__search-form modal-input-form" method="GET" id="id_form_get_coupon">\
                              <div class="input-group">\
                                  <input id='id_name' class="header__search-input modal-input" type="text" placeholder="Введите Ваше имя"  name='name'>\
                                  <input id='id_email' class="header__search-input modal-input" type="email" placeholder="Введите Вашу почту"  name='email'>\
                                  <input class="form-control input-lg header__search-input modal-input" id="id_phone" name="phone" type="text" placeholder="Введите Ваш телефон">\

                                  <input type="hidden" name="coupon" value="${data.coupon}" id="coupon_id" />
                                  <input type="hidden" name="item" value="${data.id}" id="product_id"/>
                              </div>\
                              <input type="submit" id="check_coupon_form" value="ОТПРАВИТЬ" />
                          </form>\
                      </div>\
                  </div>\
              </div>\
          </div>\
      </div>\
      <div class="full-description__footer">\
          <img src="" alt="" class="svg-icon d-none" onclick="wishlist( ${data.id} )" id="wish" target="_blank">\
          <img src="" alt="" class="d-none">\
          <a class='orange-btn-cs orange-btn-padding-cs shop-btn' href="/bid/transition/${data.id}/" id="redirect-popup-button" target="_blank" >В МАГАЗИН</a>\
          <a class='orange-btn-cs orange-btn-padding-cs coupon-btn' >ОТПРАВИТЬ</a>\
      </div>\
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


function allMagicWithAddingDescBlock(){

  allItems = $('.catalog-block_li')
  getPositionInline = posInline()
  var activeBtn = $('.full-desc.active')
  var parentDiv = activeBtn.parent().parent().parent().parent()
  var positionOfItem = getPositionOfItemBlock();

  url = '/w/gti/?item='+$('.full-desc.active').data('id'),
  ajaxData = getAjaxData(url),
  moreBtnDisplay = JSON.parse(ajaxData).description_full.length > 0 ? 'block' : 'none',
  couponExists = typeof JSON.parse(ajaxData).coupon_size == 'undefined' ? 'none' : 'block'

  // add custom styles for active statement
  if($(window).width() > 1024 && $(window).width() < 1200) {
    parentDiv.find('.item_img').css({
      'border-top': '1px solid #FF4B00',
      'border-left': '1px solid #FF4B00',
      'border-right': '1px solid #FF4B00',
    })
    parentDiv.find('.item_footer').css({
        'border-bottom': '1px solid #FF4B00',
        'border-left': '1px solid #FF4B00',
        'border-right': '1px solid #FF4B00',
    })
  }


  $('.full-description-desctop').remove()


  // после какого елемента нужно вставить наш див
  // жопа с посленим рядом. для него надо делать проверку на количество елементов
  var getDivAfterInsert = Math.ceil(correctItem / getPositionInline) * getPositionInline;

  allItems.length < getDivAfterInsert
    ? currDiv = allItems.last()
    : currDiv = allItems[getDivAfterInsert-1]

  jQuery(currDiv).after(addDescBlock(JSON.parse(ajaxData), couponExists, moreBtnDisplay));

  setTimeout(function(){
    // scroll top
    sctollUpThanOpenDescBlock(600)
  }, 200)
}




// при наведении мыши делает эффект active
$('.catalog-block_li').mouseenter(function(){
  var actBtnClass = $(this).find('.full-desc').attr('class')
  if ($(window).width() >= 1201) {
      $(this).css({'overflow':'visible'});
  }
  }).mouseleave(function() {
  if ($(window).width() >= 1201) {
      var actBtnClass = $(this).find('.full-desc').attr('class')
      if (actBtnClass.includes('active')){
          $(this).find('.item_box').css({'border':'1px solid #FF4B00'});
          $(this).css({'overflow':'hidden'});
      } else {
          $(this).find('.item_box').css({'border':'1px solid #ededed'});
          $(this).css({'overflow':'hidden'});
      }
  }
});


function removeActiveCssStyles(actBtn) {
 
  var parDiv = actBtn.parent().parent().parent().parent(),  //  Это типа box, not full element
      windowWidth = $(window).width();

  // add custom styles for active statement
  if(windowWidth > 1200) {

    // scroll top
    // sctollUpThanOpenDescBlock(600);

    parDiv.css({'border':'none'})
    parDiv.css({'border':'1px solid #ededed'})
    parDiv.find('.item_img').css({
      'border-top': 'none',
      'border-left': 'none',
      'border-right': 'none',
    })
    parDiv.find('.item_footer').css({
        'border-bottom': 'none',
        'border-left': 'none',
        'border-right': 'none',
    })
  } else if($(window).width() > 1024 && $(window).width() < 1200) {
    parDiv.find('.item_img').css({
      'border-top': '1px solid #ededed',
      'border-left': '1px solid #ededed',
      'border-right': '1px solid #ededed',
    })
    parDiv.find('.item_footer').css({
        'border-bottom': '1px solid #ededed',
        'border-left': '1px solid #ededed',
        'border-right': '1px solid #ededed',
    })
  }

  $('.full-desc').removeClass('active');
}


// скрол наверх, когда нажимает на открыть desc
function sctollUpThanOpenDescBlock(speed){
  parentDiv = $('.full-desc.active').parent().parent().parent().parent()
  $('html, body').animate({ scrollTop: parentDiv.offset().top-100  }, speed)
}


// ПОДРОБНЕЕ - главная фигня
$(document).on('click', '.full-desc', function(event){
  event.preventDefault();

  if ($('.sort_filter .active').attr('class').includes('table')) {
    var windowWidth = $(window).width(),
      allItems = $('.catalog-block_li'),
      getPositionInline = posInline();

    if($('.full-desc.active').length != 0){
      removeActiveCssStyles($('.full-desc.active'));
    }
    

    windowWidth > 1024 ? $('.full-description-desctop').css({'display':'none'}) : null

    if(!$(this).attr('class').includes('active')){
        $(this).addClass('active')

        // показываем простой блок или модалку
        if (windowWidth > 1024) {
          allMagicWithAddingDescBlock()
        } else {
          $('body').css({'overflow':'hidden'})
          $('#descModal').css({'display':'block'})

          $('#descModal .full-description__footer').css({'display':'block'})
          $('#descModal .full-description__close--btn').css({'display':'block'})
          $('#descModal .more-btn.hdd').css({'display':'block'})
        }   
    }
  }
});



$('body').on('click', '.close', function(){
  $('body').css({'overflow':'auto'})
  $('.filter__item').css({'display':'none'})
  $('#descModal').css({'display':'none'})

  // если у нас отображение inline
  !$(this).parent().parent().parent().attr('class').includes('product-item--inline-bigger')
      ? sctollUpThanOpenDescBlock(600) : null
});


// click on img - не будет пригать вверх при нажатии
$(document).on('click', '.item_img', function (event){
  event.preventDefault();
})


// закрываем desc после повторного нажатия на Побробнее
$(document).on('click', '.full-desc.active', function() {
  $('.full-description__close--btn').click();
})


function lastLineOfDivsSetWidth(){
  var posInlineDivs = posInline(), 
  allItems = $('.catalog-block_li').length,
  insertValue = allItems % posInlineDivs, // последний ряд елементов
  arrSlice = $('.catalog-block_li').slice(allItems - insertValue, allItems);

  setTimeout(function(){
    $.each(arrSlice, function(index, value) {
      jQuery(value).css({ 'max-width': $('.catalog-block_li').first().css('width') })
    })
  }, .5) 
}

lastLineOfDivsSetWidth()



// TODO - ПЕРЕЛЕДАТЬ. ПОПАТ ДОЛЖНЕ С ВЫСОТЫ 1024px
oldPos = posInline()
$(window).on('resize', function(){


  allItems = $('.product-item')
  currPos = posInline();
  var windowWidth = $(window).width();

  lastLineOfDivsSetWidth()

  // FIRST DESCTOP VERSION.     SECOND - MODAL
  if(windowWidth > 1024){

    // from modal to desctop
    if($('#descModal').css('display')=='block' && $('.icon.active').attr('class').includes('table')){

      console.log('REMOVE MODAL FROM RESIZE')
      $('#descModal').css({'display':'none'});
      if($('.full-description-desctop').length == 0) {
        allMagicWithAddingDescBlock();
      }

      $('body').css({'overflow':'auto'})
      $('.full-description-desctop').css({'display':'block'})
    
    } else if($('#descModal').css('display')=='block' && $('.icon.active').attr('class').includes('inline')){  
      console.log('REMOVE MODAL FROM RESIZE - INLINE MODE')
      $('#descModal').css({'display':'none'});
      
      // при смене закрывается модалка но нужно оставить активной нужный блок
      allData = $('.product-item--inline .item_box');
      $.each(allData, function(index, value){
        console.log(jQuery(value).css('border-color'))
        if(jQuery(value).css('border-color') == 'rgb(255, 75, 0)') {
          jQuery(value).click();
          return false;
        }
      });

    } else {
      if (oldPos != currPos) {
        // мы уменьшаем размер екрана
        if ($('.full-desc .active') && oldPos > currPos && oldPos != Infinity) {
    
          console.log('Уменьшили')
          $('.full-description-desctop').remove()
          allMagicWithAddingDescBlock();
        } else if ($('.full-desc .active') && oldPos < currPos && oldPos != Infinity) {

          console.log('Увеличили')
          $('.full-description-desctop').remove()
          allMagicWithAddingDescBlock();
        }
        
        oldPos = currPos;
      }
    }
  } else {
    if ($('.full-desc.active').length == 1) {
      console.log('MODAL FROM RESIZE')
      $('.full-description-desctop').remove()
      $('#descModal').css({'display':'block'})
    }
    $('.full-description-modal').css({'display':'block'})
    $('#descModal .full-description__footer').css({'display':'block'})
    $('#descModal .full-description__close--btn').css({'display':'block'})

    // than me have inline data
    if($('.icon.active').attr('class').includes('inline') && $('.product-item--inline-bigger').length != 0) {
      $('#descModal').css({'display':'block'})
      $('#descModal .more-btn').css({'display':'block'})
    }
    
    oldPos = currPos;
  }  

})  



function sctollUpInlineThanOpenDescBlock(speed){
  $('html, body').animate({ scrollTop: $('.product-item--inline-bigger').offset().top-100  }, speed)
}


//  inline table
$(document).on('click', '.product-item--inline', function(){

  clsName = $(this).attr('class')
  windowWidth = $(window).width();

  if(windowWidth >1024) {
    $('.full-description__footer').css({'display':'none'})
    $('.full-description__close--btn').css({'display':'none'})
    $('.more-btn').css({'display':'none'})
    $('.more-btn').removeClass('shwd').removeClass('hhd').addClass('hdd').html('Еще')
    $('.lalal').css({'display':'none'})
    $('.lalal').removeClass('shwd').removeClass('hhd').addClass('hdd')


    if (clsName.includes('product-item--inline-bigger')) {
      $(this).removeClass('product-item--inline-bigger')
      $(this).find('.more-btn').css({'display':'none'})
    } else {
      $('.product-item--inline').removeClass('product-item--inline-bigger')
      $(this).addClass('product-item--inline-bigger')
      $(this).find('.product-item--title').before('<span class="full-description__close--btn close">×</span>')
      $(this).find('.more-btn').css({'display':'block'})
      $(this).find('.item_detail').after('<div class="full-description__footer"> <img src="" alt="" class="svg-icon d-none" onclick="wishlist( 1141864 )" id="wish" target="_blank"> <img src="" alt="" class="d-none"> <a class="orange-btn-cs orange-btn-padding-cs shop-btn" href="/bid/transition/1141864/" id="redirect-popup-button" target="_blank" style="position: absolute; bottom: 24px;">В МАГАЗИН</a> <a class="orange-btn-cs orange-btn-padding-cs coupon-btn" style="position: absolute; bottom: 24px;">ОТПРАВИТЬ</a> </div>')
      sctollUpInlineThanOpenDescBlock(600)
    }
  } else {
    $('.product-item--inline').removeClass('product-item--inline-bigger')
    $('#descModal .full-description__footer').css({'display':'block'})
    $('#descModal .full-description__close--btn').css({'display':'block'})
    $('#descModal .more-btn').css({'display':'block'})
    $('#descModal').css({'display':'block'});
  }

});




// иконка для фильтрации
$(document).on('click', '.icon', function(){
  $('.icon').removeClass('active');
  $(this).addClass('active');

  var clsName = $(this).attr('class')
  if (clsName.includes('inline')) {
    $('.full-description-desctop').remove()
    // if($(window).width() > 1024) {
    //   $('.full-description').css({'display':'none'})
    // }
    
    $('.catalog-block_ul').addClass('catalog-block_ul--inline');
    $('.catalog-block_li').addClass('product-item--inline');
    $('.item_box').css({'border':'1px solid #ededed'})
    $('.product-item').css({'overflow':'hidden'})
    $('.full-desc').removeClass('active')

    allData = $('.product-item');
    $.each(allData, function(index, value){
      var shortDesc = jQuery(value).find('.item_detail').attr('data-id').slice(0, 200),
          fullDesc = jQuery(value).find('.item_detail').attr('data-id').slice(200, -1);
          
          // delete dublicate than multiplay click in icon
          if(jQuery(value).find('.general-content-here').length != 0) {
            jQuery(value).find('.general-content-here').remove()
          }
          jQuery(value).find('.item_detail').first().before('<div class="item_short_desc general-content-here"></div>')
          jQuery(value).find('.item_short_desc').html(`<p>${shortDesc}<span class="lalal hdd" style="display:none;">${fullDesc}</span></p><span class="more-btn hdd" style="display: none;">Еще</span>`)
    })

  } else {
    $('.catalog-block_ul').removeClass('catalog-block_ul--inline');
    $('.catalog-block_li').removeClass('product-item--inline').removeClass('product-item--inline-bigger');
    $('.item_short_desc.general-content-here').remove()
    $('.full-description__footer').css({'display':'none'})
    $('.full-description__close--btn').css({'display':'none'})
    $('.product-item').css({'overflow':'hidden'})
  }
});
