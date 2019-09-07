import youtube_dl
import subprocess
import os.path
import shutil
import os
import json

class OnlineMediaConverter(youtube_dl.YoutubeDL):
    def __init__(self, options, extension, cache_limit):
        super().__init__(options)
        self.options = options
        self.id = ""
        self.extension = '.' + extension
        self.cache_limit = cache_limit

    def download_from_url(self, url, filename, clip_times=()):
        video_id = 'yt-' + self._get_id(url)
        input_path = './download.wav'
        if not self._check_cache(video_id):
            self.download([url])
            self._convert_to_pcm(input_path, filename, clip_times)
            # Move one file to cache and other to media
            self._move_to_folder("./download.wav", ".cache/" + video_id + self.extension)
        else:
            input_path = '.cache/'+ video_id + self.extension
            # TODO MAKE _convert_to_pcm take a location to convert from
            self._convert_to_pcm(input_path, filename, clip_times)


    def _get_id(self, url):
      if "youtube.com/watch?v=" in url:
        return url.replace('https://www.youtube.com/watch?v=', '')
      else:
        raise Exception('Currently only Youtube is supported.')

    def _convert_to_pcm(self, input_path, output_filename, clip_times):
        if isinstance(clip_times, tuple):
            if len(clip_times) == 0:
                output = subprocess.getoutput(['ffmpeg', '-i', input_path, 
                                                output_filename])
                return output
            elif len(clip_times) == 2:
                start_time = clip_times[0]
                end_time = clip_times[1]
                return self._convert_to_pcm_clip(input_path, output_filename, start_time, end_time)
            else:
                 raise TypeError('Clip times must be in the form (start_time, end_time)')
        else:
            raise TypeError('Clip times must be in the form (start_time, end_time)')

    def _convert_to_pcm_clip(self, input_path, output_filename, start_time, end_time):
        output = subprocess.getoutput(['ffmpeg', '-i', input_path,
                                      '-ss', str(start_time), '-to',
                                       str(end_time), 'media/' + output_filename])
        return output
    
    def _move_to_folder(self, current_path, output_path):
        if os.path.isfile(current_path) and not os.path.isfile(output_path)  :
            shutil.move(current_path, output_path)
        else:
            raise Exception('''Please enter valid current_path and move_path 
                                and ensure move_path does not already exist''')

    def _check_cache(self, video_id):
        return(os.path.isfile('.cache/'+ video_id + self.extension))

        