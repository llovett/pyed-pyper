from flask import Flask, render_template, request, Response
from music_crawler import MUSIC_FILE_TYPES, crawl_music
import settings
import json
import os

app = Flask(__name__)

def authenticate(username, password):
    return username == settings.USERNAME and password == settings.PASSWORD

@app.route("/", methods=["GET", "POST"])
def main_page():
    if request.method == 'POST':
        # Check authentication
        username = request.form["username"]
        password = request.form["password"]
        if authenticate(username, password):
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
        return Response("Could not verify credentials.", 401)
    return render_template("login.html")

if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)
