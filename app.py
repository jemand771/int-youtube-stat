from flask import abort, Flask, jsonify, request, render_template, Response

app: Flask = Flask(__name__)


@app.get("/")
def home_page() -> str:
    return render_template("home.html")


@app.get("/video_ids/<url>")
def get_video_ids(url) -> Response:
    print("fetching video ids for", url)
    # TODO fetch video ids
    return jsonify(["a", "b", "c"])


@app.get("/video_info/<video_id>")
def get_video_info(video_id: str) -> str:
    print(video_id)
    return ""


# POST video_ids als json-array
# z.B. ["foo", "bar", "asasdasdasd"]
@app.post("/stats")
def get_stats_from_video_ids() -> str:
    if not isinstance(request.json, list):
        abort(400, "request body needs to be of type list")
    # TODO calculate stats
    return ""


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
