"""
Demo Flask application to test the operation of Flask with socket.io

Aim is to create a webpage that is constantly updated with random numbers from a background python process.

30th May 2014

===================

Updated 13th April 2018

+ Upgraded code to Python 3
+ Used Python3 SocketIO implementation
+ Updated CDN Javascript and CSS sources

"""




# Start with a basic flask app webpage.
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from random import random
from time import sleep
from threading import Thread, Event
import sys
import os
import json
import spotipy
import webbrowser
import spotipy.util as util
import colorgram
from google_images_download import google_images_download
import requests
import random
import elements


__author__ = 'slynn'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

prevTrack = ""
#turn the flask app into a socketio app
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

#random number Generator Thread
thread = Thread()
thread_stop_event = Event()

username =  sys.argv[1]
# sys.argv[1]
scope = 'user-read-playback-state streaming user-modify-playback-state user-top-read playlist-modify-public user-read-currently-playing playlist-read-collaborative'

#erase cache and prompt for user permission
try:
    token = util.prompt_for_user_token(username, scope)
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, scope)

#print('well we got past the stupid junk')
#set up spotify object
spotifyObj = spotipy.Spotify(auth=token)

# get cover image so it can be analyzed for bgcolor
def getCoverImage(title):
    query = "{} cover".format(title)

    r = requests.get("https://api.qwant.com/api/search/images",
        params={
            'count': 1,
            'q': query,
            't': 'images',
            'safesearch': 1,
            'locale': 'en_US',
            'uiv': 4
        },
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }
    )

    response = r.json().get('data').get('result').get('items')
    urls = [r.get('media') for r in response]
    return random.choice(urls)

def artistArt(spotifyObj, artistId):
    artist = spotifyObj.artist(artistId)
    # print(json.dumps(artist, indent=4))
    return artist["images"][0]["url"]

def randomNumberGenerator():
    """
    Generate a random number every 1 second and emit to a socketio instance (broadcast)
    Ideally to be run in a separate thread?
    """
    #infinite loop of magical random numbers
    #print("Making random numbers")
    while not thread_stop_event.isSet():
        try:
            songPlayingNow = spotifyObj.current_user_playing_track()["item"]
            #print(json.dumps(songPlayingNow, indent=4))
            songName = songPlayingNow["name"]
            songArtist = songPlayingNow["artists"][0]["name"]
            artistId = songPlayingNow["artists"][0]["id"]
            songAlbum = songPlayingNow["album"]["name"]
            album_cover = songPlayingNow["album"]["images"][0]["url"]
            prevTrack = songPlayingNow
            print("test")
            # album_cover = getCoverImage(songAlbum + " " + songArtist)
            # color = colorgram.extract(album_cover, 1)
            print("heres the color " + color)
        except:
            if(prevTrack == ""):
                songName = "Play a song to start!"
                album_cover = ""
                bgcolor = "#000000"
            else:
                songName = prevTrack["name"]
                songArtist = prevTrack["artists"][0]["name"]
                album_cover = prevTrack["album"]["images"][0]["url"]

        pitchfork_element = elements.pitchforkAbstract(songArtist, songAlbum)

        artistImg = ""
        while(artistImg == ""):
            rand = random.randint(0,2)

            if(rand == 0):
                artistImg = artistArt(spotifyObj, artistId)
            else:
                artistImg = elements.wikipediaImage(songArtist)
                

        if(songName != "Play a song to start!"):
            number = "{} by {}".format(songName, songArtist)
        else:
            number = songName
        #print(number)
        socketio.emit('newnumber', 
        {'number': number, 
        'album_cover': album_cover, 
        'pitchfork_element': pitchfork_element,
        'artist_img': artistImg
        })
        socketio.sleep(5)


@app.route('/')
def index():
    #only by sending this page first will the client be connected to the socketio instance
    return render_template('index.html')

@socketio.on('connect')
def song_connect():
    

    # need visibility of the global thread object
    global thread
    print('Client connected')

    #Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        # important note -- to my knowledge socket tasks cant take arguments
        # this is probably untrue but as of now i've only been able to get it to work by making
        # the vars i need global
        thread = socketio.start_background_task(randomNumberGenerator)

@socketio.on('disconnect')
def song_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app)