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

function getRatingStars(ratingValue, size){
    var starMarkup = '<i class="fas fa-star"></i>',
        rating,
        htmlString = '';

    if (ratingValue && ratingValue != "0"){
        htmlString = '<span class="stars stars-' + (size ? size : 'none') + '" title="' + ratingValue + ' stars">';
        rating = Math.ceil(ratingValue);
        for(var i = 1; i <= rating; i++){
            htmlString += starMarkup;
        }
        htmlString += ratingValue + '</span>';
    } else {
        htmlString += '<small class="text-muted">Be the first to rate this item!</small>';
    }

    return htmlString;
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
        $('div.ratings-info').html(data);
        //alert($('.rating-number').attr('data-rating'), $('.rating-number').attr('data-rating-size'))
        $('.rating-number').html(
            getRatingStars($('.rating-number').attr('data-rating'), $('.rating-number').attr('data-rating-size'))
        );
    })
    .fail(function(error){
        console.log("Error submitting rating.");
        console.log(error);
    });
}
function commentDish(dishId){
    console.log('about to comment on dish via ajax.');
    $.ajax({
        url: dishId + '/comment',
        method: 'POST',
        data: $('.comment-form').serialize(),
    })
    .done(function(data){
        console.log('Successfully  commented.');
        $('div.comments').html(data);
        //alert($('.rating-number').attr('data-rating'), $('.rating-number').attr('data-rating-size'))
    })
    .fail(function(error){
        console.log("Error submitting comment.");
        console.log(error);
    });
}

$('.ratings-form input[type="submit"]').on('click', function(e){
    e.preventDefault();
    var dishId = $(this).closest('.container').attr('data-id');
    rateDish(dishId);
});

// $('.search-form').submit(function(e){
//     e.preventDefault();
//     console.log('AJAX SEARCH:')
//     console.log($('.search-form').serialize());

//     var data = $('.search-form').serialize();
//     data.csrfmiddlewaretoken = getCookie('csrftoken');

//     $.ajax({
//         url: '/search',
//         method: 'GET',
//         data: data,
//     })
//     .done(function(data){
//         console.log(data);
//         $('div.content').html(data);
//     })
//     .fail(function(error){
//         console.log("Error getting search results.");
//         console.log(error);
//     });
// });

$('[data-rating]').html(function(index,oldHTML){
    var rating = $(this).attr('data-rating');
    var size = $(this).attr('data-rating-size') || null;
    return getRatingStars(rating, size);
})

$('.newDish').click(function(e){
    $('#newRating').show()
})

$('.newComment').click(function(e){
    $('#newComment').show()
})

$('.comment-form input[type="submit"]').on('click', function(e){
    e.preventDefault();
    var dishId = $(this).closest('.container').attr('data-id');
    commentDish(dishId);
});