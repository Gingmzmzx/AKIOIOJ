import Swiper from 'swiper/swiper-bundle.mjs';
import 'swiper/swiper-bundle.css';

export default class VSwiper {
  constructor(swiperContainer, imgLists) {
    var h5Str = `
      <!-- Additional required wrapper -->
      <div class="swiper-wrapper">
        <!-- Slides -->`;

    for (const i in imgLists) {
      const img = imgLists[i];
      h5Str += `
        <div class="swiper-slide">
          <a href="${img.href}"><img src="${img.src}" ></a>
        </div>`;
    }

    h5Str += `</div>
    <div class="swiper-pagination"></div>
    <div class="swiper-button-prev"></div>
    <div class="swiper-button-next"></div>`;

    $(swiperContainer).html(h5Str);
    this.swiper_container = swiperContainer;
    this.imgLists = imgLists;
    // init Swiper:
    this.swiper = new Swiper(swiperContainer, {
      autoplay: {
        delay: 3000,
      },
      pagination: {
        el: '.swiper-pagination',
      },
      navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
      },
    });
  }
}
