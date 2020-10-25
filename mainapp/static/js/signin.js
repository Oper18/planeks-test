function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Check if this cookie string begin with the name we want
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
             }
         }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function sendAJAX(data, uri, e) {
    $.ajax({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        },
        url: uri,
        type: 'POST',
        data: data,
        success: function(response){
            console.log(response);
            window.location.replace(window.location.origin + response['redirect'])
        },
        error: function(response){
            $('#danger-mes').css('display', 'block');
            console.log(response);
        }
    });
}

function Login(e) {
    var u = $('#username-input-id').val();
    var p = $('#password-input-id').val();
    var csrfmiddlewaretoken = $('[name=csrfmiddlewaretoken').val();
    var data = {'username': u, 'password': p, 'csrfmiddlewaretoken': csrfmiddlewaretoken, 'uri': window.location.href};

    sendAJAX(data, '/ajax/login/', e.target);
}

function checkReportStatus(filename) {
    let csrfmiddlewaretoken = $('[name=csrfmiddlewaretoken').val();
    var data = {'csrfmiddlewaretoken': csrfmiddlewaretoken, 'filename': filename};
    $.ajax({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        },
        url: '/ajax/check_report_status/',
        type: 'POST',
        data: data,
        success: function(response){
            console.log(response);
            $('.csv-maker-wait').css('display', 'none');
            $('#csv-download-id').attr('href', response['link']);
            $('.csv-download').css('display', 'block');
        },
        error: function(response){
            console.log(response);
            setTimeout(function() {checkReportStatus(filename);}, 10000);
        }
    });
}

function MakeCSV(e) {
    $.ajax({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        },
        url: '/ajax/make_csv/',
        type: 'GET',
        success: function(response){
            console.log(response);
            $('.csv-maker-btn').css('display', 'none');
            $('.csv-maker-wait').css('display', 'block');
            checkReportStatus(response['filename']);
        },
        error: function(response){
            console.log(response);
        }
    });
}

function createRecord(e) {
    let csrfmiddlewaretoken = $('[name=csrfmiddlewaretoken').val();
    let first_name = $('#first-name-input-id').val();
    if (first_name == '') {
        first_name = null;
    }
    let last_name = $('#last-name-input-id').val();
    if (last_name == '') {
        last_name = null;
    }
    let job = $('#job-name-input-id').val();
    if (job == '') {
        job = null;
    }
    let type = $('#type-name-input-id').val();
    if (!['1', '2', '3', '4'].includes(type)) {
        type = '1';
    }
    let website = $('#website-name-input-id').val();
    if (website == '') {
        website = null;
    }
    let date = $('#date-name-input-id').val();
    if (date == '') {
        date = null;
    }
    let info = $('#info-name-input-id').val();
    if (info == '') {
        info = null;
    }
    var data = {csrfmiddlewaretoken, first_name, last_name, job, type, website, date, info};
    $.ajax({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        },
        url: '/ajax/add_record/',
        type: 'POST',
        data: data,
        success: function(response){
            console.log(response);
            location.reload();
        },
        error: function(response){
            console.log(response);
        }
    });
}

$(document).ready(function(){
    $('#signin-btn').on('click', Login);
    $('#logout-btn').on('click', function(e){
        $.ajax({
            url: '/ajax/logout/',
            type: 'GET',
            success: function(response) {
                window.location.replace(window.location.origin + response['redirect']);
            },
            error: function(response) {
                console.log(response);
                $('#invite-mes-label').text('Some went wrong, try later');
                $('#invite-mes-label').css('display', 'block');
            }
        })
    })
    $('#make-csv-id').on('click', MakeCSV);
    $('#create-record').on('click', createRecord);
})