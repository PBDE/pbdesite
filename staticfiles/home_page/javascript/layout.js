console.log("Hello, World")

// mobile navigation

const btnNavEl = document.querySelector('.nav-menu-btn');
const navMenuBarEl = document.querySelector('.nav-menu-bar');
const navMenuListEl = document.querySelector('.nav-menu-list');
const mainBlockEl = document.querySelector('.main-block')

btnNavEl.addEventListener('click', function(){
    navMenuListEl.style.transition = "all 0.5s";
    navMenuBarEl.classList.toggle('nav-open');
    mainBlockEl.classList.toggle('behind-nav');
});

// const allLinks = document.querySelectorAll('a:link');

// allLinks.forEach(function(link) {
//     link.addEventListener('click', function(e){
//         e.preventDefault();
//         const href = link.getAttribute('href');
//     })
// })
