var brokerIp = 'localhost:1884'

// ----------------------------------------------------------

String.prototype.format = function() {
    var i = 0,
        args = arguments;
    return this.replace(/{}/g, function() {
        return typeof args[i] != 'undefined' ? args[i++] : '';
    });
};

//---------------------------------------------------------------

// Setup MySQL
var mysql = require('mysql');
var fs = require('fs');

var con = mysql.createConnection({
    host: 'localhost',
    user: 'ntust-iot',
    password: 'prasetyo12',
    database: 'ntust-iot_datalog',
});

con.connect(function(err) {
    if (err) throw err;
    console.log("MySQL Connected!");
})
// --------------------------------------------------------------

// Setup Server
var brokerAddress = "localhost";
var brokerPort = 1884;
var httpAddress = "localhost";
var httpPort = 3003;

// Embedded Mosca initialization
var mosca = require("mosca");
var server = new mosca.Server({
    // host: brokerAddress,
    port: brokerPort,
    http: {
        // host: httpAddress,
        port: httpPort,
        bundle: true,
        static: './public/'
    },
    persistence: {
        factory: mosca.persistence.Memory // so i can use retain function
    },
});

// Triggered when server status is ready
server.on('ready', function() {
    console.log('-------------------------------')
    console.log('Mosca Broker is up and running in %s:%s !', brokerAddress, brokerPort)
    console.log('Using %s:%s for HTTP and MQTT over Web-Sockets !', httpAddress, httpPort)
    console.log('-------------------------------')
    console.log('')

    con.query('select * from `log-alert`;', function(err, results, fields) {
      client.publish('allData', JSON.stringify(results), {retain:true})
    });
})

// Triggered when a client connected
server.on('clientConnected', function(client) {
    console.log('BROKER : client connected (%s)', client.id)
})

// Triggered when a client disconnected
server.on('clientDisconnected', function(client) {
    console.log('BROKER : client disconnected (%s)', client.id)
})

// Triggered when a message received
server.on('published', function(packet, client) {
    console.log('MESSAGE : %s', packet.payload.toString('utf-8'))
})

//---------------------------------------------------------------

var mqtt = require("mqtt")
var client = mqtt.connect('mqtt://' + brokerIp);

client.on('connect', function() {
    client.subscribe('dataAlert')
})

client.on('message', function(topic, message) {
    //console.log('received message on %s: %s', topic, message)
    message = JSON.parse(message.toString())
    switch (topic) {
        case 'dataAlert':
            if(message.status){
                newData(message);
            }
            break;
    }
})

function newData(message) {
    var sql = "INSERT INTO `log-alert` (`Date`, `Time`, `Area`, `Filename`) VALUES ( '{}', '{}', {}, '{}')".format(message.date, message.time, message.area, message.filename);
    con.query(sql, function(err, result) {
        if (err) throw err;
        console.log(message.filename + " inserted");
    });

    con.query('select * from `log-alert`;', function(err, results, fields) {
      client.publish('allData', JSON.stringify(results), {retain:true});
    });
}
