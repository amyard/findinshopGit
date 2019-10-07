(function($){

	"use strict";

/* ==========================================================================
   When document is ready, do
   ========================================================================== */
   
	$(document).ready(function(){

		// sticky header
		// http://imakewebthings.com/jquery-waypoints/shortcuts/sticky-elements/	
	
		var stickyHeader = true;
		
		if((typeof $.fn.waypoint != 'undefined') && stickyHeader && ($(window).width() > 1024)){ 
		
			$('#header').waypoint('sticky', {
			  wrapper: '<div class="sticky-wrapper" />',
			  stuckClass: 'stuck'
			});

		}
		
		// simplePlaceholder - polyfill for mimicking the HTML5 placeholder attribute using jQuery
		// https://github.com/marcgg/Simple-Placeholder/blob/master/README.md
		
		if(typeof $.fn.simplePlaceholder != 'undefined'){
			
			$('input[placeholder], textarea[placeholder]').simplePlaceholder();
		
		}
		
		// Fitvids - fluid width video embeds
		// https://github.com/davatron5000/FitVids.js/blob/master/README.md
		
		if(typeof $.fn.fitVids != 'undefined'){
			
			$('.fitvids').fitVids();
		
		}
		
		// Superfish - enhance pure CSS drop-down menus
		// http://users.tpg.com.au/j_birch/plugins/superfish/options/
		
		if(typeof $.fn.superfish != 'undefined'){
			
			$('#menu').superfish({
				delay: 100,
				animation: {opacity:'show',height:'show'},
				speed: 100,
				cssArrows: false
			});
			
		}
		
		// Revolution Slider
		
		if(typeof $.fn.revolution != 'undefined'){
			
			$('.fullwidthbanner').revolution({
				delay: 9000,
				startheight: 600,
				startwidth: 940,
				hideThumbs: 10,
				thumbWidth: 100,							// Thumb With and Height and Amount (only if navigation Tyope set to thumb !)
				thumbHeight: 50,
				thumbAmount: 5,
				navigationType: "both",					//bullet, thumb, none, both		(No Thumbs In FullWidth Version !)
				navigationArrows: "verticalcentered",	//nexttobullets, verticalcentered, none
				navigationStyle: "round",				//round,square,navbar
				touchenabled: "on",						// Enable Swipe Function : on/off
				onHoverStop: "on",						// Stop Banner Timet at Hover on Slide on/off
				navOffsetHorizontal: 0,
				navOffsetVertical: 0,
				stopAtSlide: -1,
				stopAfterLoops: -1,
				shadow: 0,								//0 = no Shadow, 1,2,3 = 3 Different Art of Shadows  (No Shadow in Fullwidth Version !)
				fullWidth: "on",
				lazyLoad: "on"						// Turns On or Off the Fullwidth Image Centering in FullWidth Modus
			});
				
		}
		
		// bxSlider - responsive slider
		// http://bxslider.com/options
		
		if(typeof $.fn.bxSlider != 'undefined'){
			
			$('#bxslider .slides').bxSlider({
				 mode: 'fade',
				 speed: 500,
				 useCSS:false, 							// fix bug with Jquery 2.1 and mode Horizontal
				 slideMargin: 0,
				 infiniteLoop: true,
				 hideControlOnEnd: false,
				 adaptiveHeight: false,
				 adaptiveHeightSpeed: 500,
				 video: false,
				 pager: true,
				 pagerType: 'full' ,
				 controls: false,
				 //pagerSelector: "#pager",
				 //nextSelector: "#controls", 
				 //prevSelector: "#controls", 
				 auto: true,
				 pause: 4000,
				 autoHover: true
			});
			
			// Testimonial slider
			
			$('#testimonial-slider .slides').bxSlider({
				 mode: 'horizontal',
				 speed: 500,
				 useCSS:false, 							// fix bug with Jquery 2.1 and mode Horizontal
				 slideMargin: 0,
				 infiniteLoop: true,
				 hideControlOnEnd: false,
				 adaptiveHeight: false,
				 adaptiveHeightSpeed: 500,
				 video: false,
				 pager: true,
				 pagerType: 'full' ,
				 controls: false,
				 auto: true,
				 pause: 4000,
				 autoHover: true
			});
			
			// Portfolio items slider
			
			$('#portfolio-items-slider .slides').bxSlider({
				 mode: 'fade',
				 speed: 500,
				 useCSS:false, 							// fix bug with Jquery 2.1 and mode Horizontal
				 slideMargin: 0,
				 infiniteLoop: true,
				 hideControlOnEnd: false,
				 adaptiveHeight: false,
				 adaptiveHeightSpeed: 500,
				 video: false,
				 pager: true,
				 pagerType: 'full' ,
				 controls: false, 
				 auto: true,
				 pause: 4000,
				 autoHover: true
			});
			
			// Portfolio images slider
			
			$('#portfolio-images-slider .slides').bxSlider({
				 mode: 'fade',
				 speed: 500,
				 useCSS:false, 							// fix bug with Jquery 2.1 and mode Horizontal
				 slideMargin: 0,
				 infiniteLoop: true,
				 hideControlOnEnd: false,
				 adaptiveHeight: false,
				 adaptiveHeightSpeed: 500,
				 video: false,
				 pager: true,
				 pagerType: 'full' ,
				 controls: true, 
				 auto: true,
				 pause: 4000,
				 autoHover: true,
				 pagerCustom: '#bx-pager'
			});
			
		}
				
		// Magnific PopUp - responsive lightbox
		// http://dimsemenov.com/plugins/magnific-popup/documentation.html
		
		if(typeof $.fn.magnificPopup != 'undefined'){
		
			$('.magnificPopup').magnificPopup({
				disableOn: 400,
				closeOnContentClick: true,
				type: 'image'
			});
			
			$('.magnificPopup-gallery').magnificPopup({
				disableOn: 400,
				type: 'image',
				gallery: {
					enabled: true
				}
			});
		
		}

		// EasyTabs - tabs plugin
		// https://github.com/JangoSteve/jQuery-EasyTabs/blob/master/README.markdown
		
		if(typeof $.fn.easytabs != 'undefined'){
			
			$('div[id^="tab-"]').easytabs({
				animationSpeed: 300,
				updateHash: false
			});
		
		}
		
		// gMap -  embed Google Maps into your website; uses Google Maps v3
		// http://labs.mario.ec/jquery-gmap/
		
		if(typeof $.fn.gMap != 'undefined'){
		
			$('#google-map').gMap({
				maptype: 'ROADMAP',
				scrollwheel: false,
				zoom: 15,
				markers: [{
						address: 'New York Avenue Northwest, Washington, DC, United States',
						html: '',
						popup: false
					}
				]
			});
		
		}
		
		// Isotope
		// http://isotope.metafizzy.co/beta/
		
		if (typeof $.fn.isotope != 'undefined') {
			
			$('.portfolio-items').imagesLoaded( function() {
			
				var container = $('.portfolio-items');
					
				container.isotope({
					itemSelector: '.item',
					layoutMode: 'masonry'
				});
		
				$('.portfolio-filter li a').click(function () {
					$('.portfolio-filter li a').removeClass('active');
					$(this).addClass('active');
		
					var selector = $(this).attr('data-filter');
					container.isotope({
						filter: selector
					});
		
					return false;
				});
		
				$(window).resize(function () {
		
					container.isotope({ });
				
				});
			
			});
			
		}
		
		// Charts and Graphs
		// http://www.chartjs.org/
		
		if (typeof Chart != 'undefined') {

			// doughnutData
		
			if ($("#canvas-doughnut-data").length > 0) {
		
				var doughnutData = [{
					value: 30,
					color: "#d7dcdb"
				}, {
					value: 70,
					color: "#94ebe3"
				}, {
					value: 120,
					color: "#52a39d"
				}, ];
		
				var myDoughnut = new Chart(document.getElementById("canvas-doughnut-data").getContext("2d")).Doughnut(doughnutData);
		
			}
		
			// barChartData
		
			if ($('#canvas-bar-chart-data').length > 0) {
		
				var barChartData = {
					labels: [" Jan ", " Feb ", " Mar ", " Apr ", " May ", " Jun ", " Jul ", " Aug ", " Sep ", " Oct ", " Nov ", " Dec "],
					datasets: [{
						fillColor: "#94ebe3",
						strokeColor: "#94ebe3",
						data: [11, 12, 14, 15, 20, 18, 18, 20, 22, 26, 30, 34]
					}]
		
				}
		
				var myLine = new Chart(document.getElementById("canvas-bar-chart-data").getContext("2d")).Bar(barChartData);
		
			}
		
			// lineChartData
		
			if ($('#canvas-line-chart-data').length > 0) {
		
				var lineChartData = {
					labels: ["January", "February", "March", "April", "May", "June", "July"],
					datasets: [{
						fillColor: "#d6f3f2",
						strokeColor: "#d6f3f2",
						pointColor: "rgba(220,220,220,1)",
						pointStrokeColor: "#fff",
						data: [65, 59, 90, 81, 56, 55, 40]
					}, {
						fillColor: "#81dad8",
						strokeColor: "#81dad8",
						pointColor: "rgba(151,187,205,1)",
						pointStrokeColor: "#fff",
						data: [28, 48, 40, 19, 96, 27, 100]
					}]
		
				}
		
				var myLine = new Chart(document.getElementById("canvas-line-chart-data").getContext("2d")).Line(lineChartData);
		
			}
		
		}
		
		//

	});
	
/* ==========================================================================
   When the window is scrolled, do
   ========================================================================== */
   	
	$(window).scroll(function () {
							   
		
		
	});

})(window.jQuery);

// non jQuery plugins below