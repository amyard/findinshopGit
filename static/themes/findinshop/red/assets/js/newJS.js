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
        $('.product-item--price').css({'margin-top':'10px'});
        $('.product-item--stars').css({'display':'none'});
    }

    function getCurrentPosition(windowWidth) {
        if (windowWidth > 1399) {
            return 5
        } else if (windowWidth > 1199 && windowWidth < 1400) {
            return 4
        } else if (windowWidth >= 768 && windowWidth < 1200) {
            return 3
        } else {
            return 2
        }
    }

    // create block
    function addDataDiv(data, mgBtm) {
        return `\
            <div class='testtest'>\
                <span class='opacity-zero'>dd<br>dd<br>dd<br></span>\
                <div class="full-description" style="margin-top: ${mgBtm}">\
                    <div class="full-description__close">\
                        <span class='full-description__close--btn'>&times;</span>\
                    </div>\

                    <div class="full-description__content">\

                        <div class="full-description__content--img">\
                            <img alt='' src='${data.image_url}'>\
                        </div>\

                        <div class="full-description__content--info">\
                            <div>\

                                <ul class="nav nav-tabs" role="tablist">\
                                    <li class="active"><a href="#home" aria-controls="home" role="tab" data-toggle="tab">Продукт</a></li>\
                                    <li><a href="#profile" aria-controls="profile" role="tab" data-toggle="tab">Магазин</a></li>\
                                    <li class='discount-btn d-none'><a href="#discount" aria-controls="discount" role="tab" data-toggle="tab">Купон на скидку</a></li>\
                                </ul>\

                                <div class="tab-content">\
                                    <div role="tabpanel" class="tab-pane active" id="home">\
                                        <h3>${data.name}</h3>\
                                        <p>${data.description}</p>\
                                        <div class='product-item--stars d-flex marg-y-24 d-none'>\
                                            <img src="img/star.png" alt="">\
                                            <img src="img/star.png" alt="">\
                                            <img src="img/star.png" alt="">\
                                            <img src="img/star.png" alt="">\
                                            <img src="img/star.png" alt="">\
                                        </div>\
                                        <span class='product-item--old-price d-block'>1999 грв</span>\
                                        <h2 class="price-btn no-pad-top">${data.price}</h2>\
                                    </div>\
                                    <div role="tabpanel" class="tab-pane" id="profile">\
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
                                        <h2 class="no-pad-top">${data.price}</h2>\
                                    </div>\
                                    <div role="tabpanel" class="tab-pane d-none" id="discount">\
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
                                        <h2 class="no-pad-top">${data.price}</h2>\
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

//    function addModalDataDiv(data) {
//        return `\
//            <div class="modal-body">\
//                <div class="full-description">\
//                    <div class="full-description__close">\
//                        <span class='full-description__close--btn close'>&times;</span>\
//                    </div>\
//
//                    <div class="full-description__content">\
//
//                        <div class="full-description__content--img">\
//                            <img alt='' src='${data.image_url}'>\
//                        </div>\
//
//                        <div class="full-description__content--info">\
//                            <div>\
//
//                                <ul class="nav nav-tabs" role="tablist">\
//                                    <li class="active"><a href="#home" aria-controls="home" role="tab" data-toggle="tab">Продукт</a></li>\
//                                    <li><a href="#profile" aria-controls="profile" role="tab" data-toggle="tab">Магазин</a></li>\
//                                    <li class='discount-btn d-none'><a href="#discount" aria-controls="discount" role="tab" data-toggle="tab">Купон на скидку</a></li>\
//                                </ul>\
//
//                                <div class="tab-content">\
//                                    <div role="tabpanel" class="tab-pane active" id="home">\
//                                        <h3>${data.name}</h3>\
//                                        <p>${data.description}</p>\
//                                        <div class='product-item--stars d-flex marg-y-24 d-none'>\
//                                            <img src="img/star.png" alt="">\
//                                            <img src="img/star.png" alt="">\
//                                            <img src="img/star.png" alt="">\
//                                            <img src="img/star.png" alt="">\
//                                            <img src="img/star.png" alt="">\
//                                        </div>\
//                                        <span class='product-item--old-price d-block'>1999 грв</span>\
//                                        <h2 class="no-pad-top">${data.price}</h2>\
//                                    </div>\
//                                    <div role="tabpanel" class="tab-pane" id="profile">\
//                                        <table>\
//                                            <tr>\
//                                                <td class='table-grey'>Название магазина</td>\
//                                                <td class='table-black'><a href="${data.map_stores_url}" target="_blank">Магазины и пункты выдачи</a> | <a href="/bid/transition/${data.id}/" class="popup-store" rel="nofollow" target="_blank" >${data.store_name}</a></td>\
//                                            </tr>\
//                                            <tr>\
//                                                <td class='table-grey'>Доставка</td>\
//                                                <td class='table-black'>${data.delivery}</td>\
//                                            </tr>\
//                                            <tr>\
//                                                <td class='table-grey'>Способ оплаты</td>\
//                                                <td class='table-black'>${data.payment_methods}</td>\
//                                            </tr>\
//                                            <tr>\
//                                                <td class='table-grey'>Контактный телефон</td>\
//                                                <td class='table-black'>${data.phone}</td>\
//                                            </tr>\
//                                        </table>\
//                                        <span class='product-item--old-price d-block'>1999 грв</span>\
//                                        <h2 class="no-pad-top">${data.price}</h2>\
//                                    </div>\
//                                    <div role="tabpanel" class="tab-pane d-none" id="discount">\
//                                        <div class='discount'>\
//                                            <p class='orange-color'>-50%</p>\
//                                            <p>Действителен до 26.09.2020 07:19</p>\
//                                        </div>\
//
//                                        <form class="header__search-form modal-input-form" action="" method="get">\
//                                            <div class="input-group">\
//                                                <input class="header__search-input modal-input" type="search" placeholder="Введите Ваше имя" autocomplete="on" name="" required="">\
//                                                <input class="header__search-input modal-input" type="search" placeholder="Введите Вашу почту" autocomplete="on" name="" required="">\
//                                                <input class="header__search-input modal-input" type="search" placeholder="Введите Ваш телефон" autocomplete="on" name="" required="">\
//                                            </div>\
//                                        </form>\
//                                        <span class='product-item--old-price d-block'>1999 грв</span>\
//                                        <h2 class="no-pad-top">${data.price}</h2>\
//                                    </div>\
//                                </div>\
//                            </div>\
//                        </div>\
//
//                    </div>\
//
//                    <div class="full-description__footer">\
//                        <img src="../img/like.png" alt="" class="svg-icon" onclick="wishlist( ${data.id} )" id="wish" target="_blank">\
//                        <img src="img/mdi-scale-balance.png" alt="">\
//                        <a class='orange-btn-cs orange-btn-padding-cs' href="/bid/transition/${data.id}/" id="redirect-popup-button" target="_blank" >В магазин</a>\
//                    </div>\
//                </div>\
//            </div>\
//        `
//    }

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


    function changeSizeOfImg() {
        // change img height / для нокиа - height: 100%  для других hieght: auto
        var imgHeight = $('.full-description__content--img img').height(),
            divImgHeight = $('.full-description__content').height();

        $('.full-description__content--img img').css({'max-height': '100%'})
        imgHeight > divImgHeight
            ? $('.full-description__content--img img').css({'height': '100%'})
            : $('.full-description__content--img img').css({'height': 'auto'})
    }

    function scrollUpToTheParentDiv(parentDiv, speed){
        $('html, body').animate({ scrollTop: parentDiv.offset().top-130  }, speed);
    }

    function scrollDownToDecsBlock() {
        $('html, body').animate({ scrollTop:  $('.full-description').offset().top - 250 }, 'slow');
    }

    function scrollTopToTheBtn(pixel, speed) {
        $('html, body').animate({ scrollTop:  $('.full-description').offset().top - pixel }, speed);
    }

    function imgContainerDesc (windowWidth) {
        if (windowWidth > 1199) {
            var imgDescBlockWidth = $('.full-description__content--img').width(),
                containerDescBlockWidth = $('.full-description').width()
                newWidth = parseInt(containerDescBlockWidth) - parseInt(imgDescBlockWidth) - 74 - 64;
            $('.full-description__content--info').css({'width': `${newWidth}px`})
        }
    }

    $(document).on('click', '.full-desc', function(event){
        event.preventDefault();

        deleteExtraData()

        var classBtn = $(this).attr('class'),
            allItems = $('.product-item'),
            btnItemBlock = $(this).parent().parent(),
            windowWidth = $(window).width(),
            getPosition = getCurrentPosition(windowWidth),
            correctItem = '',
            amountOfItems = $('.product-item').length,
            redirect_url = $(this).data('url'),
            url = '/w/gti/?item='+$(this).data('id'),
            ajaxData = getAjaxData(url);


        // первый раз нажали на кнопку
        if(!classBtn.includes('active')) {

            // display extra data for item block
            $(this).addClass('active');
            $(this).next().css({'display':'block'});
            $(this).parent().parent().find('.product-item--old-price').css({'display':'block'});
            $(this).parent().parent().find('.product-item--price').css({'margin-top':'0px'});
            $(this).parent().parent().find('.product-item--stars').css({'display':'flex'});

            mgBtm = windowWidth < 1200 ?  `-${$('.catalog-block_li').first().css('margin-bottom')}` : 'auto'
            mgBtm = windowWidth < 1200 ?  '-50px' : 'auto'


            // делаю меньше растояние между блоком с коннетном и самим итемом
            if (windowWidth >= 768 && windowWidth < 1200) {
                mgBtm = '-50px'
            } else if (windowWidth < 768) {
                mgBtm = '-75px'
            } else {
                mgBtm = 'auto'
            }


            var parentDiv = $(this).parent().parent().parent().parent()

            var positionOfItem = getPositionOfItemBlock();

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
                    last.after(addDataDiv(JSON.parse(ajaxData), mgBtm))
                    changeSizeOfImg()
                    scrollUpToTheParentDiv(parentDiv, 800)
                    imgContainerDesc (windowWidth)
                } else {
                    jQuery(currDiv).after(addDataDiv(JSON.parse(ajaxData), mgBtm))
                    changeSizeOfImg()
                    scrollUpToTheParentDiv(parentDiv, 800)
                    imgContainerDesc (windowWidth)
                }
            } else {
                jQuery(currDiv).before(addDataDiv(JSON.parse(ajaxData), mgBtm))
                changeSizeOfImg()
                scrollUpToTheParentDiv(parentDiv, 800)
                imgContainerDesc (windowWidth)

                // когда добаляет блок, то сносится маргин у последнего блока каждо строки
                // ({'margin-right':'0', 'margin-left':'2rem'})
//                var allDataAfter = $(".testtest").nextAll();
//                $.each(allDataAfter, function(index, value) {
//                    if((index+1) % getPosition == 0) {
//                        jQuery(value).css({'margin-right':'0', 'margin-left':'2rem'})
//                    }
//                });
            }
        } else {
            //  убираем active из кнопки
            scrollTopToTheBtn(550, 900)
            deleteExtraData();
        }
    });

    $(document).on('click', '.full-desc.active', function(event){
        event.preventDefault();
        deleteExtraData();
    });

    $(document).on('click', '.full-description__close--btn', function() {
        scrollTopToTheBtn(650, 1000)
        deleteExtraData()
    });

    /////////////////////////////////////////////////////////////////////////////////
    ////           MODAL
    /////////////////////////////////////////////////////////////////////////////////

    function displayModal(id, data) {

        // addModalDataDiv
        $(`#${id} .modal-footer`).remove();
        $(`#${id} .modal-body`).remove();
        $(`#${id} .modal-content`).prepend(addModalDataDiv(data));


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


    /////////////////////////////////////////////////////////////////////////////////
    ////           MODAL
    /////////////////////////////////////////////////////////////////////////////////
//    $(document).on('click', '.discount-btn', function(){
//        $('.modal-footer .orange-btn').html('Получить купон');
//    });


    $(document).on('click', '.tab-pane.active', function(event){
        event.preventDefault();
    });
});