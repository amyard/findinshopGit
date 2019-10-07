
$(document).ready(function () {

    //////////////////////////////////////////////////////////////////////////////////////
    //            resize window
    //////////////////////////////////////////////////////////////////////////////////////
    // var width = $(window).width();
    // $(window).on('resize', function() {
    //     if ($(this).width() != width && $(this).width() < 648) {
    //         width = $(this).width();
    //         console.log(width)
    //         $('.body').css({'min-width': `${width}px`})
    //     }
    // });


    //////////////////////////////////////////////////////////////////////////////////////
    //            problem with flexbox
    //////////////////////////////////////////////////////////////////////////////////////
    
    function getFlexTitleBox() {
        var allPrItems = $('.product-item--title'),
            asd = [],
            maxValue = '';
        $.each(allPrItems, function(index, value) {
            asd.push(jQuery(value).height());
        });
        maxValue = Math.max(...asd);
        $('.product-item--title').css({'height':maxValue})
    }

    getFlexTitleBox()
    $(window).on('resize', function() {
        $('.product-item--title').css({'height':'100%'})
        getFlexTitleBox();
    });




    //////////////////////////////////////////////////////////////////////////////////////
    //            tabulation
    //////////////////////////////////////////////////////////////////////////////////////
    $(document).on('click', '.nav-tabs li', function (){
        $('.nav-tabs li').removeClass('active');
        $(this).addClass('active');
        $('.modal-footer .orange-btn').html('В магазин');

        var trWidth = $('.tab-content').width() / 2;
        $('.full-description table td').css({'width': trWidth})
    });

    //////////////////////////////////////////////////////////////////////////////////////
    //                       accordion
    //////////////////////////////////////////////////////////////////////////////////////
    var acc = document.getElementsByClassName("filter__item-title");
    var i;

    for (i = 0; i < acc.length; i++) {
        acc[i].addEventListener("click", function() {
            this.classList.toggle("active");
            var panel = this.nextElementSibling;
            if (panel.style.display === "block") {
                panel.style.display = "none";
            } else {
                panel.style.display = "block";
            }
        
        });
    }

    //////////////////////////////////////////////////////////////////////////////////////
    //                   display description
    //////////////////////////////////////////////////////////////////////////////////////


    // remove all active btn and opacity and remove desc block
    function deleteExtraData() {


        var allDataAfter = $(".testtest").nextAll(),
            windowWidth = $(window).width(),
            getPosition = getCurrentPosition(windowWidth);

        $.each(allDataAfter, function(index, value) {
            if((index+1) % getPosition == 0) {
                jQuery(value).css({'margin-left':'0'})
            }
        }); 

        $('.full-desc').removeClass('active');
        $('.product-item').css({'opacity': '1'});
        $('.testtest').remove();
        $('.delete-empty').remove();
        $('.product-item--action img').css({'display':'none'});
        $('.product-item--old-price').css({'display':'none'});
        $('.product-item--price').css({'margin-top':'24px'});
        $('.product-item--stars').css({'display':'none'});
    }

    function getCurrentPosition(windowWidth) {
        if (windowWidth > 1472) {
            return 5
        } else if ( windowWidth > 1281 && windowWidth < 1472) {
            return 4
        } else {
            return 3
        }
    }

    $(document).on('click', '.full-desc', function(event){
        event.preventDefault();

        deleteExtraData();


        var classBtn = $(this).attr('class'),
            allItems = $('.product-item'),
            btnItemBlock = $(this).parent().parent(),
            windowWidth = $(window).width(),
            getPosition = getCurrentPosition(windowWidth),
            correctItem = '',
            amountOfItems = $('.product-item').length;


        if(windowWidth > 986) {
            // первый раз нажали на кнопку
            if(!classBtn.includes('active')) {

                // display extra data for item block
                $(this).addClass('active');
                $(this).next().css({'display':'block'});
                $(this).parent().parent().find('.product-item--old-price').css({'display':'block'});
                $(this).parent().parent().find('.product-item--price').css({'margin-top':'0px'});
                $(this).parent().parent().find('.product-item--stars').css({'display':'flex'});
                


                var positionOfItem = getPositionOfItemBlock();

                function getPositionOfItemBlock() {
                    $.each(allItems, function(dt, value) {
                        var innerBtnClass = jQuery(value).find('.full-desc').attr('class');
                        innerBtnClass.includes('active')
                            ? correctItem = dt+1
                            : jQuery(value).css({'opacity':'0.5'})
                    })
                    return correctItem
                }

                var getDivAfterInsert = Math.ceil(correctItem / getPosition) * getPosition;

                position = parseInt(getDivAfterInsert) > parseInt(amountOfItems) ? amountOfItems : getDivAfterInsert

                var currDiv = allItems[position],
                    title = jQuery(allItems[positionOfItem-1]).find('.product-item--title').html();
               

                if(typeof currDiv === 'undefined') {
                    currDiv = allItems.last()
                    arr = [...Array(getDivAfterInsert - amountOfItems).keys()]

                    // когда у нас количество елементов полное в ряд, то последний ряд не отображается (arr.length = 0)
                    if (arr.length !== 0) {
                        arr.forEach(function(value){
                            jQuery(currDiv).after(addSecondDataForBorrom( $('.product-item').height() ))
                        })
                        last = jQuery($('.delete-empty').last())
                        last.after(addDataDiv(title))
                    } else {
                        jQuery(currDiv).after(addDataDiv(title))
                    }
                    
                } else {
                    jQuery(currDiv).before(addDataDiv(title))

                    // когда добаляет блок, то сносится маргин у последнего блока каждо строки 
                    // ({'margin-right':'0', 'margin-left':'2rem'})
                    var allDataAfter = $(".testtest").nextAll();
                    $.each(allDataAfter, function(index, value) {
                        if((index+1) % getPosition == 0) {
                            jQuery(value).css({'margin-right':'0', 'margin-left':'2rem'})
                        }
                    });    
                }

                // create block
                function addDataDiv(title) {
                    return `\
                            <div class='testtest'>\
                                <span class='opacity-zero'>dd</span>\
                                <div class="full-description">\
                                    <div class="full-description__close">\
                                        <span class='full-description__close--btn'>&times;</span>\
                                    </div>\
                            
                                    <div class="full-description__content">\
                                        
                                        <div class="full-description__content--img">\
                                            <img alt='' src='img/asd.jpg'>\
                                        </div>\
                            
                                        <div class="full-description__content--info">\
                                            <div>\
                                                
                                                <ul class="nav nav-tabs" role="tablist">\
                                                    <li class="active"><a href="#home" aria-controls="home" role="tab" data-toggle="tab">Продукт</a></li>\
                                                    <li><a href="#profile" aria-controls="profile" role="tab" data-toggle="tab">Магазин</a></li>\
                                                    <li class='discount-btn'><a href="#discount" aria-controls="discount" role="tab" data-toggle="tab">Купон на скидку</a></li>\
                                                </ul>\
                                                
                                                <div class="tab-content">\
                                                    <div role="tabpanel" class="tab-pane active" id="home">\
                                                        <h3>${title}</h3>\
                                                        <p>Динамические закрытого типа - Частотные характеристики 5 Гц - 22000 Гц - Чувствительность 102 дБ / мВт - сопротивление 24 Ом (1 кГц) - микрофон есть...</p>\
                                                        <div class='product-item--stars d-flex marg-y-24'>\
                                                            <img src="img/star.png" alt="">\
                                                            <img src="img/star.png" alt="">\
                                                            <img src="img/star.png" alt="">\
                                                            <img src="img/star.png" alt="">\
                                                            <img src="img/star.png" alt="">\
                                                        </div>\
                                                        <span class='product-item--old-price d-block'>1999 грв</span>\
                                                        <h2 class="no-pad-top">1199 грв</h2>\
                                                    </div>\
                                                    <div role="tabpanel" class="tab-pane" id="profile">\
                                                        <table>\
                                                            <tr>\
                                                                <td class='table-grey'>Название магазина</td>\
                                                                <td class='table-black'>Пример</td>\
                                                            </tr>\
                                                            <tr>\
                                                                <td class='table-grey'>Доставка</td>\
                                                                <td class='table-black'>Нет</td>\
                                                            </tr>\
                                                            <tr>\
                                                                <td class='table-grey'>Способ оплаты</td>\
                                                                <td class='table-black'>Нет</td>\
                                                            </tr>\
                                                            <tr>\
                                                                <td class='table-grey'>Контактный телефон</td>\
                                                                <td class='table-black'>+38 (000) 000-00-00</td>\
                                                            </tr>\
                                                        </table>\
                                                        <span class='product-item--old-price d-block'>1999 грв</span>\
                                                        <h2 class="no-pad-top">1199 грв</h2>\
                                                    </div>\
                                                    <div role="tabpanel" class="tab-pane" id="discount">\
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
                                                        <h2 class="no-pad-top">1199 грв</h2>\
                                                    </div>\
                                                </div>\
                                            </div>\
                                        </div>\
                            
                                    </div>\
                            
                                    <div class="full-description__footer">\
                                        <img src="img/like.png" alt="" class="svg-icon">\
                                        <img src="img/mdi-scale-balance.png" alt="" class="svg-icon">\
                                        <button class='orange-btn orange-btn-padding'>В магазин</button>\
                                    </div>\
                                </div>\
                            </div>\
                            `
                }

                function addSecondDataForBorrom(height) {
                    return `<div class='col-1-of-4 product-item delete-empty' style='opacity: 0; height: ${height}px; margin-bottom: 96px;'></div>`
                }
            }
        } else {
            displayModal('descModal')
        } 
    });

    $(document).on('click', '.full-desc.active', function(event){
        event.preventDefault();
        deleteExtraData();
    });

    $(document).on('click', '.full-description__close--btn', function() {
        deleteExtraData()
    });



    /////////////////////////////////////////////////////////////////////////////////
    ////           MODAL
    /////////////////////////////////////////////////////////////////////////////////

    function displayModal(id) {

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
        
        setTimeout(function() {
            $(`#${id} .modal-content`).css({'height': '100%'})
            var windowHeight = $(window).height(),
                modalHeight = $(`#${id} .modal-content`).height(),
                newSize = windowHeight + 1;

            if(windowHeight < modalHeight) {
                $(`#${id} .modal-content`).css({'height':'100%', 'overflow-y':'scroll'})
            } else {
                $(`#${id} .modal-content`).css({'height':`${newSize}px`, 'overflow-y':'scroll'})
            }
        }, 310);
    }

    $(document).on('click', '.filter__title', function() {    
        if ($(window).width() <= 986) {
            displayModal('successModal')
        }  
    });


    /////////////////////////////////////////////////////////////////////////////////
    ////           MODAL
    /////////////////////////////////////////////////////////////////////////////////
    $(document).on('click', '.discount-btn', function(){
        $('.modal-footer .orange-btn').html('Получить купон');
    });
    $(document).on('click', '.tab-pane.active', function(event){
        event.preventDefault();
    });


    /////////////////////////////////////////////////////////////////////////////////
    ////           Search icon
    /////////////////////////////////////////////////////////////////////////////////
    $(document).on('click', '.header__search-icon', function(event){
        event.preventDefault();
        var clsName = $(this).attr('class')
        if(!clsName.includes('active')) {
            $(this).addClass('active');
            $('.header__search-form').css({
                'display': 'block', 
                'position':'absolute', 
                'z-index':'100',
                'top':'110px',
                'margin':'0 auto',
                'left':'32px',
                'border':'1px solid #F4F4F4',
                'background-color': '#f4f4f4',
                'box-shadow':'0px 2px 8px rgba(0, 0, 0, 0.1)',
                'padding':'7px 15px'
            });
            var windowWidth = ($(window).width()) * 0.55;
            $('.header__search-input').css({'width': `${windowWidth}px`});

            
        } else {
            $(this).removeClass('active');
            $('.header__search-form').css({
                'display': 'none',
                'position':'relative',
                'border':'none',
                'background-color':'none',
                'box-shadow':'none',

            })
        }
    });

    $(window).on('resize', function() {
        if ($(window).width() < 768) {
            var windowWidth = ($(window).width()) * 0.55;
            $('.header__search-input').css({'width': `${windowWidth}px`});
        } else {
            $('.header__search-input').css({'width': `381px`});
        }

        var sliderWidth = $('.filter').width(),
            inputWidth = sliderWidth * 0.97;
        $('.rangeslider').css({'width':`${sliderWidth}px`})

        $('.filter').find('input[type="range"]').css({'width':`${inputWidth}px`})
    })




    /////////////////////////////////////////////////////////////////////////////////
    ////           RANGE SSLIDER
    /////////////////////////////////////////////////////////////////////////////////

    
    function addSeparator(nStr) {
        nStr += '';
        var x = nStr.split('.');
        var x1 = x[0];
        var x2 = x.length > 1 ? '.' + x[1] : '';
        var rgx = /(\d+)(\d{3})/;
        while (rgx.test(x1)) {
            x1 = x1.replace(rgx, '$1' + '.' + '$2');
        }
        return x1 + x2;
    }

    function rangeInputChangeEventHandler(e){
        var rangeGroup = $(this).attr('name'),
            minBtn = $(this).parent().children('.min'),
            maxBtn = $(this).parent().children('.max'),
            range_min = $(this).parent().children('.range_min'),
            range_max = $(this).parent().children('.range_max'),
            minVal = parseInt($(minBtn).val()),
            maxVal = parseInt($(maxBtn).val()),
            origin = $(this).context.className;

        if(origin === 'min' && minVal > maxVal-5){
            $(minBtn).val(maxVal-5);
        }
        var minVal = parseInt($(minBtn).val());
        $(range_min).html(addSeparator(minVal*1000) + ' €');


        if(origin === 'max' && maxVal-5 < minVal){
            $(maxBtn).val(5+ minVal);
        }
        var maxVal = parseInt($(maxBtn).val());
        $(range_max).html(addSeparator(maxVal*1000) + ' €');
    }





});