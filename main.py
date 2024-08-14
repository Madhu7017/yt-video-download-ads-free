from flask import Flask, render_template, request, redirect, url_for
import yt_dlp
import os

app = Flask(__name__)

def sanitize_filename(filename):
    return "".join(c for c in filename if c not in r'\/:*?"<>|')

def download_2k_resolution(url, output_path='.'):
    try:
        ydl_opts = {
            'format': 'best[height<=1440]',  # Download the best single format available up to 1440p (2K)
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'noplaylist': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            sanitized_title = sanitize_filename(info_dict['title'])
            return f"Downloaded: {sanitized_title}"
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""
    if request.method == 'POST':
        video_url = request.form['url']
        output_path = '.'  # You can change this to a specific directory
        message = download_2k_resolution(video_url, output_path)
    return render_template('index.html', message=message)

if __name__ == "__main__":
    app.run(debug=True)
