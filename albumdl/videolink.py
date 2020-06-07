import pyyoutube
import re
import html2text
from collections import namedtuple
import os
from . import cfg

api_key = cfg.get_key()
api = pyyoutube.Api(api_key=api_key)

re_youtube_url_timestamp = re.compile(r'www.youtube.com/watch\?v=.{11}&amp;t=\d+m\d{2}s')
re_video_id = re.compile(r'(?:\/|%3D|v=|vi=)([0-9A-z-_]{11})(?:[%#?&]|$)')
re_get_time = re.compile(r'((\d{1,2}).{1})?(\d{1,2}).{1}(\d{2})')
SongRecord = namedtuple('SongRecord', ('s', 'end', 'song_name'), defaults=[None, None])
formatter = html2text.HTML2Text()
formatter.ignore_links = True
path = os.path.dirname(os.path.realpath(__file__))


class VideoLink:
    def __init__(self, url):
        self.url = url
        try:
            self.video_id = re_video_id.findall(url)[0]
        except IndexError:
            print('[ERROR] video id could not be found within the link {}, check your URL'.format(url))
        self.video_api_response = api.get_video_by_id(video_id=self.video_id).items[0]
        self.title = self.video_api_response.snippet.title
        self.video_length = self.video_api_response.contentDetails.get_video_seconds_duration()
        self.comments = api.get_comment_threads(video_id=self.video_id, count=10, order='relevance').items
        self.comment_generator = self.gen_fit_comment()
        self.timestamps_comment = None
        self.songs = None

    def get_timestamps_from_comment(self):
        if self.timestamps_comment is None:
            self.timestamps_comment = next(self.comment_generator)

    def print_comments(self):
        i = 1
        for comment in self.comments:
            print('{}. {}'.format(i, comment.snippet.topLevelComment.snippet.textDisplay))
            i += 1

    def set_timestamps_comment(self, i):
        self.timestamps_comment = self.comments[i-1].snippet.topLevelComment.snippet.textDisplay

    # TODO get_timestamps_from_description

    def fitness_comment_timestamps(self, str):
        # how likely is that comment provides song timestamps, lower is better so it is appropriate as sorting key
        n_of_links = len(re_youtube_url_timestamp.findall(str))
        if n_of_links < 2:
            return 10000
        else:
            song_length_assumption = 180
            return abs(self.video_length / n_of_links - song_length_assumption)

    def gen_fit_comment(self):
        ct_by_video = self.comments
        comment_text = [x.snippet.topLevelComment.snippet.textDisplay for x in ct_by_video]
        comment_text.sort(key=self.fitness_comment_timestamps)
        yield from comment_text

    def format_comment(self, comment):
        # TODO make timestamps work with hours
        html = comment
        text = formatter.handle(html)
        song_lst = text.split('\n')
        start_seconds = []
        end_seconds = []
        song_title_lst = []
        # create list of seconds and list of song_titles for each song while excluding lines with no timestamps
        for song in song_lst:
            time = re_get_time.search(song)
            if time:
                hours = int(time.group(2)) if time.group(2) else 0
                minutes = int(time.group(3))
                seconds = int(time.group(4))
                total_seconds = hours * 3600 + minutes * 60 + seconds
                start_seconds.append(total_seconds)
                title = re_get_time.sub('', song).strip()
                song_title_lst.append(title)
        # create list of song endings in s
        end_seconds = start_seconds[1:] + [self.video_length]
        # remove common prefix and suffix from songs titles
        song_title_lst = remove_common_prefix(song_title_lst)
        song_title_lst = remove_common_suffix(song_title_lst)
        # create list of SongRecords
        self.songs = []
        for s, end, title in zip(start_seconds, end_seconds, song_title_lst):
            self.songs.append(SongRecord(s, end, title))

    def __call__(self, output, album_name=None, make_folder=True):
        if not self.timestamps_comment:
            self.timestamps_comment = next(self.comment_generator)
        if not self.songs:
            self.format_comment(self.timestamps_comment)
        if not album_name:
            album_name = self.title
        # download full audio from url with youtube-dl
        print(self.url)
        os.system('youtube-dl -f bestaudio -o "{}/temp/%(title)s.%(ext)s" {}'.format(path, self.url))
        # make new folder for songs
        if make_folder:
            print('[STATUS] creating album directory')
            os.makedirs('{}/{}'.format(output, album_name), exist_ok=True)
            output += "/" + album_name
        # cut the songs with ffmpeg into folder
        for song in self.songs:
            print('[slicing] song to {}/{}.mp4'.format(output, song.song_name))
            os.system('ffmpeg -i "{downloaded_file}" -ss {start} -to {duration} "{output}/{song_name}.mp3"'.format(
                start=song.s,
                downloaded_file="{}/temp/{}.webm".format(path, self.title),
                duration=song.end,
                output=output,
                song_name=song.song_name))


def remove_common_prefix(lst):
    i = 0
    condition = True
    while condition:
        value = lst[0][i]
        for s in lst:
            if s[i] != value and not s[i].isdigit():
                i -= 1
                condition = False
                break
        i += 1
    return [s[i:] for s in lst]


def remove_common_suffix(lst):
    reverse = [s[::-1] for s in lst]
    return [s[::-1] for s in remove_common_prefix(reverse)]