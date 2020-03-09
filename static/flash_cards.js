$(document).ready(function(){
    // $(".nav-link").css("background-color", "");
    $(".nav-link.active").css("background-color", $(".nav-link.active").find(".parent-color").text());
    $(".nav-link").on( "mouseup", change_color);
});

function change_color() {
    $(".nav-link").css("background-color", "");
    $(this).css("background-color", $(this).find(".parent-color").text())
}