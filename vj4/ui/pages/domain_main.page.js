import { NamedPage } from 'vj/misc/PageLoader';
import VSwiper from 'vj/components/swiper';
import Truncate from 'vj/components/truncate';

const page = new NamedPage('domain_main', () => {
  $(function(){
    var swiper_dom = $("#swiper_list");
    if (swiper_dom && $("#swiper")){
      console.log("Loading swiper...");

      var swiper_list = [];
      swiper_dom.children().each((idx, element) => {
        swiper_list.push({
          href: element.getAttribute("data-href"),
          src: element.getAttribute("data-src"),
        })
      });
      console.log("Swiper_list:", swiper_list);

      const swiper = new VSwiper("#swiper", swiper_list);
    }

    new Truncate('.truncate', 40);
  });
});

export default page;
