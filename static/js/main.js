/* ===================================================================
 * Calvin 1.0.0 - Main JS
 *
 * ------------------------------------------------------------------- */

(function($) {

    "use strict";
    
    const cfg = {
                scrollDuration : 800, // smoothscroll duration
                mailChimpURL   : ''   // mailchimp url
                };

    // Add the User Agent to the <html>
    // will be used for IE10/IE11 detection (Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0; rv:11.0))
    // const doc = document.documentElement;
    // doc.setAttribute('data-useragent', navigator.userAgent);


   /* Preloader
    * -------------------------------------------------- */
    const ssPreloader = function() {

        const preloader = document.querySelector('#preloader');
        if (!preloader) return;

        document.querySelector('html').classList.add('ss-preload');
        
        window.addEventListener('load', function() {
            
            document.querySelector('html').classList.remove('ss-preload');
            document.querySelector('html').classList.add('ss-loaded');

            preloader.addEventListener('transitionend', function(e) {
                if (e.target.matches("#preloader")) {
                    this.style.display = 'none';
                }
            });
        });

        // force page scroll position to top at page refresh
        // window.addEventListener('beforeunload' , function () {
        //     window.scrollTo(0, 0);
        // });

    }; // end ssPreloader


   /* Mobile Menu
    * ---------------------------------------------------- */ 
    const ssMobileMenu = function() {

        const $navWrap = $('.s-header__nav-wrap');
        const $closeNavWrap = $navWrap.find('.s-header__overlay-close');
        const $menuToggle = $('.s-header__toggle-menu');
        const $siteBody = $('body');
        
        $menuToggle.on('click', function(e) {
            e.preventDefault();
            e.stopPropagation();

            $siteBody.addClass('nav-wrap-is-visible');
        });

        $closeNavWrap.on('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
        
            if($siteBody.hasClass('nav-wrap-is-visible')) {
                $siteBody.removeClass('nav-wrap-is-visible');
            }
        });

        // open (or close) submenu items in mobile view menu. 
        // close all the other open submenu items.
        $('.s-header__nav .has-children').children('a').on('click', function (e) {
            e.preventDefault();

            if ($(".close-mobile-menu").is(":visible") == true) {

                $(this).toggleClass('sub-menu-is-open')
                    .next('ul')
                    .slideToggle(200)
                    .end()
                    .parent('.has-children')
                    .siblings('.has-children')
                    .children('a')
                    .removeClass('sub-menu-is-open')
                    .next('ul')
                    .slideUp(200);

            }
        });

    }; // end ssMobileMenu


   /* Search
    * ------------------------------------------------------ */
    const ssSearch = function() {

        const searchWrap = document.querySelector('.s-header__search');
        const searchTrigger = document.querySelector('.s-header__search-trigger');

        if (!(searchWrap && searchTrigger)) return;

        const searchField = searchWrap.querySelector('.s-header__search-field');
        const closeSearch = searchWrap.querySelector('.s-header__overlay-close');
        const siteBody = document.querySelector('body');

        searchTrigger.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();

            siteBody.classList.add('search-is-visible');
            document.querySelector('.s-content').style.filter = "blur(5px)";
            /*searchWrap.querySelector('.s-header__search-field').focus();*/
            searchWrap.querySelector('.s-header__search-field').focus();
        });

        closeSearch.addEventListener('click', function(e) {
            e.stopPropagation();

            if(siteBody.classList.contains('search-is-visible')) {
                siteBody.classList.remove('search-is-visible');
                document.querySelector('.s-content').style.filter = "blur(0px)";
                searchWrap.querySelector('.s-header__search-field').blur();
            }
        });

        searchWrap.addEventListener('click', function(e) {
            if( !(e.target.matches('.s-header__search-inner')) ) {
                //closeSearch.dispatchEvent(new Event('click'));
            }
        });

        searchField.addEventListener('click', function(e) {
            e.stopPropagation();
        })

        searchField.setAttribute('placeholder', 'Search for...');
        searchField.setAttribute('autocomplete', 'off');

    }; // end ssSearch


   /* Masonry
    * ------------------------------------------------------ */
    const ssMasonry = function() {
        const containerBricks = document.querySelector('.bricks-wrapper');
        if (!containerBricks) return;

        imagesLoaded(containerBricks, function() {

            const msnry = new Masonry(containerBricks, {
                itemSelector: '.entry',
                columnWidth: '.grid-sizer',
                percentPosition: true,
                resize: true
            });

        });

    }; // end ssMasonry


   /* Slick Slider
    * ------------------------------------------------------ */
    const ssSlickSlider = function() {

        const $animateEl = $('.animate-this');
        const $heroSlider = $('.s-hero__slider');

        $heroSlider.on('init', function(event, slick){
            setTimeout(function() {
                $animateEl.first().addClass('animated');
            }, 500);
        });

        $heroSlider.slick({
            arrows: false,
            dots: true,
            speed: 1000,
            fade: true,
            cssEase: 'linear',
            autoplay: false,
            autoplaySpeed: 5000,
            pauseOnHover: false
        });

        $heroSlider.on('beforeChange', function(event, slick, currentSlide){
            $animateEl.removeClass('animated');
        });    
        $heroSlider.on('afterChange', function(event, slick, currentSlide){
            $animateEl.addClass('animated');
        });

        $('.s-hero__arrow-prev').on('click', function() {
            $heroSlider.slick('slickPrev');
        });

        $('.s-hero__arrow-next').on('click', function() {
            $heroSlider.slick('slickNext');
        });

    }; // end ssSlickSlider


   /* Animate on Scroll
    * ------------------------------------------------------ */
    const ssAOS = function() {
        
        AOS.init( {
            offset: 100,
            duration: 800,
            easing: 'ease-in-out',
            delay: 400,
            once: true,
            disable: 'mobile'
        });

    }; // end ssAOS


   /* Alert Boxes
    * ------------------------------------------------------ */
    const ssAlertBoxes = function() {

        const boxes = document.querySelectorAll('.alert-box');

        boxes.forEach(function(box) {

            box.addEventListener('click', function(e){
                if (e.target.matches(".alert-box__close")) {
                    e.stopPropagation();
                    e.target.parentElement.classList.add("hideit");

                    setTimeout(function() {
                        box.style.display = "none";
                    }, 500)
                }    
            });

        })

    }; // end ssAlertBoxes


   /* Smooth Scrolling
    * ------------------------------------------------------ */
    const ssSmoothScroll = function() {
        
        $('.smoothscroll').on('click', function (e) {
            const target = this.hash;
            const $target = $(target);
            
            e.preventDefault();
            e.stopPropagation();

            $('html, body').stop().animate({
                'scrollTop': $target.offset().top
            }, cfg.scrollDuration, 'swing').promise().done(function () {
                window.location.hash = target;
            });
        });

    }; // end ssSmoothScroll


   /* Back to Top
    * ------------------------------------------------------ */
    const ssBackToTop = function() {

        const pxShow = 900;
        const goTopButton = document.querySelector(".ss-go-top");

        if (!goTopButton) return;

        // Show or hide the button
        if (window.scrollY >= pxShow) goTopButton.classList.add("link-is-visible");

        window.addEventListener('scroll', function() {
            if (window.scrollY >= pxShow) {
                if(!goTopButton.classList.contains('link-is-visible')) goTopButton.classList.add("link-is-visible")
            } else {
                goTopButton.classList.remove("link-is-visible")
            }
        });

    }; // end ssBackToTop
    
    
    /* Pagination API
     * ----------------------------------------------------- */
    const ssAPI = function () {
    
    $('.pgn__num.idx, .pgn__next.idx, .pgn__prev.idx').click(function () {
        const page_size = 12;
        let page_no = 0;

        if ($(this).text() == 'Next') {
            var isNext = true;
            page_no = parseInt($('.pgn__num.idx.current').text()) + 1;
        } else if ($(this).text() == 'Prev' && parseInt($('.pgn__num.idx.first').text()) > 1) {
            var isPrev = true;
            page_no = parseInt($('.pgn__num.idx.current').text()) - 1;
        } else {
            page_no = parseInt($(this).text());
        }

        const data = JSON.stringify({page: page_no, page_size: page_size});
        const url = $('a.logo').attr('href') + 'api/page';

        $.ajax({
            type: 'POST',
            url: url,
            data: data,
            contentType: 'application/json',
            dataType: 'json',
            success: function (page_posts) {
                if (!page_posts) {
                    return;
                } else {
                    if (page_posts.data) {
                        $('article.brick.entry').remove();
                        for (const i in page_posts.data) {
                            const artHtml = `<article class="brick entry" data-aos="fade-up">
    
                        <div class="entry__thumb">
                            <a href="${$('a.logo').attr('href')}post/${(page_posts.data)[i].route}" class="thumb-link">
                                <img src="${(page_posts.data)[i].image_url}" 
                                     srcset="images/thumbs/masonry/macbook-600.jpg 1x, images/thumbs/masonry/macbook-1200.jpg 2x" alt="">
                            </a>
                        </div> <!-- end entry__thumb -->
    
                        <div class="entry__text">
                            <div class="entry__header">
                                <h1 class="entry__title"><a href="${$('a.logo').attr('href')}post/${(page_posts.data)[i].route}">${(page_posts.data)[i].title}</a></h1>
                                
                                <div class="entry__meta">
                                    <span class="byline"">By:
                                        <span class='author'>
                                            ${(page_posts.data)[i].posted_by}
                                    </span>
                                </span>
                                    <span class="cat-links">
                                    </span>
                                </div>
                            </div>
                            <div class="entry__excerpt">
                                <p>
                                ${(page_posts.data)[i].dex}
                                </p>
                            </div>
                            <a class="entry__more-link" href="${$('a.logo').attr('href')}post/${(page_posts.data)[i].route}">Read More</a>
                        </div> <!-- end entry__text -->
                    
                    </article>`;
                    $('div.bricks-wrapper.h-group').append(artHtml);
                        }
                    }
                }
                if (isNext) {
                    $('.pgn__num.idx').each(function (index) {
                        $(this).text(parseInt($(this).text()) + 1);
                    });
                } else if (isPrev) {
                    $('.pgn__num.idx').each(function (index) {
                        $(this).text(parseInt($(this).text()) - 1);
                    });
                } else {
                    $('a.pgn__num.idx.current').removeClass('current');
                    $(this).addClass(function () {
                        console.log(`${$(this).text()} : is the current page.`);
                        return 'current';
                    });
                }
                ssMasonry();
                ssAOS();
                ssSmoothScroll();
            }
            });
        });
    
        
        $('.pgn__num.cat, .pgn__next.cat, .pgn__prev.cat').click(function () {
        const page_size = 12;
        let page_no = 0;

        if ($(this).text() == 'Next') {
            var isNext = true;
            page_no = parseInt($('.pgn__num.cat.current').text()) + 1;
        } else if ($(this).text() == 'Prev' && parseInt($('.pgn__num.cat.first').text()) > 1) {
            var isPrev = true;
            page_no = parseInt($('.pgn__num.cat.current').text()) - 1;
        } else {
            page_no = parseInt($(this).text());
        }

        const data = JSON.stringify({page: page_no, page_size: page_size});
        const url = $('a.logo').attr('href') + 'api/page/category';

        $.ajax({
            type: 'POST',
            url: url,
            data: data,
            contentType: 'application/json',
            dataType: 'json',
            success: function (page_posts) {
                if (!page_posts) {
                    return;
                } else {
                    if (page_posts.data) {
                        $('article.brick.entry').remove();
                        for (const i in page_posts.data) {
                            const artHtml = `<article class="brick entry" data-aos="fade-up">
    
                        <div class="entry__thumb">
                            <a href="${$('a.logo').attr('href')}${(page_posts.data)[i].route}" class="thumb-link">
                                <img src="${(page_posts.data)[i].image_url}" 
                                     srcset="images/thumbs/masonry/macbook-600.jpg 1x, images/thumbs/masonry/macbook-1200.jpg 2x" alt="">
                            </a>
                        </div> <!-- end entry__thumb -->
    
                        <div class="entry__text">
                            <div class="entry__header">
                                <h1 class="entry__title"><a href="${$('a.logo').attr('href')}${(page_posts.data)[i].route}">${(page_posts.data)[i].title}</a></h1>
                                
                                <div class="entry__meta">
                                    <span class="byline"">By:
                                        <span class='author'>
                                            ${(page_posts.data)[i].posted_by}
                                    </span>
                                </span>
                                    <span class="cat-links">
                                    </span>
                                </div>
                            </div>
                            <div class="entry__excerpt">
                                <p>
                                ${(page_posts.data)[i].dex}
                                </p>
                            </div>
                            <a class="entry__more-link" href="${$('a.logo').attr('href')}${(page_posts.data)[i].route}">Read More</a>
                        </div> <!-- end entry__text -->
                    
                    </article>`;
                    $('div.bricks-wrapper.h-group').append(artHtml);
                        }
                    }
                }
                if (isNext) {
                    $('.pgn__num.cat').each(function (index) {
                        $(this).text(parseInt($(this).text()) + 1);
                    });
                } else if (isPrev) {
                    $('.pgn__num.cat').each(function (index) {
                        $(this).text(parseInt($(this).text()) - 1);
                    });
                } else {
                    $('a.pgn__num.cat.current').removeClass('current');
                    console.log('remove class should work');
                    $(this).addClass(function () {
                        console.log(`${$(this).text()} : is the current page.`);
                        return 'current';
                    });
                }
                ssMasonry();
                ssAOS();
                ssSmoothScroll();
            }
            });
        });
    };



   /* initialize
    * ------------------------------------------------------ */
    (function ssInit() {

        ssPreloader();
        ssMobileMenu();
        ssSearch();
        ssMasonry();
        ssSlickSlider();
        ssAOS();
        ssAlertBoxes();
        ssSmoothScroll();
        ssBackToTop();
        ssAPI();
    })();

})(jQuery);
