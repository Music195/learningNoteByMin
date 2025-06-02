from flask import Flask, render_template_string, redirect, url_for
import os
import json
import re

app = Flask(__name__)
NOTES_FOLDER = "notes"

notes_list = sorted([f[:-5] for f in os.listdir(NOTES_FOLDER) if f.endswith(".html")])

with open("tags.json") as f:
    note_tags = json.load(f)

@app.route("/")
def index():
    return redirect(url_for("view_note", filename=notes_list[0]))

@app.route("/note/<filename>")
def view_note(filename):
    if filename not in notes_list:
        return "<h1>Note not found</h1>", 404

    index = notes_list.index(filename)
    prev_note = notes_list[index - 1] if index > 0 else None
    next_note = notes_list[index + 1] if index < len(notes_list) - 1 else None

    with open(f"{NOTES_FOLDER}/{filename}.html", encoding="utf-8") as f:
        content = f.read()

    notes_json = json.dumps(notes_list)
    tags_json = json.dumps(note_tags)

    return render_template_string(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{{{{ filename.title() }}}} - Math Notes</title>
        <script>
            const NOTES_LIST = {notes_json};
            const NOTE_TAGS = {tags_json};
        </script>
        <script src="https://cdn.jsdelivr.net/npm/fuse.js@6.6.2"></script>
        <script src="/static/script.js" defer></script>
        <style>
            body {{
                font-family: sans-serif;
                padding: 2em;
                min-width: 700px;
                margin: auto;
            }}
            nav {{
                margin-bottom: 1em;
                display: flex;
                justify-content: space-between;
            }}
            .nav-buttons a {{
                margin-right: 1em;
            }}
            #search-results a {{
                display: block;
                margin-bottom: 5px;
            }}
        </style>
        <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
        <script type="text/javascript" async
          src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
        </script>
    </head>
    <body>
        <nav>
            <div class="nav-buttons">
                {'<a href="/note/' + prev_note + '">⬅ Back</a>' if prev_note else ''}
                {'<a href="/note/' + next_note + '">Next ➡</a>' if next_note else ''}
            </div>
            <div>
                <input type="text" id="search" placeholder="Search notes...">
                <select id="tagFilter" onchange="filterByTag()">
                    <option value="">Filter by Tag</option>
                </select>
                <select id="noteSelect" onchange="location = this.value;">
                    {''.join([f'<option value="/note/' + n + '" ' + ('selected' if n == filename else '') + '>' + n.title() + '</option>' for n in notes_list])}
                </select>
                <div id="search-results"></div>
            </div>
        </nav>
        <div style="margin: auto 10% auto 10%">{content}</div>
    </body>
    </html>
    """, filename=filename)

if __name__ == "__main__":
    app.run(debug=True)