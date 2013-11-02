'''
Music Crawler
Crawls ROOT dir and compiles a mapping of song to file path
'''
import os
import sys


music_file_types = [".asf", ".flac", ".m4a", ".ape", ".mp3", ".mpc", ".ogg", ".opus", ".ogv", ".oga", ".ogx", ".spx", ".tta", ".wv", and OptimFROG]

songs = []

'''
crawl_music
params:
    root -- root directory. All music will be crawled from root. Paths to music files will be prepended with root
'''
def crawl_music(root):

    #array of Song objects
    
    if not os.path.isdir(root):
	fail_and_exit("Cannot scrape from "+root+": not a directory");

    walk_dirs(root)

    return songs

def walk_dirs(dir):
    global songs

    for dirname, dirnames, filenames in os.walk(dir):
	# print path to all subdirectories first.
	for subdirname in dirnames:
	    #print "subdirname is "+subdirname
	    #print os.path.join(os.path.abspath(dirname), subdirname)
	    walk_dirs(subdirname)
	
	# print path to all filenames.
	for filename in filenames:
	    #print "filename is "+filename
	    print os.path.join(os.path.abspath(dirname), filename)
	    if os.path.splitext(filename)[1] in music_file_types:
		songs.append(make_new_song(os.path.join(os.path.abspath(dirname), filename))

def fail_and_exit(message):
    print message
    sys.exit(1)

def main():
    crawl_music(sys.argv[1])

main()

class Song:

    def __init__(self, path, track_name, artist, song_length):
	self.path = ""
	self.track_name = ""
	self.artist = ""
	self.song_length = ""




