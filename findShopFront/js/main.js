$(document).ready(function () {

    //////////////////////////////////////////////////////////////////////////////////////
    //            tabulation
    //////////////////////////////////////////////////////////////////////////////////////
    $('body').on('click', '.nav-tabs li', function (){
        $('.nav-tabs li').removeClass('active');
        $(this).addClass('active');
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
        $('.full-desc').removeClass('active');
        $('.product-item').css({'opacity': '1'});
        $('.testtest').remove();
        $('.delete-empty').remove();
    }

    $(document).on('click', '.full-desc', function(event){
        event.preventDefault();

        

        deleteExtraData();        


        var classBtn = $(this).attr('class'),
            allItems = $('.product-item'),
            btnItemBlock = $(this).parent().parent(),
            windowWidth = $(window).width(),
            getPosition = getCurrentPosition(),
            correctItem = '',
            amountOfItems = $('.product-item').length;

        function getCurrentPosition() {
            if (windowWidth > 1472) {
                return 5
            } else if (1280 < windowWidth < 1472) {
                return 4
            }
        }


        // первый раз нажали на кнопку
        if(!classBtn.includes('active')) {
            $(this).addClass('active');

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

                arr.forEach(function(value){
                    jQuery(currDiv).after(addSecondDataForBorrom())
                })

                last = jQuery($('.delete-empty').last())
                last.after(addDataDiv(title))
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
                                                <li class="active"><a href="#home" aria-controls="home" role="tab" data-toggle="tab">Домой</a></li>\
                                                <li><a href="#profile" aria-controls="profile" role="tab" data-toggle="tab">Профиль</a></li>\
                                                <li><a href="#messages" aria-controls="messages" role="tab" data-toggle="tab">Сообщения</a></li>\
                                                <li><a href="#settings" aria-controls="settings" role="tab" data-toggle="tab">Настройки</a></li>\
                                            </ul>\
                                            
                                            <div class="tab-content">\
                                                <div role="tabpanel" class="tab-pane active" id="home">\
                                                    <h3>${title}</h3>\
                                                    <p>Динамические закрытого типа - Частотные характеристики 5 Гц - 22000 Гц - Чувствительность 102 дБ / мВт - сопротивление 24 Ом (1 кГц) - микрофон есть...</p>\
                                                    <h2>1199 грв</h2>\
                                                </div>\
                                                <div role="tabpanel" class="tab-pane" id="profile">\
                                                    
                                                </div>\
                                                <div role="tabpanel" class="tab-pane" id="messages">\
                        
                                                </div>\
                                                <div role="tabpanel" class="tab-pane" id="settings">\
                                                    
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

            function addSecondDataForBorrom() {
                return `<div class='col-1-of-4 product-item delete-empty' style='opacity: 0;'></div>`
            }
        } 
    });

    $(document).on('click', '.active', function(event){
        event.preventDefault();
        deleteExtraData();
    })

    $(document).on('click', '.full-description__close--btn', function() {
        $('.testtest').remove();
        $('.product-item').css({'opacity': '1'});
        deleteExtraData()
    })
});
