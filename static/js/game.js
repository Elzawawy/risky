var io = io(80);
var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');

const usaCountries = ["Alabama","Alaska","Arizona","Arkansa","California","Colorado","Connecticut","Delaware",  "Florida",  "Georgia",  "Hawaii",  "Idaho",  "Illinois",  "Indiana",  "Iowa","Kansas", "Kentucky",  "Louisiana",  "Maine",  "Maryland",  "Massachusetts",  "Michigan",  "Minnesota", "Mississippi", "Missouri",  "Montana",  "Nebraska", "Nevada",  "New Hampshire",  "New Jersey", "New Mexico",  "New York",  "North Carolina",  "North Dakota", "Ohio",  "Oklahoma", "Oregon",  "Pennsylvinia",  "Rhode Island",  "South Carolina",  "South Dakota",  "Tennessee",  "Texas",  "Utah",  "Vermont",  "Virginia",  "Washington", "West Virginia",  "Wisconsin",  "Wyoming" ];

socket.on('update state', function(msg) {
    var data = JSON.parse(msg.data);
    updateDeplpyments(data)
});




$('form#emit').submit(function(event) {
    socket.emit('my event', {data: $('#emit_data').val()});
    return false;
});
$('form#broadcast').submit(function(event) {
    socket.emit('my broadcast event', {data: $('#broadcast_data').val()});
    return false;
});