var is_nav_open = false;

function openNav() {
    document.getElementById("sideMenu").style.transform = "translateX(0)";
    document.getElementById("blackLayer").style.opacity = "0.2";
    document.getElementById("blackLayer").style.zIndex = "3";

    is_nav_open = true;
}

function closeNav() {
    document.getElementById("sideMenu").style.transform = "translateX(400px)";
    document.getElementById("blackLayer").style.opacity = "0";
    document.getElementById("blackLayer").style.zIndex = "-100";

    is_nav_open = false;
}

// document.addEventListener('click', function(e){
//     var side_menu = document.getElementById('sideMenu');
//     var profile_div = document.getElementById('profileDiv');
//     if (!side_menu.contains(e.target) && (!profile_div.contains(e.target))){
//         closeNav();
//     }
// })
