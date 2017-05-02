$(function() {
    function capitalizeFirstLetter(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }

    // Submit post on submit
    $('#post-form').on('submit', function(event){
        event.preventDefault();
        console.log("form submitted!")  // sanity check
        create_post();
        send_messages();
    });

	$('body').on('click', '#button-delete',function(event){
        event.preventDefault();
        console.log("event for delete stuff!")  // sanity check
        if (confirm(gettext('Are you sure?'))) {
            delete_post($(this).val());
            send_delete();
        }
    });

    function create_post() {

        $.ajax({
            url : "blog/new/", // the endpoint
            type : "POST", // http method
            data : { content : $('#post-content').val(),
                     title : $('#post-title').val()}, // data sent with the post request

            // handle a successful response
            success : function(json) {
                $('#post-content').val(''); // remove the value from the input
                $('#post-title').val(''); // remove the value from the input
                $("#talk").prepend("<div id='post-"+json.slug+"'><h3><a href='blog/"+json.slug+"/'>"+capitalizeFirstLetter(json.title)+"</a></h3><p>"+json.content+"</p><p>"+json.username+"</p><button id='button-delete' value='"+json.slug+"' class='btn btn-default'>"+gettext('Delete')+" <span class='glyphicon glyphicon-pencil'></span></button></div>");
                console.log(json); // log the returned json to the console
                console.log("success"); // another sanity check
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    };

    function delete_post(slug) {

        $.ajax({
            url : "blog/" + slug + '/delete/', // the endpoint
            type : "POST", // http method

            // handle a successful response
            success : function() {
                $("#post-" + slug).remove();
                console.log("success"); // another sanity check
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    };
    
    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    /* --- Echo new message --- */
    // TODO optimize. This Websocket is created each time a form is submitted
    // instead connection need to be initialized once
    function send_messages() {

        var options = {};
        // TODO read from Django settings
        options.port = 1337;
        var ws = new TornadoWebSocket('/messages', options);
        ws.on('open', function (event) {
            ws.on('new_connection', function(data) {
                console.log("new_connection : Message received!");
            });

            // Message sent to all clients
            ws.emit('new_message', {'message': gettext('new message created by ')+ $('#username').text()});

            ws.on('new_message_created', function(data) {
                console.log("new_message_created : Message received!");
                write_message(data);
            });

        });
        ws.on('error', function(event) { console.log(event); });
        ws.on('close', function(event) { console.log(event); });
    }

    /* --- Echo delete --- */
    // TODO optimize. This Websocket is created each time a button is submitted
    // instead connection need to be initialized once
    function send_delete() {

        var options = {};
        // TODO read from Django settings
        options.port = 1337;
        var ws = new TornadoWebSocket('/deletes', options);
        ws.on('open', function (event) {
            ws.on('new_connection', function(data) {
                console.log("new_connection : Delete received!");
            });

            // Message sent to all clients
            ws.emit('delete_action', {'message': gettext('new delete made by ')+ $('#username').text()});

            ws.on('delete_action_made', function(data) {
                console.log("delete_action_made: Delete received!");
                write_message(data);
            });

        });
        ws.on('error', function(event) { console.log(event); });
        ws.on('close', function(event) { console.log(event); });
    }

    function write_message(data) {
        // TODO add timed popup coming from below the web page
        // TODO need translation
        alert(data.message);

    }
});
