$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    var numbers_received = [];
    var prevSong = "";
    //receive details from server
    socket.on('newnumber', function(msg) {
        console.log("Received number" + msg.number);
        //maintain a list of ten numbers        
        numbers_received = msg.number;
        numbers_string = '';
        numbers_string = '<h1>' + numbers_received.toString() + '</h1>';

        pitchfork_review = "<p style=\"font-size: 30px; text-shadow: 3px 3px #000000\">" + msg.number + "</p> <p>" + msg.pitchfork_element + "</p>";

        $('#songs').html(numbers_string);
        if(prevSong != msg.number){
            album_cover = "<img src=" + msg.album_cover + " class=\"w3-card\"></img>";
            artist_img = "<img src=" + msg.artist_img + " class=\"w3-card img\"></img>";
            $('#album_cover').html(album_cover);
            prevSong = msg.number;
            $('#artist_img').html(artist_img);
            $('#pitchfork_element').html(pitchfork_review);
        }
        //http://i106.photobucket.com/albums/m262/WRWILDCAT55/ravens9_1024x7682.jpg
        coverwUrl = 'url(' + msg.album_cover + ')';
        $("#myBackgroundImage.backgroundImage").css({
            'background': coverwUrl,
                'background-attachment': 'fixed',
                'width': '100vw',
                'height': '100vw',
                'position' : 'absolute',
                'z-index' : '-1',
        });
        $("#myBackgroundImage").css("-webkit-filter", "blur(50px) contrast(1.75) brightness(50%)");
        
        
        
    });

});