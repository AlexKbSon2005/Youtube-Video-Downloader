from flask import Flask, render_template, request
from pytube import YouTube

app = Flask(__name__)

# Function to download YouTube video or audio
def download_youtube_content(video_url, save_path, download_audio=False):
    try:
        yt = YouTube(video_url)
        if download_audio:
            stream = yt.streams.filter(only_audio=True).first()
        else:
            stream = yt.streams.get_highest_resolution()
        stream.download(save_path)
        return yt.title, yt.thumbnail_url  # Return title and thumbnail URL
    except Exception as e:
        return None, None, f"Error: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form['video_url']
    format_option = request.form['format_option']
    save_path = "./downloads/"

    if format_option == 'video':
        title, thumbnail_url = download_youtube_content(video_url, save_path, download_audio=False)
        if title and thumbnail_url:
            return render_template('downloaded.html', title=title, thumbnail_url=thumbnail_url)
        else:
            return render_template('downloaded.html', message="Error occurred during download.")
    elif format_option == 'audio':
        title, thumbnail_url = download_youtube_content(video_url, save_path, download_audio=True)
        if title and thumbnail_url:
            return render_template('downloaded.html', title=title, thumbnail_url=thumbnail_url)
        else:
            return render_template('downloaded.html', message="Error occurred during download.")
    else:
        return render_template('downloaded.html', message="Invalid format option")

if __name__ == '__main__':
    app.run(debug=True)
