from flask import Flask, render_template
from music_crawler import MUSIC_FILE_TYPES, crawl_music
import json
import os

app = Flask(__name__)

@app.route("/")
def main_page():
    library = crawl_music([os.path.join(os.getcwd(), "static", "audio")])

    # Take off all directories up to this one (hack for now)
    cur_path = str(os.getcwd())
    for song in library:
        song["full_path"] = song["full_path"][len(cur_path):]
        for ext in MUSIC_FILE_TYPES:
            ext_key = ext[1:]
            if ext_key in song:
                song[ext_key] = song[ext_key][len(cur_path):]

    return render_template("index.html", library=json.dumps(library))

if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)
