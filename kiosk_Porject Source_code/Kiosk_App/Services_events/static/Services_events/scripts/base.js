// used in some pages this loading gif for ajax and loading
// show animation until page is not loaded
$(window).on('load', function() {
    $(".loader").fadeOut();
    $(document)
        .ajaxStart(function () {
            $(".loader").show();
        })
        .ajaxStop(function () {
            $(".loader").hide();
        });
});

// ajax******************************
// book_event.html
// ajax for changing student data
$('input[id="id_student_roll_no"], input[id="id_course_name"], input[id="id_cource_finish"]').change(function(){
    $("#student_form_btn").removeAttr('disabled');
});
$("#student_form_btn").on('click', function () {
    var course_name = $('input[id="id_course_name"]').val();
    var student_roll_no = $('input[id="id_student_roll_no"]').val();
    var cource_finish = $('input[id="id_cource_finish"]').val();
    var endpoint = $(this).attr("data-url");

    $.ajax({
    url: endpoint,
    data: {
        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
        'course_name': course_name,
        'student_roll_no': student_roll_no,
        'cource_finish' : cource_finish,
    },
    dataType: 'json',
    success: function (data) {
        if (data.success) {
        alert("Your information is updated successfuly!!!");
        $("#student_form_btn").attr('disabled', 'disabled');
        }else{
        alert("Error!!! Something is wrong please check you connection and make sure you roll number is unique.");
        }
    }
    });

});

// specific_event_booking.html
// ajax call for deleting the event booking
$("#delete_event_booking_btn").on('click', function () {
    var endpoint = $(this).attr("data-url");
    $.ajax({
    url: endpoint,
    data: {
        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
    },
    dataType: 'json',
    success: function (data) {
        if (data.success) {
        window.location.replace(data.redirect_url);
        }else{
            $('.confirm-cancel-model').modal('hide')
            $('.container-fluid').prepend("<div class='alert alert-danger alert-dismissible' role='alert'>Error!!! Could not delete this booking, something is wrong please check you connection and try again.</div>")
        }
    }
    });
});


// ajax call for deleting the service booking
$("#delete_service_booking_btn").on('click', function () {
    var endpoint = $(this).attr("data-url");
    $.ajax({
    url: endpoint,
    data: {
        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
    },
    dataType: 'json',
    success: function (data) {
        if (data.success) {
        window.location.replace(data.redirect_url);
        }else{
            $('.confirm-cancel-model').modal('hide')
            $('.container-fluid').prepend("<div class='alert alert-danger alert-dismissible' role='alert'>Error!!! Could not delete this booking, something is wrong please check you connection and try again.</div>")
        }
    }
    });
});


// my_bookings.html
$( document ).ready(function() {
    $('table tr .not-approved-yet').each(function() { 
        var td =  $(this).text();     
        if (td === 'Not Approved yet'){
            $(this).addClass("text-secondary shadow-sm");
        }
        else{
            $(this).addClass("text-primary shadow-sm");
        }
    });
});

$( document ).ready(function() {
    $('table tr .status').each(function() { 
        var td =  $(this).text();     
        if (td === 'Pending'){
            $(this).addClass("text-danger shadow-sm");
        }
        else{
            $(this).addClass("text-success shadow-sm");
        }
    });
});


// add_service.html
$( document ).ready(function() {
    // id of below button is same as model which is in the template for adding new category
    var add_category_btn = $("<button data-toggle='modal' type='button' data-target='#add_category_model' class='btn btn-outline-dark btn-sm my-2'>Add New Category</button>").appendTo('#add_service_form #div_id_category').trigger( 'create' );
    $('#add_service_form #id_category').change(function(){
        if($('#add_service_form #id_category :selected').val() == ''){
            add_category_btn.appendTo('#add_service_form #div_id_category').trigger( 'create' );
        }
        else{
            add_category_btn.remove()
        }
    });
});


// specific_event.html
$('.delete-my-event-btn').click(function(event) {
    event.preventDefault();
    $.confirm({
        title: 'Delete Event ???',
        content: 'Are you sure you want to delete this event??? <br>This will also delete all the <strong>bookings</strong> related to this event',
        autoClose: 'cancel|8000',
        buttons: {
            deleteEvent: {
                text: 'Yes Delete it',
                btnClass: 'btn-danger',
                action: function () {
                    var event_delete_url = $('.delete-my-event-btn').attr('data-del-url')
                    window.location = event_delete_url;
                }
            },
            cancel: {
                btnClass: 'btn-primary',
                action:  function () {}
            },
        }
    });
});


// specific_service.html

$('.delete-my-service-btn').click(function(event) {
    event.preventDefault();
    $.confirm({
        title: 'Delete Service ???',
        content: 'Are you sure you want to delete this service??? <br>This will also delete all the <strong>bookings</strong> related to this service',
        autoClose: 'cancel|8000',
        buttons: {
            deleteService: {
                text: 'Yes Delete it',
                btnClass: 'btn-danger',
                action: function () {
                    var service_delete_url = $('.delete-my-service-btn').attr('data-del-url')
                    window.location = service_delete_url;
                }
            },
            cancel: {
                btnClass: 'btn-primary',
                action:  function () {}
            },
        }
    });
});

// booking_requests.html
$(".confirm_service_btn").on('click', function (event) {
    event.preventDefault();
    var endpoint = $(this).attr("data-url");
    var tr_id = $(this).attr("data-tr");

    $.ajax({
    url: endpoint,
    data: {
    },
    dataType: 'json',
    success: function (data) {
        if (data.success) {
            // get tr of this row
            var tr = $('tr#'+tr_id);
            // get span with badge class and change to the confirm
            var span_badge = tr.find('span.badge')
            span_badge.removeClass("badge-warning");
            span_badge.text("Confirmed")
            span_badge.addClass("badge-success");
            // remove confirm button of this tr
            var confirm_button = tr.find('.confirm_service_btn');
            confirm_button.remove();
            $.alert({
                title: 'Confirmed!!!',
                content: 'Booking have been confirmed',
            });
        }else{
            $.alert({
                title: 'Error!!!',
                content: 'Could not confirm this booking please try again',
            });
        }
    }
    });

});


// cancel service booking
$(".cancel_service_btn").on('click', function (event) {
    event.preventDefault();
    var endpoint = $(this).attr("data-url");
    var tr_id = $(this).attr("data-tr");

    $.ajax({
    url: endpoint,
    data: {
    },
    dataType: 'json',
    success: function (data) {
        if (data.success) {
            // remove the tabe this table row
            var tr = $('#'+tr_id);
            tr.remove();
            $.alert({
                title: 'Canceled!!!',
                content: 'Booking have been cancel successfully!!!',
            });
        }else{
            $.alert({
                title: 'Error!!!',
                content: 'Could not delete this booking please try again',
            });
        }
    }
    });

});

// events
$(".confirm_event_btn").on('click', function (event) {
    event.preventDefault();
    var endpoint = $(this).attr("data-url");
    var tr_id = $(this).attr("data-tr");

    $.ajax({
    url: endpoint,
    data: {
    },
    dataType: 'json',
    success: function (data) {
        if (data.success) {
            // get tr of this row
            var tr = $('tr#'+tr_id);
            // get span with badge class and change to the confirm
            var span_badge = tr.find('span.badge')
            span_badge.removeClass("badge-warning");
            span_badge.text("Confirmed")
            span_badge.addClass("badge-success");
            // remove confirm button of this tr
            var confirm_button = tr.find('.confirm_event_btn');
            confirm_button.remove();
            $.alert({
                title: 'Confirmed!!!',
                content: 'Booking have been confirmed',
            });
        }else{
            $.alert({
                title: 'Error!!!',
                content: 'Could not confirm this booking please try again',
            });
        }
    }
    });

});


// cancel event booking
$(".cancel_event_btn").on('click', function (event) {
    event.preventDefault();
    var endpoint = $(this).attr("data-url");
    var tr_id = $(this).attr("data-tr");

    $.ajax({
    url: endpoint,
    data: {
    },
    dataType: 'json',
    success: function (data) {
        if (data.success) {
            // remove the tabe this table row
            var tr = $('#'+tr_id);
            tr.remove();
            $.alert({
                title: 'Canceled!!!',
                content: 'Booking have been cancel successfully!!!',
            });
        }else{
            $.alert({
                title: 'Error!!!',
                content: 'Could not delete this booking please try again',
            });
        }
    }
    });

});
