$(document).ready(function () {

    //////////////////////////////////////////////////////////////////////////////////////
    //            tabulation
    //////////////////////////////////////////////////////////////////////////////////////
    $(document).on('click', '.nav-tabs li', function (event){
        event.preventDefault();
        $('.nav-tabs li').removeClass('active');
        $('.tab-pane').removeClass('active');
        var newId = $(this).find('a').attr('aria-controls')
        $(this).addClass('active');
        $(`#${newId}`).addClass('active');
        $('.modal-footer .orange-btn').html('В магазин');

        var trWidth = $('.tab-content').width() / 2;
        $('.full-description table td').css({'width': trWidth})
    });

    setTimeout(function () {
        if (location.hash) {
            window.scrollTo(0, 0);
        }
    }, 1);


    // click on img
    $(document).on('click', '.item_img', function (event){
        event.preventDefault();
    })

    
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

    //////////////////////////////////////////////////////////////////////////////////////
    //                   display description
    //////////////////////////////////////////////////////////////////////////////////////


    // remove all active btn and opacity and remove desc block
    function deleteExtraData() {
        var allDataAfter = $(".testtest").nextAll(),
            windowWidth = $(window).width(),
            getPosition = getCurrentPosition(windowWidth),
            actBtn = $('.full-desc.active').parent().parent().parent().parent().parent();

        $.each(allDataAfter, function(index, value) {
            if((index+1) % getPosition == 0) {
                jQuery(value).css({'margin-left':'0'})
            }
        });
        
        
        // remove active from block effect
        parDiv = $('.full-desc.active').parent().parent().parent().parent().parent()
        $('.item_box').css({'border':'none'});
        
        if ($(window).width() >= 1201) {     
            $('.item_box').css({'border':'1px solid #ededed'});            
            // parDiv.find('.item_img').css({
            //     'border': 'none',
            //     'border-bottom': '1px solid #ededed'
            // })       
            // parDiv.find('.item_footer').css({
            //     'border-top': 'none',
            //     'border-left': 'none',
            //     'border-right': 'none',
            //     'border-bottom': 'none',
            //     'background':'none'
            // })
            // parDiv.css({ 'overflow':'hidden'})
            // setTimeout(function(){
            //     parDiv.find('.item_box').css({ 'border': '1px solid #ededed' })
            // }, 250)

        } else {
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
        $('.product-item').css({'opacity': '1'});
        $('.testtest').remove();
        $('.delete-empty').remove();
        $('.product-item--action img').css({'display':'none'});
        $('.product-item--old-price').css({'display':'none'});
        $('.product-item--price').css({'margin-top':'10px'});
        $('.product-item--stars').css({'display':'none'});
    }




    // create block
    function addDataDiv(data, mgBtm, moreBtnDisplay) {
        return `\
            <div class='testtest'>\
                <span class='opacity-zero'>dd<br>dd<br>dd<br></span>\
                <div class="full-description" style="margin-top: ${mgBtm}">\
                    <div class="full-description__content">\

                        <div class="full-description__content--img">\
                            <img alt='' src='${data.image_url}'>\
                        </div>\

                        <div class="full-description__content--info">\
                            <div>\
                                <div class="full-description__close">\
                                    <h3>${data.name}</h3>\
                                    <span class='full-description__close--btn close'>&times;</span>\
                                </div>\

                                <ul class="nav nav-tabs" role="tablist">\
                                    <li class="active"><a href="#home" aria-controls="home" role="tab" data-toggle="tab">Продукт</a></li>\
                                    <li><a href="#profile" aria-controls="profile" role="tab" data-toggle="tab">Магазин</a></li>\
                                    <li class='discount-btn'><a href="#discount" aria-controls="discount" role="tab" data-toggle="tab">Купон на скидку</a></li>\
                                </ul>\

                                <div class="tab-content">\
                                    <div role="tabpanel" class="tab-pane tab-pane-new active" id="home">\
                                        <h2 class="price-btn no-pad-top">Цена: <span>${data.price}</span></h2>\

                                        <div class='general-content-here'>\
                                            <p>${data.description_short}<span class='lalal hdd' style='display:none'>${data.description_full}</span></p>\
                                            <span class='more-btn' style="display: ${moreBtnDisplay}">Еще</span>
                                        </div>\

                                        <div class='product-item--stars d-flex marg-y-24 d-none'>\
                                            <div id='delta'>0</div>
                                            <img src="img/star.png" alt="">\
                                            <img src="img/star.png" alt="">\
                                            <img src="img/star.png" alt="">\
                                            <img src="img/star.png" alt="">\
                                            <img src="img/star.png" alt="">\
                                        </div>\
                                        <span class='product-item--old-price d-block'>1999 грв</span>\
                                    </div>\
                                    <div role="tabpanel" class="tab-pane tab-pane-new" id="profile">\
                                        <h2 class="price-btn no-pad-top">Цена: <span>${data.price}</span></h2>\
                                        <table>\
                                            <tr>\
                                                <td class='table-grey'>Название магазина</td>\
                                                <td class='table-black'><a href="${data.map_stores_url}" target="_blank">Магазины и пункты выдачи</a> | <a href="/bid/transition/${data.id}/" class="popup-store" rel="nofollow" target="_blank" >${data.store_name}</a></td>\
                                            </tr>\
                                            <tr>\
                                                <td class='table-grey'>Доставка</td>\
                                                <td class='table-black'>${data.delivery}</td>\
                                            </tr>\
                                            <tr>\
                                                <td class='table-grey'>Способ оплаты</td>\
                                                <td class='table-black'>${data.payment_methods}</td>\
                                            </tr>\
                                            <tr>\
                                                <td class='table-grey'>Контактный телефон</td>\
                                                <td class='table-black'>${data.phone}</td>\
                                            </tr>\
                                        </table>\
                                        <span class='product-item--old-price d-block'>1999 грв</span>\
                                    </div>\
                                    <div role="tabpanel" class="tab-pane tab-pane-new" id="discount">\
                                        <h2 class="price-btn no-pad-top">Цена: <span>${data.price}</span></h2>\
                                        <div class='discount'>\
                                            <p class='orange-color'>${data.coupon_size}</p>\
                                            <p>Действителен до ${data.coupon_expire}</p>\
                                        </div>\

                                        <form class="header__search-form modal-input-form" action="" method="get" id='check_coupon_form'>\
                                            <span class='product-item--old-price d-block'>1999 грв</span>\
                                            <div class="input-group">\
                                                <input class="header__search-input modal-input" type="search" placeholder="Введите Ваше имя" autocomplete="on" name="" required="">\
                                                <input class="header__search-input modal-input" type="search" placeholder="Введите Вашу почту" autocomplete="on" name="" required="">\
                                                <input class="header__search-input modal-input" type="search" placeholder="Введите Ваш телефон" autocomplete="on" name="" required="">\
                                            </div>\
                                        </form>\
                                        <span class='product-item--old-price d-block'>1999 грв</span>\
                                    </div>\
                                </div>\
                            </div>\
                        </div>\

                    </div>\

                    <div class="full-description__footer">\
                        <img src="../img/like.png" alt="" class="svg-icon d-none" onclick="wishlist( ${data.id} )" id="wish" target="_blank">\
                        <img src="img/mdi-scale-balance.png" alt="" class="d-none">\
                        <a class='orange-btn-cs orange-btn-padding-cs' href="/bid/transition/${data.id}/" id="redirect-popup-button" target="_blank" >В МАГАЗИН</a>\
                    </div>\
                </div>\
            </div>\
        `
    }


    function addModalDataDiv(data, moreBtnDisplay) {
       return `\
           <div class="modal-body">\
               <div class="full-description">\
                   <div class="full-description__content">\

                       <div class="full-description__content--img">\
                           <img alt='' src='${data.image_url}'>\
                       </div>\

                       <div class="full-description__content--info">\
                           <div>\

                               <div class="full-description__close">\
                                   <h3>${data.name}</h3>\
                                   <span class='full-description__close--btn close'>&times;</span>\
                               </div>\

                               <ul class="nav nav-tabs" role="tablist">\
                                   <li class="active"><a href="#home" aria-controls="home" role="tab" data-toggle="tab">Продукт</a></li>\
                                   <li><a href="#profile" aria-controls="profile" role="tab" data-toggle="tab">Магазин</a></li>\
                                   <li class='discount-btn'><a href="#discount" aria-controls="discount" role="tab" data-toggle="tab">Купон на скидку</a></li>\
                               </ul>\

                               <div class="tab-content">\
                                   <div role="tabpanel" class="tab-pane tab-pane-new active" id="home">\
                                       <h2 class="price-btn no-pad-top">Цена: <span>${data.price}</span></h2>\
                                       <h3>${data.name}</h3>\
                                       <div class='general-content-here'>\
                                            <p>${data.description_short}<span class='lalal hdd' style='display:none'>${data.description_full}</span></p>\
                                            <span class='more-btn' style="display: ${moreBtnDisplay}">Еще</span>
                                        </div>\

                                       <div class='product-item--stars d-flex marg-y-24 d-none'>\
                                           <div id='delta'>0</div>
                                           <img src="img/star.png" alt="">\
                                           <img src="img/star.png" alt="">\
                                           <img src="img/star.png" alt="">\
                                           <img src="img/star.png" alt="">\
                                           <img src="img/star.png" alt="">\
                                       </div>\
                                       <span class='product-item--old-price d-block'>1999 грв</span>\
                                   </div>\
                                   <div role="tabpanel" class="tab-pane tab-pane-new" id="profile">\
                                       <h2 class="price-btn no-pad-top">Цена: <span>${data.price}</span></h2>\
                                       <table>\
                                           <tr>\
                                               <td class='table-grey'>Название магазина</td>\
                                               <td class='table-black'><a href="${data.map_stores_url}" target="_blank">Магазины и пункты выдачи</a> | <a href="/bid/transition/${data.id}/" class="popup-store" rel="nofollow" target="_blank" >${data.store_name}</a></td>\
                                           </tr>\
                                           <tr>\
                                               <td class='table-grey'>Доставка</td>\
                                               <td class='table-black'>${data.delivery}</td>\
                                           </tr>\
                                           <tr>\
                                               <td class='table-grey'>Способ оплаты</td>\
                                               <td class='table-black'>${data.payment_methods}</td>\
                                           </tr>\
                                           <tr>\
                                               <td class='table-grey'>Контактный телефон</td>\
                                               <td class='table-black'>${data.phone}</td>\
                                           </tr>\
                                       </table>\
                                       <span class='product-item--old-price d-block'>1999 грв</span>\
                                   </div>\
                                   <div role="tabpanel" class="tab-pane tab-pane-new" id="discount">\
                                        <h2 class="price-btn no-pad-top">Цена: <span>${data.price}</span></h2>\
                                       <div class='discount'>\
                                           <p class='orange-color'>-50%</p>\
                                           <p>Действителен до 26.09.2020 07:19</p>\
                                       </div>\

                                       <form class="header__search-form modal-input-form" action="" method="get">\
                                           <div class="input-group">\
                                               <input class="header__search-input modal-input" type="search" placeholder="Введите Ваше имя" autocomplete="on" name="" required="">\
                                               <input class="header__search-input modal-input" type="search" placeholder="Введите Вашу почту" autocomplete="on" name="" required="">\
                                               <input class="header__search-input modal-input" type="search" placeholder="Введите Ваш телефон" autocomplete="on" name="" required="">\
                                           </div>\
                                       </form>\
                                       <span class='product-item--old-price d-block'>1999 грв</span>\
                                   </div>\
                               </div>\
                           </div>\
                       </div>\

                   </div>\

                   <div class="full-description__footer">\
                       <img src="../img/like.png" alt="" class="svg-icon d-none" onclick="wishlist( ${data.id} )" id="wish" target="_blank">\
                       <img src="img/mdi-scale-balance.png" alt="" class="d-none">\
                       <a class='orange-btn-cs orange-btn-padding-cs' href="/bid/transition/${data.id}/" id="redirect-popup-button" target="_blank" >В магазин</a>\
                   </div>\
               </div>\
           </div>\
       `
   }


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

    function addSecondDataForBorrom(height) {
        return `<li class='catalog-block_li col-1-of-4 product-item delete-empty' style='opacity: 0; height: ${height}px; margin-bottom: 96px;'></li>`
    }

    function getAjaxData(url) {
        var result="";
        $.ajax({
            url:url, async: false, success:function(data) {  result = data;  }
        });
        return result;
    }


    function scrollUpToTheParentDiv(parentDiv, speed){
        $('html, body').animate({ scrollTop: parentDiv.offset().top-130  }, speed);
    }

    function scrollDownToDecsBlock() {
        wind = $(window).width();
        if(wind >=1400) {
            $('html, body').animate({ scrollTop:  $('.full-description').offset().top - 350 }, 'slow');
        } else if (wind >= 1200) {
            $('html, body').animate({ scrollTop:  $('.full-description').offset().top - 400 }, 'slow');
        } else if (wind >= 992) {
            $('html, body').animate({ scrollTop:  $('.full-description').offset().top - 230 }, 'slow');
        } else if (wind >= 768) {
            $('html, body').animate({ scrollTop:  $('.full-description').offset().top - 230 }, 'slow');
        } else {
            $('html, body').animate({ scrollTop:  $('.full-description').offset().top - 200  }, 'slow');
        }

    }


    function scrollTopToTheBtn(pixel, speed) {
        var width = $('.full-description').height(),
            wind = $(window).height(),
            newHeight = wind-width,
            newnew = width;

        $('html, body').animate({ scrollTop:  $('.full-description__content').offset().top - pixel }, speed);
    }


    function getCurrentPosition(windowWidth) {
        if (windowWidth > 1399) {
            return 5
        } else if (windowWidth > 1199 && windowWidth < 1400) {
            return 4
        } else if (windowWidth >= 768 && windowWidth < 1200) {
            return 3
        } else if (windowWidth > 480 && windowWidth < 768) {
            return 2
        } else {
            return 1
        }
    }

    function getNewHeight() {
        var windowWidth = $(window).width(),
            posPerLine = getCurrentPosition(windowWidth),
            allDivs = $('.product-item'),
            allSlicedDiv = $('.product-item').slice(0, posPerLine);


        if (allSlicedDiv.find('.full-desc.active').length == 1){

            // if header position == relative - shit - быстрый скачок туда и назад
            // if header postion == fixed - need margin
            if ($('.header').css('position') == 'fixed') {
                $('.content').css({'margin-top':'135px'})
                $('html, body').animate({ scrollTop:  $('.full-desc.active').offset().top - 475 }, 'slow');
            } else {

                $('.header').css({
                    'display':'fixed',
                    'box-shadow': 'rgba(42, 48, 60, 0.19) 0px 1px 3px 0px',
                    'z-index':'99',
                    'left':'0',
                    'top':'0',
                    'right':'0'
                })
                console.log('HEADER')
                $('.content').css({'margin-top':'135px'})
                console.log('CONTENT')
                $('html, body').animate({ scrollTop:  $('.full-desc.active').offset().top - 455 }, 'slow');
                console.log('SCROLL')
            }

        } else {
            $('html, body').animate({ scrollTop:  $('.full-desc.active').offset().top - 475 }, 'slow');
        }
    }

    $(document).on('mousewheel', function(event) {
        var info = $('#delta'),
            oldData = info.html();
        info.html(parseInt(oldData) + event.deltaY)
        if(info.html() == 1) {
            $('.content').css({'margin-top':'0px'})
        }
    });




    function changeHeightContentTab() {
        setTimeout(function(){
            var allTabs = $('.tab-pane-new'),
                maxWidth = [],
                maxWidthForDiv = '';
            $.each(allTabs, function(index,value){ maxWidth.push(jQuery(value).height()) });
            maxWidthForDiv = Math.max.apply(Math, maxWidth)
            $('.tab-pane').css({'height': `${maxWidthForDiv}px`})
        }, 100)
    }


    $(document).on('click', '.full-desc', function(event){
        event.preventDefault();

        $('.content').css({'margin-top':'0px'})

        deleteExtraData()
        changeHeightContentTab()

        var classBtn = $(this).attr('class'),
            allItems = $('.product-item'),
            btnItemBlock = $(this).parent().parent(),
            windowWidth = $(window).width(),
            getPosition = getCurrentPosition(windowWidth),
            correctItem = '',
            amountOfItems = $('.product-item').length,
            redirect_url = $(this).data('url'),
            url = '/w/gti/?item='+$(this).data('id'),
            ajaxData = getAjaxData(url),
            filterOrangeBtnWidth = $('#price-filter').width(),
            filterOrangeBtnHeight = $('#price-filter').height(),
            moreBtnDisplay = JSON.parse(ajaxData).description_full.length > 0 ? 'block' : 'none';


        if(windowWidth > 480) {
            // первый раз нажали на кнопку
            if(!classBtn.includes('active')) {

                // display extra data for item block
                $(this).addClass('active');
                $(this).next().css({'display':'block'});
                $(this).parent().parent().find('.product-item--old-price').css({'display':'block'});
                $(this).parent().parent().find('.product-item--price').css({'margin-top':'0px'});
                $(this).parent().parent().find('.product-item--stars').css({'display':'flex'});

                parDiv = $(this).parent().parent().parent().parent().parent()
                // add active to block effect
                if ($(window).width() >= 1201) {

                } else {
                    parDiv.find('.item_img').css({
                        'border-top': '1px solid #FF4B00',
                        'border-left': '1px solid #FF4B00',
                        'border-right': '1px solid #FF4B00',
                    })
                    parDiv.find('.item_footer').css({
                        'border-bottom': '1px solid #FF4B00',
                        'border-left': '1px solid #FF4B00',
                        'border-right': '1px solid #FF4B00',
                    })
                }
                

                // делаю меньше растояние между блоком с коннетном и самим итемом
                if (windowWidth >= 1200) {
                    mgBtm = '-40px'
                } else if (windowWidth >= 768 && windowWidth < 1200) {
                    mgBtm = '-50px'
                } else if (windowWidth < 768) {
                    mgBtm = '-70px'
                } else {
                    mgBtm = 'auto'
                }
                

                

                var parentDiv = $(this).parent().parent().parent().parent()

                var positionOfItem = getPositionOfItemBlock();
                // getTriangleWidht(positionOfItem, getPosition);

                function getPositionOfItemBlock() {
                    $.each(allItems, function(dt, value) {
                        var innerBtnClass = jQuery(value).find('.full-desc').attr('class');
                        innerBtnClass.includes('active')
                            ? correctItem = dt+1
                            : jQuery(value).css({'opacity':'1'})
                    })
                    return correctItem
                }

                var getDivAfterInsert = Math.ceil(correctItem / getPosition) * getPosition;


                position = parseInt(getDivAfterInsert) > parseInt(amountOfItems) ? amountOfItems : getDivAfterInsert

                var currDiv = allItems[position];



                if(typeof currDiv === 'undefined') {
                    currDiv = allItems.last()
                    arr = [...Array(getDivAfterInsert - amountOfItems).keys()]

                    // когда у нас количество елементов полное в ряд, то последний ряд не отображается (arr.length = 0)
                    if (arr.length !== 0) {
                        arr.forEach(function(value){
                            jQuery(currDiv).after(addSecondDataForBorrom( $('.product-item').height() ))
                        })

                        last = jQuery($('.delete-empty').last())
                        last.after(addDataDiv(JSON.parse(ajaxData), mgBtm, moreBtnDisplay))
                        getNewHeight()
                    } else {
                        // последний ряд
                        jQuery(currDiv).after(addDataDiv(JSON.parse(ajaxData), mgBtm, moreBtnDisplay))
                        getNewHeight()
                    }
                } else {
                    // середина ряда и первый ряд
                    jQuery(currDiv).before(addDataDiv(JSON.parse(ajaxData), mgBtm, moreBtnDisplay))
                    getNewHeight()
                }
            } else {
                //  убираем active из кнопки
                scrollTopToTheBtn(650, 1000)
                deleteExtraData();
            }
        } else {
            $(this).addClass('active')
            displayModal('descModal', JSON.parse(ajaxData), moreBtnDisplay)
            moreBtnDisplay = JSON.parse(ajaxData).description_full.length > 0 ? 'block' : 'none';
            $('.more-btn').css({'display': moreBtnDisplay})
        }  
        
    });

    $(document).on('click', '.full-desc.active', function(event){
        event.preventDefault();
        getNewHeight()
        deleteExtraData();
    });

    $(document).on('click', '.full-description__close--btn', function() {
        getNewHeight()
        deleteExtraData()
    });


    /////////////////////////////////////////////////////////////////////////////////
    ////           resize
    /////////////////////////////////////////////////////////////////////////////////

    wdRes = $(window).width()
    oldPos = getCurrentPosition(wdRes)

    $(window).on('resize', function(){
        parentDiv = $('.full-desc.active').parent().parent().parent().parent()
        newPos = getCurrentPosition($(window).width())
        if (newPos != oldPos) {
            allItems = $('.product-item')
            $.each(allItems, function(dt, value) {
                var innerBtnClass = jQuery(value).find('.full-desc').attr('class');
                if (innerBtnClass.includes('active')) {
                    jQuery(value).find('.item_img').css({'border':'none'})
                    jQuery(value).find('.item_footer').css({'border':'none'})
                    jQuery(value).find('.item_box').css({'border':'none'})

                    jQuery(value).find('.item_box').css({'border':'#ff4b00'})

                    clickBtn = jQuery(value).find('.full-desc')

                    setTimeout(function(){
                        if(oldPos == 1) {
                            console.log('------------------')

                            $('.full-description__close--btn').click()
                        } else {
                            clickBtn.click()
                        }                        
                    }, 1);
                    setTimeout(function(){
                        clickBtn.click()
                    }, 5);
                }
            })
            
        }
        setTimeout(function(){
            oldPos = newPos;
        }, 100)
    })


    /////////////////////////////////////////////////////////////////////////////////
    ////           MODAL
    /////////////////////////////////////////////////////////////////////////////////

    function displayModal(id, data) {

        // addModalDataDiv
        $(`#${id} .modal-footer`).remove();
        $(`#${id} .modal-body`).remove();
        $(`#${id} .modal-content`).prepend(addModalDataDiv(data));

        var windHgt = $(window).height(),
        modalHgt = $('#descModal .full-description').height() + 24 + 24;
        if (windHgt > modalHgt) {
            console.log('Move down')
            $('#descModal .full-description .orange-btn-cs').css({
                'position': 'absolute',
                'bottom': '24px'
            })
        } else {
            console.log('Left as must')
            $('#descModal .full-description .orange-btn-cs').css({
                'position': 'relative',
                'bottom': '0px'
            })
        }


        $('body').css({'overflow':'hidden'})
        $('body').on('click', '.close', function(){
            $('body').css({'overflow':'auto'})
            $('.filter__item').css({'display':'none'})
            $('#descModal').css({'display':'none'})
        });


        $('.filter__item').css({'display':'block'})
        var modal = document.getElementById(id);

        // Get the <span> element that closes the modal
        var span = document.getElementsByClassName("close")[0];

        modal.style.display = "block";

        // When the user clicks on <span> (x), close the modal
        span.onclick = function() {
            modal.style.display = "none";
        }
    }


    /////////////////////////////////////////////////////////////////////////////////
    ////           MODAL
    /////////////////////////////////////////////////////////////////////////////////
    $(document).on('click', '.tab-pane.active', function(event){
        event.preventDefault();
    });
});