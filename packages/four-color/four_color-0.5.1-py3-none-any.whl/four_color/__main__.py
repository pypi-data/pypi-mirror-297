from os import environ
from pathlib import Path

from flask import Flask, make_response, redirect, request
from werkzeug.utils import secure_filename

from . import load_image, make_graph, write_four_color

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def root():
    if request.method != "POST":
        return (
            "<form action='/' enctype='multipart/form-data' "
            "method='POST'><input type='file' name='im' size='30'>"
            "<input type='submit' value='send'></from>"
        )
    f = request.files["im"]
    if not f:
        return redirect("/")
    ext = Path(secure_filename(f.filename)).suffix
    if not ext.endswith(("png", "gif", "jgp", "jpeg")):
        return redirect("/")
    fig_file = Path("fig" + ext)
    f.save(fig_file)
    im = load_image(str(fig_file))
    g = make_graph(im)
    write_four_color(im, g)
    im.save(fig_file)
    res = make_response()
    res.data = fig_file.read_bytes()
    res.headers["Content-Type"] = "application/octet-stream"
    res.headers["Content-Disposition"] = "attachment; filename=fig" + ext
    return res


HOST = environ.get("SERVER_HOST", "localhost")
_PORT = environ.get("SERVER_PORT", "")
PORT = int(_PORT) if _PORT.isdigit() else 8000
app.config["MAX_CONTENT_LENGTH"] = 210000
app.debug = True
app.run(HOST, PORT)
