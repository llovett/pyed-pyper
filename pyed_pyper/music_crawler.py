'''
Music Crawler
Crawls ROOT dir and compiles a mapping of song to file path
'''

'''
TODO
----
-m4a support --DONE
-mp3 support --DONE
-wav support --done?
-ogg support --Done
-print out dependencies when failure to open file
-support for song w/o metadata info
'''
import os
import sys
import pickle
import audiotools


#music_file_types = [".asf", ".flac", ".m4a", ".ape", ".mp3", ".mpc", ".ogg", ".opus", ".ogv", ".oga", ".ogx", ".spx", ".tta", ".wv", ".ofr"]
MUSIC_FILE_TYPES = [".m4a",".mp3", ".ogg", ".wav"]
PYED_PYPER_ROOT_DIR = "/home/liz/code/pyed-pyper"
GENERATED_DIR = PYED_PYPER_ROOT_DIR+"/generated"
SONG_CACHE_FILE = GENERATED_DIR+"/cached_songs.pickle"
TIMESTAMP_CACHE_FILE = GENERATED_DIR+"/cached_timestamps.pickle"

'''
dir_needs_scraping(dir)

- determines whether the given directory needs to be scraped by comparing
  its last modified time with the modified time in TIMESTAMP_CACHE_FILE
- updates contents of TIMESTAMP_CACHE_FILE if necessary
'''
def dir_needs_scraping(dir):
    if not os.path.exists(GENERATED_DIR):
	os.makedirs(GENERATED_DIR)
    try:
	timestamp_cache_file = open(TIMESTAMP_CACHE_FILE, 'r')
	cached_timestamps = pickle.load(timestamp_cache_file)
	if os.path.getmtime(dir) > cached_timestamps[dir]:
	    cached_timestamps[dir] = os.path.getmtime(dir)
	    timestamp_cache_file = open(TIMESTAMP_CACHE_FILE, 'w')
	    pickle.dump(cached_timestamps, timestamp_cache_file)
	    return True
	else:
	    return False
    except IOError:
	#no song_cache_file
	timestamp_cache_file = open(TIMESTAMP_CACHE_FILE, 'w')
	cached_time_stamps = { dir : os.path.getmtime(dir) }
	pickle.dump(cached_time_stamps, timestamp_cache_file)
	return True

'''
crawl_music
checks to see if the given directories need to be crawled using a pickled dictionary with "filename" => timestamp
returns pickled dictionary if 
params:
    root -- root directory. All music will be crawled from root. Paths to music files will be prepended with root
'''
def crawl_music(root_dirs):
    songs = []
    for root in root_dirs:
	if not os.path.isdir(root):
	    fail_and_exit("Cannot scrape from "+root+": not a directory");

	scrape_dir = dir_needs_scraping(root)
	if scrape_dir or not os.path.exists(SONG_CACHE_FILE):
	    songs.extend(walk_dirs(root))
	    song_cache_file = open(SONG_CACHE_FILE, 'w')
	    pickle.dump(songs, song_cache_file)
	else:
	    songs.extend(walk_dirs(root))
	    songs = pickle.load(song_cache_file)

    return songs


'''
recursively walk through all directories given root directory dir
'''
def walk_dirs(dir):
    num_song = 0
    songs = []
    for dirname, dirnames, filenames in os.walk(dir, followlinks=True):
	# print path to all subdirectories
	for subdirname in dirnames:
	    songs.extend(walk_dirs(subdirname))

	options = {"verbosity":"normal"}
	msg = audiotools.Messenger("music_crawler", options)
	# print path to all filenames
	for filename in filenames:
	    file_extension = os.path.splitext(filename)[1]
	    if file_extension in MUSIC_FILE_TYPES:
		song = {}
		song["full_path"] = os.path.join(os.path.abspath(dirname), filename)
		song[file_extension[1:]] = song["full_path"]
		try:
		    #using open_files because it supports a messenger object
		    song_audio_file = audiotools.open_files([song["full_path"]], messenger=msg)
		    if len(song_audio_file) > 0:
			song_audio_file = song_audio_file[0]
		    else:
			print "couldn't open dat file: "+filename
			continue
		except Exception as e:
		    print "Could not open file: "+song["full_path"]+". Error: "+str(e)
		    continue #skip song
		try:
		    song_metadata = song_audio_file.get_metadata()
		except Exception as e:
		    print "Could not open get file metadata: "+song["full_path"]+". Error: "+str(e)
		    continue #skip song

		if song_metadata is None:
		    song["title"] = os.path.splitext(filename)[0]
		    song["artist"] = "Unknown artist"
		    song["album"] = "Unknown album"
		    song["number"] = "Unknown track #"
		    song["year"] = "1337"
		else:
		    song["title"] = song_metadata.track_name if song_metadata.track_name else filename
		    song["artist"] = song_metadata.artist_name if song_metadata.artist_name else "Unknown artist"
		    song["album"] = song_metadata.album_name if song_metadata.album_name else "Unknown album"
		    song["number"] = song_metadata.track_number if song_metadata.track_number else "Unknown track number"
		    song["year"] = song_metadata.year if song_metadata.year else "Unknown year"

		#if len(song.items()) > 2: #only store the song if there is information besides pathname and extension
		songs.append(song)
    return songs

def fail_and_exit(message):
    print message
    sys.exit(1)

def main():
    scraped_songs = crawl_music([sys.argv[1]])
    print "printing songs"
    print scraped_songs


    for song in scraped_songs:
	print "song_title is "+song["title"]
	print "artist_name is "+song["artist"]
	print "album_name is "+song["album"]
	print "track_name is "+str(song["number"])
	print "year is "+song["year"]
	print "-----------------"

if __name__ == '__main__':
    main()
