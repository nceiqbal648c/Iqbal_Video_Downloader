import os
from flask import Flask, render_template, request, jsonify
from google import genai
from PIL import Image
import subprocess

app = Flask(__name__)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

@app.route('/')
def home():
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Iqbal Video Downloader</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&display=swap');

*{box-sizing:border-box} 
:root{--cyan:#16eaff;--orange:#ff9d00;--pink:#ff007f;--ink:#020914} 

body{margin:0;min-height:100vh;color:#eafaff;font-family:'Orbitron',sans-serif;background: radial-gradient(circle at 15% 8%,rgba(0,238,255,.13),transparent 28%), radial-gradient(circle at 88% 18%,rgba(180,95,18,.18),transparent 30%), linear-gradient(155deg,#02070c,#07141b 46%,#160d08 100%);padding:18px} 

body:before{content:"";position:fixed;inset:0;pointer-events:none;opacity:.18;background-image: linear-gradient(rgba(22,234,255,.12) 1px,transparent 1px), linear-gradient(90deg,rgba(22,234,255,.1) 1px,transparent 1px);background-size:34px 34px} 

.app-shell{width:min(100%,720px);margin:auto;position:relative} 

.glass{background:linear-gradient(135deg,rgba(8,25,35,.72),rgba(12,13,16,.62),rgba(62,34,14,.24)); -webkit-backdrop-filter:blur(22px);backdrop-filter:blur(22px);border:3px solid rgba(22,234,255,.82); box-shadow:0 0 10px rgba(22,234,255,.65),0 0 30px rgba(22,234,255,.22), inset 0 0 22px rgba(22,234,255,.14),inset -10px 0 22px rgba(255,157,0,.09);border-radius:26px; padding:22px; margin:18px 0} 

.hero{text-align:center;padding:28px 14px;margin-bottom:18px;border-color:var(--pink);box-shadow:0 0 15px rgba(255,0,127,0.5), inset 0 0 25px rgba(255,0,127,0.2)} 

h1{font-size:clamp(22px,5vw,38px);margin:0;color:var(--orange);text-shadow:0 0 14px rgba(255,157,0,.45)} 
h1 span{color:var(--cyan);text-shadow:0 0 15px rgba(22,234,255,.6)} 

.neon-creator {
    display: inline-block;
    margin-top: 12px;
    padding: 8px 20px;
    font-size: 1.1rem;
    font-weight: 900;
    letter-spacing: 3px;
    color: #fff;
    background: rgba(0, 0, 0, 0.6);
    border: 2px solid var(--cyan);
    border-radius: 50px;
    text-transform: uppercase;
    text-shadow: 0 0 8px var(--cyan), 0 0 20px var(--cyan), 0 0 35px var(--cyan);
    box-shadow: 0 0 15px var(--cyan), inset 0 0 10px var(--cyan);
    animation: neonPulse 2s infinite alternate;
}

@keyframes neonPulse {
    0% {
        border-color: var(--cyan);
        text-shadow: 0 0 8px var(--cyan), 0 0 20px var(--cyan);
        box-shadow: 0 0 10px var(--cyan), inset 0 0 10px var(--cyan);
    }
    100% {
        border-color: var(--pink);
        text-shadow: 0 0 10px var(--pink), 0 0 25px var(--pink), 0 0 40px var(--pink);
        box-shadow: 0 0 20px var(--pink), inset 0 0 15px var(--pink);
    }
}

.hero strong{display:block;color:var(--cyan);font-size:16px;margin-top:10px}
.hero p{letter-spacing:2px;margin:8px 0 0;color:#a9bdc7;font-size:0.9rem} 

h2{margin:0 0 17px;font-size:21px;color:#eafaff}
h2 small,.muted{color:#a9bdc7;font-weight:normal} 

.upload-zone{height:240px;border:2px dashed rgba(22,234,255,.8);border-radius:20px;display:grid;place-items:center;text-align:center; background:rgba(0,0,0,.2);overflow:hidden;cursor:pointer;position:relative;margin-bottom:12px}
.upload-zone input{display:none} 
#uploadPrompt{display:grid;gap:9px}
.upload-icon{font-size:50px;color:var(--cyan);text-shadow:0 0 18px var(--cyan)} 
#uploadPrompt span{color:#9fb9c6}
#preview{width:100%;height:100%;object-fit:cover;position:absolute;inset:0;display:none} 

.field{width:100%;padding:16px;border-radius:16px;border:2px solid var(--cyan);background:#020617;color:#fff;font-size:1rem;outline:none;margin-bottom:12px}
.two{display:grid;grid-template-columns:1fr 1fr;gap:12px}

.btn{width:100%;background:linear-gradient(135deg,#0ea5e9,#2563eb);color:white;border:none;padding:14px;font-size:1rem;font-weight:bold;border-radius:14px;cursor:pointer;text-transform:uppercase;box-shadow:0 4px 15px rgba(14,165,233,0.4);transition:0.3s}
.btn.accent{background:linear-gradient(135deg,#ff9d00,#d97706);box-shadow:0 4px 15px rgba(255,157,0,0.4)}
.btn.full{width:100%;margin-top:10px}
.btn:active{transform:scale(0.98)}

.result{margin-top:15px;background:#020617;border:1px solid #334155;padding:15px;border-radius:12px;font-size:0.9rem;color:#cbd5e1;white-space:pre-wrap;display:none}
.status{display:flex;justify-content:space-between;align-items:center;background:rgba(8,25,35,.9);padding:18px;border-radius:20px;border:2px solid var(--orange)}
.progress{font-weight:bold;color:var(--orange);font-size:1.2rem}

footer{text-align:center;margin-top:30px;font-size:1rem;letter-spacing:1px;color:#94a3b8}
footer .neon-name {
    color: var(--orange);
    text-shadow: 0 0 10px var(--orange), 0 0 20px var(--orange);
    font-weight: 900;
}
</style>
</head>
<body>

<div class="app-shell">
    <div class="glass hero">
        <h1>IQBAL <span>VIDEO DOWNLOADER</span></h1>
        <strong>Ver: 0.16</strong>
        <p>AI CREATOR</p>
        <div class="neon-creator">⚡ IQBAL AHMED ⚡</div>
    </div>

    <section class="glass">
      <h2>📷 Upload Image <small>(Optional)</small></h2>
      <label class="upload-zone" id="dropZone">
        <input id="imageInput" type="file" accept="image/png,image/jpeg,image/webp" onchange="previewImage()">
        <div id="uploadPrompt">
          <div class="upload-icon">⇧</div>
          <b>Tap to upload image</b>
          <span>JPG · PNG · WEBP</span>
        </div>
        <img id="preview" alt="Uploaded preview">
      </label>
      <button class="btn full" onclick="document.getElementById('imageInput').click()">CHOOSE IMAGE</button>
    </section>

    <section class="glass">
      <h2>📥 Download Video</h2>
      <input id="videoUrl" class="field" type="url" placeholder="Paste video URL here...">
      <div class="two">
        <button class="btn" onclick="pasteText()">PASTE</button>
        <button class="btn accent" onclick="downloadVideo()">DOWNLOAD</button>
      </div>
    </section>

    <section class="glass">
      <h2>✨ AI Caption & Hashtags</h2>
      <p class="muted">Generate a 200–400 character hook/caption, a question and 5 relevant hashtags.</p>
      <button class="btn accent full" onclick="generateAI()">GENERATE AI</button>
      <div id="aiResult" class="result"></div>
    </section>

    <section class="status">
      <div>
        <b>DOWNLOAD STATUS</b>
        <p id="statusText" style="margin:4px 0 0;color:#a9bdc7">Ready to download...</p>
      </div>
      <div class="progress" id="progressText">0%</div>
    </section>

    <footer>Created by : <span class="neon-name">IQBAL AHMED</span></footer>
</div>

<script>
    function previewImage() {
        const file = document.getElementById('imageInput').files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const preview = document.getElementById('preview');
                preview.src = e.target.result;
                preview.style.display = 'block';
                document.getElementById('uploadPrompt').style.display = 'none';
            }
            reader.readAsDataURL(file);
        }
    }

    async function pasteText() {
        try {
            const text = await navigator.clipboard.readText();
            document.getElementById('videoUrl').value = text;
        } catch (err) {
            alert('Please long-press and paste manually.');
        }
    }

    async function downloadVideo() {
        const url = document.getElementById('videoUrl').value;
        const statusText = document.getElementById('statusText');
        const progressText = document.getElementById('progressText');
        if(!url) { alert('Please enter a video URL'); return; }
        
        statusText.innerText = 'Downloading... Please wait ⏳';
        progressText.innerText = '50%';

        try {
            let response = await fetch('/download', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({url: url})
            });
            let data = await response.json();
            if(data.status === 'success') {
                statusText.innerText = '✅ ' + data.message;
                progressText.innerText = '100%';
            } else {
                statusText.innerText = '❌ Error: ' + data.message;
                progressText.innerText = 'Error';
            }
        } catch(e) {
            statusText.innerText = '❌ Server connection failed!';
            progressText.innerText = 'Failed';
        }
    }

    async function generateAI() {
        const fileInput = document.getElementById('imageInput');
        const resBox = document.getElementById('aiResult');
        resBox.style.display = 'block';
        resBox.innerHTML = 'Generating AI caption & hashtags... 🤖⏳';

        const formData = new FormData();
        if(fileInput.files.length > 0) {
            formData.append('image', fileInput.files[0]);
        }
        formData.append('title', document.getElementById('videoUrl').value || 'Travel Video');

        try {
            let response = await fetch('/generate-caption', {
                method: 'POST',
                body: formData
            });
            let data = await response.json();
            if(data.success) {
                resBox.innerHTML = data.caption;
            } else {
                resBox.innerHTML = '❌ Error: ' + data.error;
            }
        } catch(e) {
            resBox.innerHTML = '❌ Server connection failed!';
        }
    }
</script>

</body>
</html>
'''

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({"status": "error", "message": "URL missing"}), 400
    
    download_path = '/sdcard/Download/%(title)s.%(ext)s'
    
    try:
        subprocess.run([
            'yt-dlp', 
            '--restrict-filenames', 
            '--no-check-certificate', 
            '--cookies', '/sdcard/Documents/cookies.txt',
            '-o', download_path, 
            url
        ], check=True)
        return jsonify({"status": "success", "message": "Download completed to /sdcard/Download!"})
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "message": f"yt-dlp error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/generate-caption', methods=['POST'])
def generate_caption():
    try:
        prompt = "Write an engaging social media hook, a caption (200-400 characters), a question, and 5 trending viral hashtags with emojis."
        contents = [prompt]
        
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                img = Image.open(file.stream)
                contents = [img, prompt]
        
        response = client.models.generate_content(
            model='gemini-3.1-flash-lite',
            contents=contents
        )
        return jsonify({'success': True, 'caption': response.text})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
