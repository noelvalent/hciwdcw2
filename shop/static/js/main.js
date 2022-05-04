$(function(){
    // Header fade-in / fade-out
    $(document).on('scroll', function(){
        if($(window).scrollTop() > 30){
            $("#header").removeClass("deactive");
            $("#header").addClass("active");
        }else{
            $("#header").removeClass("active");
            $("#header").addClass("deactive");
        }
    })

    // Burger menu icon / full page menu
    $('.hamburger-button').on('click', function(event){
        event.preventDefault();
        
        $(this).toggleClass('active');
        $('.overlay').toggleClass('visible');

    });
});

curryear = new Date().getFullYear();
document.getElementById("year").innerHTML = curryear;

// Search action
function searchToggle(obj, evt){
    const container = $(obj).closest('.search-wrapper');
    if(!container.hasClass('active')){
            container.addClass('active');
            evt.preventDefault();
    }
    else if(container.hasClass('active') && $(obj).closest('search-wrapper')) {
        location.href = `?q=${document.getElementById('store-search-input').value}`;
    }
    else if(container.hasClass('active') && $(obj).closest('.input-holder').length === 0){
        container.removeClass('active');

        // clear input
        container.find('.search-input').val('');
    }
}
