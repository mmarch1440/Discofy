import spotipy
import spotipy.util as util
from securityCredentials import USERNAME
from securityCredentials import PLAYLISTID
from securityCredentials import CLIENTID
from securityCredentials import CLIENTSECRET

SCOPE = 'playlist-modify-public'
REDIRECT = 'http://localhost/8888/callback/'
SPTOKEN = util.prompt_for_user_token(USERNAME, SCOPE, CLIENTID, CLIENTSECRET, REDIRECT)
sp = spotipy.Spotify(auth=SPTOKEN)

def addSong(songID):
    return sp.user_playlist_add_tracks(USERNAME, PLAYLISTID, songID)

def getTopSongByAtistThenTitle(artist,song):
    results = sp.search(q='artist:' + artist + ' track:' + song,limit=1,offset=0,type='track',market='GB')
    for i, t in enumerate(results['tracks']['items']):
        return [t['id']]

def getTopSongByTitle(song):
    results = sp.search(q='track:' + song,limit=1,offset=0,type='track',market='GB')
    for i, t in enumerate(results['tracks']['items']):
        return [t['id']]