from flask import Flask, render_template
from music_crawler import crawl_music
import json
import os

app = Flask(__name__)

@app.route("/")
def main_page():
    library = crawl_music([os.path.join(os.getcwd(), "static", "audio")])
    return render_template("index.html", library=json.dumps(library))

if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)
