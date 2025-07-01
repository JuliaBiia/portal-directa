/* full screen */
function openFullscreen() {
    var elem = document.documentElement;
    let open = $(".full-screen-open");
    let close = $(".full-screen-close");

    if (!document.fullscreenElement && !document.webkitFullscreenElement && !document.msFullscreenElement){
        localStorage.setItem('wasFullScreen', 'true');
        if (elem.requestFullscreen) {
            elem.requestFullscreen();
        } else if (elem.webkitRequestFullscreen) {
            /* Safari */
            elem.webkitRequestFullscreen();
        } else if (elem.msRequestFullscreen) {
            /* IE11 */
            elem.msRequestFullscreen();
        }
        close.addClass("d-block").removeClass("d-none");
        open.addClass("d-none").removeClass("d-block");
    } else {
        localStorage.setItem('wasFullScreen', 'false');
        if (document.exitFullscreen) {
            document.exitFullscreen();
        } else if (document.webkitExitFullscreen) {
            /* Safari */
            document.webkitExitFullscreen();
            console.log("working");
        } else if (document.msExitFullscreen) {
            /* IE11 */
            document.msExitFullscreen();
        }
        close.removeClass("d-block").addClass("d-none");
        open.removeClass("d-none").addClass("d-block");
    }
}
/* full screen */