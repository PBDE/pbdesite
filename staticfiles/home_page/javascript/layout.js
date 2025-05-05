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

// smooth scrolling

// const allLinks = document.querySelectorAll('a:link');

// allLinks.forEach(function(link) {
//     link.addEventListener('click', function(e){
//         e.preventDefault();
//         const href = link.getAttribute('href');
//     })
// })


// svg line animation

var paths = document.querySelectorAll("svg path"), i=0;

paths.forEach(function(path, index){
    
    i++;

    var pathLength = path.getTotalLength();

    path.setAttribute("stroke-dasharray", pathLength);
    path.setAttribute("stroke-offset", pathLength);

    path.innerHTML = "<animate attributeName='stroke-dashoffset' begin='0s' dur='3s' to='0' fill='freeze' />"
    
    console.log(index, pathLength, path.innerHTML);
});
