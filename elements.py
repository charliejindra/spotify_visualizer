from pitchfork_api.pitchfork import search
import json
import wikipedia
import random
import pylast

#returns the bold abstract at the beginning of a review
def pitchforkAbstract(qArtist, qAlbum):
    p = ""

    try:
        print(qArtist,qAlbum[:10])
        p = search(qArtist, qAlbum[:10])
    except:
        return ""
    
    return p.abstract()

def wikipediaImage(qArtist):
    image = 'Commons-logo'
    try:
        while ('logo' in image) or ('.ogg' in image) or '.svg' in image:
            image = wikipedia.page(qArtist).images[random.randint(0,len(wikipedia.page(qArtist).images)-1)]
    except:
        return ""
    print(wikipedia.summary(qArtist, sentences=2))
    print(image)
    return image

def lastFmImage(qArtist):
    last = pylast.LastFMNetwork(api_key='a5e5f45db701bf491f5faa4f600a20a7', api_secret='84193a97c6b955860e0d880ef1bf0a9d')
    artist = last.get_artist('Radiohead')
    img = artist.get_cover_image()
    print(img)


#pitchforkAbstract("Sufjan Stevens", "Illinois")
#wikipediaImage('Unknown Mortal Orchestra')
#lastFmImage('test')