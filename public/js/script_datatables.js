function updateTable(allData) {
    var datatable = $('#table1').DataTable();
    datatable.destroy();
    $('#table1').DataTable({
        "iDisplayLength": 5,
        "bAutoWidth": true,
        searching: true,
        processing: true,
        "lengthChange": false,
        "bFilter": true,
        "info": false,
        columns: [{
                data: 'Id'
            },
            {
                data: 'Date'
            },
            {
                data: 'Time'
            },
            {
                data: 'Area'
            },
            // {
            //     data: 'Filename',
            //     render: function(data, type, row, meta) {
            //         if (type === 'display') {
            //             data = '<a href="./data/VidLog/' + data + '">' + data + '</a>';
            //         }
            //         return data;
            //     }
            // }
        ],
        data: allData,

    })
    console.log("Table Updated")
}

$(document).ready(function() {
    $('#table1').DataTable({
        data: null,
        columns: [{
                data: 'Id'
            },
            {
                data: 'Date'
            },
            {
                data: 'Time'
            },
            {
                data: 'Area'
            },
            // {
            //     data: 'Filename',
            //     render: function(data, type, row, meta) {
            //         if (type === 'display') {
            //             data = '<a href="./data/VidLog/' + data + '">' + data + '</a>';
            //         }
            //         return data;
            //     }
            // }
        ],
        "iDisplayLength": 5,
        "bAutoWidth": true,
        searching: true,
        processing: true,
        "lengthChange": false,
        "bFilter": true,
    })
    // console.log("ANCANG")
});

function updateStatus(messageAll){
  for (i=0; i<messageAll.length; i++){
    var message = messageAll[i];
    var area_span = document.querySelector('#area'+message.Area);
    if (message.Status){
      area_span.style.backgroundColor = '#d9534f';
    } else if (!message.Status) {
      area_span.style.backgroundColor = '#5cb85c';
    }
  }
}

client.on('message', function(topic, message) {
    //console.log('received message on %s: %s', topic, message)
    switch (topic) {
        case 'allData':
            updateTable(JSON.parse(message.toString()));
            break;
        case 'allStatus':
            meall = JSON.parse(message.toString());
            updateStatus(JSON.parse(message.toString()));
            break;
    }
})
