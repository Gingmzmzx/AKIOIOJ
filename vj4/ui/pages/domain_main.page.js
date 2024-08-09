import { NamedPage } from 'vj/misc/PageLoader';
import VSwiper from 'vj/components/swiper';

const page = new NamedPage('domain_main', () => {
  $(function(){
    if ($("#swiper")){
      const swiper = new VSwiper("#swiper", [
        {
          href: "/contest/66b31c4e4e6a230001d8011b",
          src: "https://cdn.luogu.com.cn/upload/image_hosting/0l7lzw47.png"
        },
        {
          href: "#",
          src: "https://cdn.luogu.com.cn/upload/image_hosting/k7o1musn.png"
        },
        {
          href: "#",
          src: "https://cdn.luogu.com.cn/upload/image_hosting/wqgk9c1v.png"
        }
      ]);
    }
  });
});

export default page;
