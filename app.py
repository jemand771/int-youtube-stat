import dataclasses
import functools
import os
import re

from flask import abort, Flask, jsonify, request, render_template, Response
from flask.json import JSONEncoder

import api_helper

app: Flask = Flask(__name__)
api = api_helper.YouTubeApi(os.environ.get("YOUTUBE_API_KEY"))


def validate_video_list(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not isinstance(request.json, list):
            abort(400, "request body needs to be of type list")
        if not all(type(x) == str for x in request.json):
            abort(400)
        return func(*args, **kwargs)

    return wrapper


class MyJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, api_helper.YouTubeData):
                return {
                    key: str(val)
                    for key, val
                    in dataclasses.asdict(obj).items()
                }
        except TypeError as ex:
            print(ex)
            pass
        return JSONEncoder.default(self, obj)


# TODO test? -> <-
app.json_encoder = MyJSONEncoder


@app.get("/")
def home_page() -> str:
    return render_template("home.html")


@app.get("/video_data/<path:url>")
def get_video_data_multi(url) -> Response:
    # forward the query string from flask to the url parser inside the ytapi
    if request.query_string:
        url += "?" + request.query_string.decode("utf-8")
    # workaround for werkzeug's wonky double slash handling
    url = re.sub(r"^https?://?", "", url)
    url = f"https://{url}"
    print("fetching video data for", url)
    return jsonify(api.get_video_data_multi(api.get_video_ids_from_link(url)))


# POST video_ids als json-array
# z.B. ["foo", "bar", "asasdasdasd"]
@validate_video_list
@app.post("/stats")
def get_stats_from_video_ids() -> Response:
    return jsonify(api.get_stats(request.json))


@app.errorhandler(api_helper.InvalidLinkFormatException)
@app.errorhandler(api_helper.VideoNotFoundException)
def handle_api_error(ex):
    return str(ex), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
