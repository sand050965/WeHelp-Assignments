let sideMenu = document.getElementById("side-menu");

function openSideMenu() {
    let event = window.event;
    sideMenu.style.width = "250px";
    event.stopPropagation();
}

function closeSideMenu() {
    if (sideMenu.style.width  == "250px") {
        sideMenu.style.width  = "0px";    
    }
}