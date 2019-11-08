var alertCount = 0;
var totalData = null;

toastr.options = {
    "closeButton": false,
    "debug": false,
    "newestOnTop": false,
    "progressBar": false,
    "positionClass": "toast-bottom-left",
    "preventDuplicates": false,
    "onclick": null,
    "showDuration": "300",
    "hideDuration": "1000",
    "timeOut": "5000",
    "extendedTimeOut": "1000",
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut"
}

// -----------------------------------------------------------------------------
// MQTT Setup ------------------------------------------------------------------
// -----------------------------------------------------------------------------

var client = mqtt.connect();

client.on('connect', function() {
    client.subscribe('dataAlert');
    client.subscribe('allData')
})

client.on('message', function(topic, message) {
    //console.log('received message on %s: %s', topic, message)
    switch (topic) {
        case 'dataAlert':
            newData(JSON.parse(message.toString()));
            break;
    }
})

function newData(message) {
    document.getElementById("myAudio").play();

    var time = message.time;
    var alert = "Area : " + message.area.toString();
    // console.log(alert);

    alertCount += 1;
    document.querySelector('#alertCount').innerHTML = alertCount;

    if ($('#noNotif').length) {
        $('#noNotif').remove();
        $('#alertBody').append("<button class='btn btn-sm btn-info' id='clearButton' onClick='clearNotif()'>Clear Notification </button>");
    }

    $('#alertBody').append("<p class='dropdown-item alert-items'>" + alert + " <span class='badge badge-warning'>" + time + "</span></p>");
    toastr.warning(alert, time);

}

function clearNotif() {
    document.querySelectorAll('.alert-items').forEach(e => e.parentNode.removeChild(e));
    document.querySelector('#clearButton').remove();

    alertCount = 0;
    document.querySelector('#alertCount').innerHTML = alertCount;

    $('#alertBody').append("<p id='noNotif' class='dropdown-item' style='visibility:visible'> No Notification ! </p>");
}
