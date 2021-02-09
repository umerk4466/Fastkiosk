
// all_events.html 
// date setting
Date.prototype.monthNames = [
    "January", "February", "March",
    "April", "May", "June",
    "July", "August", "September",
    "October", "November", "December"
];

Date.prototype.getMonthName = function() {
    return this.monthNames[this.getMonth()];
};
Date.prototype.getShortMonthName = function () {
    return this.getMonthName().substr(0, 3);
};

// fucntion for getting event
function get_events(city, country, lat, log, next_page, req_type){
    if(req_type == "normal"){
        // url with country and city url
        custom_url = "https://app.ticketmaster.com/discovery/v2/events.json?size=20&city="+city+"&country="+country+"&sort=date,asc&apikey=mrJCAMRTt9ufDC8TLAceC2DHXOQ75kBo"
    }
    else if(req_type == "next"){
        custom_url = "https://app.ticketmaster.com/discovery/v2/events.json?size=20&city="+city+"&country="+country+"&page="+next_page+"&sort=date,asc&apikey=mrJCAMRTt9ufDC8TLAceC2DHXOQ75kBo"
    }
    $.ajax({
        type:"GET",
        url: custom_url,
        async:true,
        dataType: "json",
        success: function(data) {
            if (data.hasOwnProperty("_embedded")){
                // get total number of event and set to heading
                var total_events = data.page.totalElements;
                $('p#ticketmaster-heaiding').html("Found <strong>"+total_events+"</strong> events in "+city)
                var events = data._embedded.events;
                // check if there are more pages get next page number
                var total_pages = data.page.totalPages;
                var current_page = data.page.number;
                //  add button to the bottom for loading next pages
                if (current_page < total_pages){
                    // add button attribbute and show in the page
                    $("#load-more-event").attr("data-current-page" , current_page);
                    $("#load-more-event").removeClass("d-none");
                    $("#go-top-btn").removeClass("d-none");
                }
                // else remove the button
                else{
                    $("#load-more-event").remove();
                }
                $.each(events, function(index, value) {

                    var date = new Date(value.dates.start.localDate);
                    // get venue data
                    if (value.hasOwnProperty("_embedded")){
                        venue = value._embedded.venues
                        $.each(venue, function(index, val){
                        // append the event to the all event page
                        $('#third-party-events').append("<div class='events-box'><div class='media'><h1 class='mb-0 mr-2 text-primary font-weight-normal'>"+date.getDate()+"</h1><div><p class='font-weight-bold mb-0 text-dark'>"+date.getShortMonthName()+"</p><p class='mb-0'>"+date.getFullYear()+"</p></div><div class='media-body ml-4'><p class='text-dark font-weight-bold mb-0'><a href='"+value.url+"' class='text-dark' target='_blank'>"+value.name+"</a></p><p class='mb-0'><span>"+val.name+", "+val.city.name+", "+val.country.name+"</span></p></div></div><hr></div>");
                        
                        });
                    }
                });
            }
            else{
                $.alert("No Events Fount in "+city+", "+country)
                $('#third-party-events').html("<h6 class='font-wight-normal'>No Events listed in "+city+", "+country+". Search in other city<h6>")

            }
            // console.log(data._embedded.events);
        },
        error: function(xhr, status, err) {
                    $.alert("!!!Error, Could not load the events from 'Ticketmaster' try again!")
                }
    });
}

// empty varbale for storing the serch data
var city;
var country;
// fucntion on serch click button
$('#event-search-form').submit(function( event ) {
    event.preventDefault();
    // make default page view
    $('.events-box').remove()
    $("#load-more-event").addClass("d-none");
    $("#go-top-btn").addClass("d-none");
    $('p#ticketmaster-heaiding').html('Search Events Form "Ticketmaster"')
    // get city data from the getcitydetails function and check if the are not empty
    if(city || country ){
        // send the ajax to the masterticket with the serch values
        get_events(city=city, country=country, lat=null, log=null, next_page=null ,req_type="normal");
    }
    else{
        $.alert("Error!!! Please select the valid place")
        $("#f_elem_city").val("")
    }
});

// function to get data of the user seched are
function getcitydetails(fqcn) {

	if (typeof fqcn == "undefined") fqcn = jQuery("#f_elem_city").val();
	cityfqcn = fqcn;
	if (cityfqcn) {
        jQuery.getJSON("https://secure.geobytes.com/GetCityDetails?key=7c756203dbb38590a66e01a5a3e1ad96&callback=?&fqcn="+cityfqcn,
                        function (data) {
                            city = data.geobytescity
                            country = data.geobytescountry
            }
        );
	}
}

// auto complete the city names funtion
function autofil() 
{
    jQuery("#f_elem_city").autocomplete({
    source: function (request, response) {
        jQuery.getJSON(
        "https://secure.geobytes.com/AutoCompleteCity?key=7c756203dbb38590a66e01a5a3e1ad96&callback=?&q="+request.term,
        function (data) {
            response(data);
        }
        );
    },
    minLength: 3,
    select: function (event, ui) {
        var selectedObj = ui.item;
        jQuery("#f_elem_city").val(selectedObj.value);

    getcitydetails(selectedObj.value);
        return false;
    },
    open: function () {
        jQuery(this).removeClass("ui-corner-all").addClass("ui-corner-top");
    },
    close: function () {
        jQuery(this).removeClass("ui-corner-top").addClass("ui-corner-all");
    }
    });
    jQuery("#f_elem_city").autocomplete("option", "delay", 100);    
}


// run auto complete function on input select
$('#f_elem_city').click( function(){
    autofil();
});

$(document).ready(function() {
    $("a#load-more-event").click(function () {
        // e.preventDefault();
        var current_page = $(this).attr("data-current-page");
        var next_page = parseInt(current_page) + 1;
        toString(next_page);
        get_events(city=city, country=country, lat=null, log=null, next_page=next_page ,req_type="next");
    });
});
