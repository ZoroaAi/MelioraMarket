import { hello } from "./tests.mjs";   
// import { openCloseMenu, openCloseSearch } from "./functions/navSearch.mjs"; 
hello();

// openCloseSearch(); openCloseMenu();

searchButt = document.querySelector("#search-icon");
searchButt.addEventListener("click", () => {
    // Toggle the "search" and "no-search" classes on the "nav" element
    $(".nav").toggleClass("search");
    $(".nav").toggleClass("no-search");
    // Toggle the "search-active" class on the "search-input" element
    $(".search-input").toggleClass("search-active");
});

menuButt = document.querySelector(".menu-toggle");
menuButt.onClick(()=>{
    // Toggle the "mobile-nav" class on the "nav" element
    $(".nav").toggleClass("mobile-nav");
    // Toggle the "is-active" class on the clicked element
    $(this).toggleClass("is-active");
});