import os
import requests
import yt_dlp
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

DOWNLOAD_DIR = '/data/data/com.termux/files/home/storage/downloads'
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json or request.form
    url = data.get('url')

    if not url:
        return jsonify({'status': 'error', 'message': 'Please provide a valid URL'}), 400

    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
        'restrictfilenames': True,
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'nocheckcertificate': True,
        'quiet': True,
        'no_warnings': True,
        'cookiefile': os.path.expanduser('~/Iqbal_Video_Downloader/cookies/youtube_cookies.txt'),
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        return jsonify({
            'status': 'success',
            'message': 'Downloaded successfully to downloads/ folder!',
            'filename': os.path.basename(filename)
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/generate-ai', methods=['POST'])
def generate_ai():
    if not GEMINI_API_KEY:
        return jsonify({'status': 'error', 'message': 'GEMINI_API_KEY .env ফাইলে সেট করা নেই।'}), 500
    try:
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={GEMINI_API_KEY}"
        headers = {'Content-Type': 'application/json'}
        prompt = (
            "Generate a 200-400 character engaging hook/caption for a video, "
            "include one interesting question to boost engagement, "
            "and end with 5 relevant viral hashtags."
        )
        payload = {"contents": [{"parts": [{"text": prompt}]}]}

        response = requests.post(api_url, json=payload, headers=headers)
        res_data = response.json()

        if response.status_code == 200:
            result_text = res_data['candidates'][0]['content']['parts'][0]['text']
            return jsonify({'status': 'success', 'result': result_text})
        else:
            error_msg = res_data.get('error', {}).get('message', 'API Error')
            return jsonify({'status': 'error', 'message': error_msg}), 500

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
