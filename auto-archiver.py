import os
import sys
import subprocess
from flask import Flask, render_template, request, session, redirect, url_for
from yt_dlp import YoutubeDL
import ffmpeg
import threading

app = Flask(__name__)
url_queue = []
is_processing = False


@app.route('/archive', methods=['GET'])
def archive():
    try:
        url = request.args.get('url')
        print(f"Recieved URL: {url}")
        print("Checking cache")
        if not check_cache(url):
            url_queue.append(url)
            update_cache(url)
            if not is_processing:
                start_processing()
        else:
            print("Video already archived")


        return "OK", 200
    except:
        return "URL INVALID", 400


def start_processing():
    global is_processing
    is_processing = True
    processing_thread = threading.Thread(target=process_queue)
    processing_thread.start()


def process_queue():
    global is_processing
    while url_queue:
        url = url_queue.pop(0)
        try:
            clean_up_list = []
            video = download_video(url)
            clean_up_list.append(video)
            remuxed_video = remux(video)
            clean_up_list.append(remuxed_video)
            upload(remuxed_video)
            clean_up(clean_up_list)
        except:
            continue

    is_processing = False

def check_cache(url):
    with open("video_cache", "r") as file:
        for line in file:
            return line.strip() == url


def update_cache(url):
    with open("video_cache", "a") as file:
        file.write(url + "\n")


def download_video(url):
    video = ""

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'outtmpl': '%(title)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video = ydl.prepare_filename(info)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    return video


def remux(video):
    video_parts = video.split(".")
    if video_parts[-1] == "mp4":
        return video
    output_file = video_parts[0] + ".mp4"
    stream = ffmpeg.input(video)
    stream = ffmpeg.output(stream, output_file, format='mp4', vcodec='copy', acodec='copy')
    ffmpeg.run(stream)
    return output_file


def upload(remuxed_video):
    print(f"Uploading: {remuxed_video}")
    local_file = remuxed_video
    remote_path = "onedrive:youtube_videos/"

    with subprocess.Popen(["rclone", "sync", local_file, remote_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, text=True) as process:
        if process.stdout:
            for line in process.stdout:
                print(line, end="")
        if process.stderr:
            for line in process.stderr:
                print(line, end="")

    exit_code = process.wait()
    print(f"rclone sync completed with exit code: {exit_code}")


def clean_up(clean_up_list):
    clean_up_list = set(clean_up_list)
    for file in clean_up_list:
        print(f"Deleting {file}")
        os.remove(file)


if __name__ == '__main__':
    default_port = 5431

    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Invalid port number. Using default port.")
            port = default_port
    else:
        port = default_port

    app.run(host="0.0.0.0", port=port)
