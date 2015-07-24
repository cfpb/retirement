$(document).ready(function (){
    $('.toggle-menu').on('click', function(ev){
        ev.preventDefault();
        $('nav.main ul').toggleClass('vis');
    });
});
