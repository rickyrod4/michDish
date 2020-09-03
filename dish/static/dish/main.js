function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function rateDish(dishId){
    console.log('about to rate dish via ajax.');
    $.ajax({
        url: dishId + '/rate',
        method: 'POST',
        data: $('.ratings-form').serialize(),
    })
    .done(function(data){
        console.log('Successfully rated class.');
        $('div.newRating').html(data);
    })
    .fail(function(error){
        console.log("Error submitting rating.");
        console.log(error);
    });
}

$('.ratings-form input[type="submit"]').on('click', function(e){
    e.preventDefault();
    var dishId = $('#main-content').attr('data-id');
    rateDish(dishId);
});

$('.search-form').submit(function(e){
    e.preventDefault();
    console.log('AJAX SEARCH:')
    console.log($('.search-form').serialize());

    var data = $('.search-form').serialize();
    data.csrfmiddlewaretoken = getCookie('csrftoken');

    $.ajax({
        url: '/search',
        method: 'GET',
        data: data,
    })
    .done(function(data){
        console.log(data);
        $('div.content').html(data);
    })
    .fail(function(error){
        console.log("Error getting search results.");
        console.log(error);
    });
});