import browser_cookie3
import json

try:
    # Try to get cookies from Chrome/Chromium
    cj = browser_cookie3.chrome()
    print("✅ Chrome cookies found!")
except:
    try:
        # Try Firefox
        cj = browser_cookie3.firefox()
        print("✅ Firefox cookies found!")
    except:
        print("❌ No browser cookies found. Using manual method...")
        cj = None

if cj:
    # Save to file
    cookies_file = os.path.expanduser('~/AI_Travel_App/downloads/cookies.txt')
    with open(cookies_file, 'w') as f:
        for cookie in cj:
            f.write(f"{cookie.domain}\tTRUE\t{cookie.path}\tFALSE\t0\t{cookie.name}\t{cookie.value}\n")
    print(f"✅ Cookies saved to: {cookies_file}")
else:
    print("Please install a browser or use manual cookies file")
