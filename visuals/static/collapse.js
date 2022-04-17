$(document).ready(function(){
    $('.expandbar').click(function(){
        let box = $(this).closest('.box');
        if ( box.hasClass('collapsed') ){
            box.removeClass('collapsed');
            box.find("fade").remove();
            box.find(".expandbar").html("<span style='font-size:30px;'>&#x2303</span>")
        } else{
            box.addClass('collapsed');
            box.append("<fade/>");
            box.find(".expandbar").html("<span style='font-size:30px;'>&#x2304</span>")
        }
    });
});