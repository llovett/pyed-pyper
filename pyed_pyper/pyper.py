from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def main_page():
    # test data
    library = [
        {
            "title": "FML",
            "m4a": "/static/audio/Deadmau5/For Lack Of A Better Name/01 FML.m4a",
            "album": "For Lack Of A Better Name",
            "number": 1,
            "artist": "Deadmau5"
        },
        {
            "title": "Moar Ghosts 'n' Stuff",
            "m4a": "/static/audio/Deadmau5/For Lack Of A Better Name/02 Moar Ghosts 'n' Stuff.m4a",
            "album": "For Lack Of A Better Name",
            "number": 2,
            "artist": "Deadmau5"
        },
        {
            "title": "Bot",
            "m4a": "/static/audio/Deadmau5/For Lack Of A Better Name/05 Bot.m4a",
            "album": "For Lack Of A Better Name",
            "number": 5,
            "artist": "Deadmau5"
        },
        {
            "title": "Word Problems",
            "m4a": "/static/audio/Deadmau5/For Lack Of A Better Name/06 Word Problems.m4a",
            "album": "For Lack Of A Better Name",
            "number": 6,
            "artist": "Deadmau5"
        },
        {
            "title": "Soma",
            "m4a": "/static/audio/Deadmau5/For Lack Of A Better Name/07 Soma.m4a",
            "album": "For Lack Of A Better Name",
            "number": 7,
            "artist": "Deadmau5"
        },
        {
            "title": "Lack Of A Better Name",
            "m4a": "/static/audio/Deadmau5/For Lack Of A Better Name/08 Lack Of A Better Name.m4a",
            "album": "For Lack Of A Better Name",
            "number": 8,
            "artist": "Deadmau5"
        },
        {
            "title": "The 16th Hour",
            "m4a": "/static/audio/Deadmau5/For Lack Of A Better Name/09 The 16th Hour.m4a",
            "album": "For Lack Of A Better Name",
            "number": 9,
            "artist": "Deadmau5"
        },
        {
            "title": "Strobe",
            "m4a": "/static/audio/Deadmau5/For Lack Of A Better Name/10 Strobe.m4a",
            "album": "For Lack Of A Better Name",
            "number": 10,
            "artist": "Deadmau5"
        }
    ]
    library *= 10
    return render_template("index.html", library=library)

if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)
