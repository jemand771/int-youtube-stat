import os

from flask import abort, Flask, jsonify, request, render_template, Response

from api_helper import YouTubeApi

app: Flask = Flask(__name__)
api = YouTubeApi(os.environ.get("YOUTUBE_API_KEY"))


@app.get("/")
def home_page() -> str:
    return render_template("home.html")


@app.get("/video_ids/<path:url>")
def get_video_ids(url) -> Response:
    # forward the query string from flask to the url parser inside the ytapi
    if request.query_string:
        url += "?" + request.query_string.decode("utf-8")
    print("fetching video ids for", url)
    return jsonify(api.get_video_ids_from_link(url))


@app.get("/video_info/<video_id>")
def get_video_info(video_id: str) -> Response:
    return jsonify(api.get_video_data(video_id))


# POST video_ids als json-array
# z.B. ["foo", "bar", "asasdasdasd"]
@app.post("/stats")
def get_stats_from_video_ids() -> Response:
    if not isinstance(request.json, list):
        abort(400, "request body needs to be of type list")
    if not all(type(x) == str for x in request.json):
        abort(400)
    return jsonify(api.get_stats(request.json))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
