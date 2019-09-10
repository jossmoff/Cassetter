from __future__ import unicode_literals
from omc import OnlineMediaConverter
from cassettes import CassettePlayer, CassetteMaker
import youtube_dl
import os
import os.path
import subprocess
import shutil
import configparser
import json
import glob


__version__ = "0.1.0"

BANNER = [r"""   ____________________________""",
r""" /|............................|""",
r"""| |:          Cassetter       :|""",
r"""| |:        Joss Moffatt      :|""",
r"""| |:     ,-.   _____   ,-.    :|""",
r"""| |:    ( `)) [_____] ( `))   :|""",
r"""|v|:     `-`   ' ' '   `-`    :|""",
r"""|||:     ,______________.     :|""",
r"""|||...../::::o::::::o::::\.....|""",
r"""|^|..../:::O::::::::::O:::\....|""",
r"""|/`---/--------------------`---|""",
r"""`.___/ /====/ /=//=/ /====/____/""",
r"""     `--------------------'"""]

MENU_OPTIONS = ['Clip Music', 'Create Cassette', 'View Cassettes', 'Share Cassettes', 'Import Cassettes', 'Settings']

YDL_OPTS = {
            'format': 'bestaudio/best',
            'outtmpl': 'download.wav'
        }

def read_config():
    parser = configparser.ConfigParser()
    parser.read('config.ini')
    extension = parser.get('DEFAULTS', 'EXTENSION')
    cache_limit = int(parser.get('DEFAULTS', 'CACHE_LIMIT'))
    return extension, cache_limit

def print_menu(banner_arr, options_arr):
    longest_item_length = len(max(banner_arr, key=len))
    width = shutil.get_terminal_size()[0]
    offset = (width - longest_item_length) // 2
    for index, line in enumerate(banner_arr):
        print((" " * offset) + line )
    for index, line in enumerate(options_arr):
        print((" " * offset) + str(index + 1) + ") " + line )
    return offset

def existing_file(filename):
    return os.path.isfile('media/' + filename)

def set_mapping(file_id, arr):
    with open('.cache/mappings.JSON', 'r') as f:
        mapping_dict = json.loads(f.read())
    mapping_dict[file_id] = arr
    with open('.cache/mappings.JSON', 'w') as f:
        f.write(json.dumps(mapping_dict))

#TODO wrap these up in an object Cassette maker
def get_cassettes():
    cassettes = []
    for filename in glob.glob(os.path.join('cassettes/', '*.cst')):
        cassettes.append(filename)
    return cassettes

def print_cassettes(cassettes):
    for index, cassette in enumerate(cassettes):
        print(' ' +  str(index + 1) + " > " + cassette.replace('cassettes\\', ''))

def main():
    offset = print_menu(BANNER, MENU_OPTIONS)
    # Read in config varspo 
    extension, cache_limit = read_config()
    while 1:
        try:
            menu_option = int(input('\n' + " " * offset + 'Enter your choice > '))
        except ValueError:
            print('Enter a valid number.') 
        else:
            if not (1 <= menu_option < len(MENU_OPTIONS)):
                print('Enter a valid number.') 
            else:
                menu_option -= 1
                break
    if MENU_OPTIONS[menu_option] == 'Clip Music':

        url = input("Enter Media URL > ")
        while True:
            title = input("Enter Desired Filename > ")
            output_filename = title + '.' + extension
            if not existing_file(output_filename):
                break
            else:
                print("This file already exists, try again")
        #TODO validate inputs
        print('Press [ENTER] to ignore clips')
        start_clip = input('Enter Start Timestamp for Clip > ')
        if len(start_clip) == 0:
            clip_times = ()
        else:
            end_clip = int(input('Enter End Timestamp for Clip > '))
            clip_times = (int(start_clip),end_clip)
        
        converter = OnlineMediaConverter(YDL_OPTS, extension, cache_limit)
        converter.download_from_url(url, output_filename, clip_times=clip_times)
        set_mapping(output_filename, [url, clip_times])

    elif MENU_OPTIONS[menu_option] == 'Create Cassette':
        cassette_name = input('Enter Cassette name > ')
        cassette_maker = CassetteMaker()
        cassette_maker.add_cassette_name(cassette_name)
        cassette_maker.print_songs()
        print('\n Press [ENTER] to finish selecting')
        #TODO validate input
        while True:
            track_index = input('Enter your selection > ')
            if len(track_index) == 0:
                break
            else:
                track_index = int(track_index) - 1
                cassette_maker.add_song(track_index)
        cassette = cassette_maker.export()
        cassette_player = CassettePlayer()
        cassette_player.load(cassette)
        cassette_player.play()

    elif MENU_OPTIONS[menu_option] == 'View Cassettes':
        cassettes = get_cassettes()
        print('CASSETTES')
        print_cassettes(cassettes)

    elif MENU_OPTIONS[menu_option] == 'Share Cassettes':
        cassettes = get_cassettes()
        print('CASSETTES')
        print('\n Press [ENTER] to return')
        print_cassettes(cassettes)
        while True:
            try:
                cassette_index = int(input('Enter the cassette you want to share > '))
            except ValueError:
                print('[ERROR] That is not a valid number')
            else:
                cassette_index = cassette_index - 1
                break

    elif MENU_OPTIONS[menu_option] == 'Import Cassettes':
        cassette_string = input('Input Share data > ')
        cassette_maker = CassetteMaker()
        download_items = cassette_maker.import_cassette(cassette_string)
        converter = OnlineMediaConverter(YDL_OPTS, extension, cache_limit)
        for download_item in download_items:
            url = download_item[0]
            output_filename = download_item[1]
            clip_times = download_item[2]
            converter.download_from_url(url, output_filename, clip_times=clip_times)
            set_mapping(output_filename, [url, clip_times])
        cassette = cassette_maker.export()
        cassette_player = CassettePlayer()
        cassette_player.load(cassette)
        cassette_player.play()
        


    


if __name__ == '__main__':
    main()


"""
'ffmpeg -i peter.wav out.wav'


t1 = 0
t2 = 60
convert_to_pcm(output_filename,t1,t2)

audio_abs_path = os.path.abspath(pcm_filename)
newAudio = AudioSegment.from_wav(audio_abs_path)
newAudio = newAudio[t1:t2]
newAudio.export(output_filename, format=file_format) #Exports to a wav file in the current path.
"""

