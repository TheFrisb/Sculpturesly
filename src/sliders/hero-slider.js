import Splide from "@splidejs/splide";

export function initHeroSlider() {
   new Splide('.splide--heroSection', {
     type: "loop",
     height: "100vh",
     perPage: 1,
     autoplay: true,
     interval: 7000,
   }).mount();
}