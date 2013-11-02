'''
Music Crawler
Crawls ROOT dir and compiles a mapping of song to file path
'''
import os
import sys


'''
crawl_music
params:
    root -- root directory. All music will be crawled from root. Paths to music files will be prepended with root
'''
def crawl_music(root):

    music_file_to_path = {}
    
    if not os.path.isdir(root):
	fail_and_exit("Cannot scrape from "+root+": not a directory");

    for dirname, dirnames, filenames in os.walk(root):
	# print path to all subdirectories first.
	for subdirname in dirnames:
	    print os.path.join(os.path.abspath(dirname), subdirname)

	# print path to all filenames.
	for filename in filenames:
	    print os.path.join(os.path.abspath(dirname), filename)

        # Advanced usage:
	# editing the 'dirnames' list will stop os.walk() from recursing into there.
        if '.git' in dirnames:
        # don't go into any .git directories.
	    dirnames.remove('.git')
	
	return music_file_to_path

def fail_and_exit(message):
    print message
    sys.exit(1)

def main():
    crawl_music(sys.argv[1])

main()
