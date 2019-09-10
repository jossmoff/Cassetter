import glob
import os.path
import json
import simpleaudio as sa
import pygame
from omc import OnlineMediaConverter

class CassetteMaker():
    def __init__(self):
        self.all_tracks = self._get_songs_from_media()
        self.cassette_track_list = []
        self.name = ''
        self.filename = '.cst'

    def _get_songs_from_media(self):
        songs = []
        for filename in glob.glob(os.path.join('media/', '*.wav')):
            songs.append(filename)
        songs = list(map(lambda x: x.replace('media\\', ''), songs))
        return songs

    def print_songs(self):
        print('TRACKS')
        for index, track in enumerate(self.all_tracks):
            print(" " + str(index + 1) + " > " + track.replace('media\\', ''))
    
    def add_song(self, index):
        self.cassette_track_list.append(self.all_tracks[index])

    def add_cassette_name(self, filename):
        self.name = filename
        self.filename = filename + '.cst'
    
    def export(self):
        with open('.cache/mappings.JSON', 'r') as f:
            mappings = json.loads(f.read())
        tracks_data = [self.name]
        with open('cassettes/' + self.filename, 'w') as f:
            for track in self.cassette_track_list:
                tracks_data.append([track] + mappings[track])
            json.dump(tracks_data, f)
        
        return Cassette(self.name, self.cassette_track_list)

    def import_cassette(self, string):
        #[["Mall Grab - Glitch Finisher.wav", "https://www.youtube.com/watch?v=4mtfCl5J78c", [3500, 3908]]]
        # url, filename, clip_times=()
        tracks_data = json.loads(string)
        self.add_cassette_name(tracks_data[0])
        download_arr = []
        for track_data in tracks_data[1:]:
            download_arr.append([track_data[1], track_data[0], (track_data[2][0], track_data[2][1])])
            self.cassette_track_list.append(track_data[0])

        return download_arr



class Cassette:
    def __init__(self, filename, track_list):
        self.cassette_track_list = track_list
        self.name = filename

    def get_track_list(self):
        return self.cassette_track_list

class CassettePlayer():
    def __init__(self):
        self.track_list = []
        self.track_wav_objs = []
        pygame.mixer.init()
    
    def load(self, cassette):
        self.track_list = cassette.get_track_list()
        self._convert_to_wav_objs()

    def play(self):
        max_item_length = len(max(self.track_list, key=len))
        for index, track in enumerate(self.track_list):
            track_obj = self.track_wav_objs[index]
            print('Playing : ' + '' * (max_item_length - len(track)) + track, end='\r')
            play_obj = track_obj.play()
            play_obj.wait_done() 

    def _convert_to_wav_objs(self):
        for track in self.track_list:
            wave_obj = sa.WaveObject.from_wave_file('media/' + track)
            self.track_wav_objs.append(wave_obj)

        



    