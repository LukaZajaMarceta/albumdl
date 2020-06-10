To install ensure ensure you have pip on your system.

Download the folder and while in folder with setup.py from terminal run:

$ pip install .


usage: albumdl [-h] [-o OUTPUT] [-O DEFAULT_OUTPUT] [-c] [-C COMMENT] [-a ALBUM_NAME] [-A] URL

tool to download albums from youtube with sliced songs

positional arguments:
  URL                   url of youtube video

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        folder to save album for this video
  -O DEFAULT_OUTPUT, --default_output DEFAULT_OUTPUT
                        change the default output folder
  -c, --comments        lists the comments that could hold song timestamps
  -C COMMENT, --comment COMMENT
                        selects specific comment to yield song timestamps use -c to see possible options
  -a ALBUM_NAME, --album_name ALBUM_NAME
                        specify album name, default is video name
  -A, --album_folder    if used separate album folder will NOT be created
