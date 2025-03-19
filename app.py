from flask import Flask, request, send_file, render_template
import yt_dlp
import os

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download", methods=["GET"])
def download_video():
    video_url = request.args.get("url")
    if not video_url:
        return {"error": "Missing URL"}, 400

    try:
        output_path = "videos"
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        ydl_opts = {
            "format": "best",
            "outtmpl": os.path.join(output_path, "%(title)s.%(ext)s"),
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            file_name = ydl.prepare_filename(info_dict)

        return send_file(file_name, as_attachment=True)

    except yt_dlp.utils.DownloadError:
        return {"error": "Invalid YouTube URL or video is restricted"}, 400
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)






