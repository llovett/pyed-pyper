'''
Music Crawler
Crawls ROOT dir and compiles a mapping of song to file path
'''
import os
import sys

import audiotools


#music_file_types = [".asf", ".flac", ".m4a", ".ape", ".mp3", ".mpc", ".ogg", ".opus", ".ogv", ".oga", ".ogx", ".spx", ".tta", ".wv", ".ofr"]
music_file_types = [".m4a",".mp3", ".ogg", ".wav"]

# global dictionary of song information
songs = []

'''
crawl_music
params:
    root -- root directory. All music will be crawled from root. Paths to music files will be prepended with root
'''
def crawl_music(root_dirs):
    global songs

    for root in root_dirs:
	if not os.path.isdir(root):
	    fail_and_exit("Cannot scrape from "+root+": not a directory");

	walk_dirs(root)

    return songs

'''
recursively walk through all directories given root directory dir
'''
def walk_dirs(dir):
    global songs
    num_song = 0
    for dirname, dirnames, filenames in os.walk(dir):
	# print path to all subdirectories
	for subdirname in dirnames:
	    walk_dirs(subdirname)
	
	# print path to all filenames
	for filename in filenames:
	    file_extension = os.path.splitext(filename)[1]
	    if file_extension in music_file_types:
		song = {}
		song["full_path"] = os.path.join(os.path.abspath(dirname), filename)
		song[file_extension] = song["full_path"]
		try:
		    song_audio_file = audiotools.open(song["full_path"])
		except Exception as e:
		    print "Could not open file: "+song["full_path"]+". Error: "+str(e)
		    continue #skip song
		try:
		    song_metadata = song_audio_file.get_metadata()
		    if song_metadata == None:
			continue
		except Exception as e:
		    print "Could not open get file metadata: "+song["full_path"]+". Error: "+str(e)
		    continue #skip song
		
		song["title"] = song_metadata.track_name
		song["artist"] = song_metadata.artist_name
		song["album"] = song_metadata.album_name
		song["number"] = song_metadata.track_number
		song["year"] = song_metadata.year

		#if len(song.items()) > 2: #only store the song if there is information besides pathname and extension
		songs.append(song)

def fail_and_exit(message):
    print message
    sys.exit(1)

def main():
    crawl_music([sys.argv[1]])
    for song in songs:
	print "song_title is "+song["title"]
	print "artist_name is "+song["artist"]
	print "album_name is "+song["album"]
	print "track_name is "+str(song["number"])
	print "year is "+song["year"]

main()

