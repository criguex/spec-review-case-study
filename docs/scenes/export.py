import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
ASSETS = HERE.parent / "assets"
FPS = 12
NAMES = sys.argv[1:] or ["explained", "explained.es"]

with sync_playwright() as pw:
    browser = pw.chromium.launch(channel=os.environ.get("CHROME_CHANNEL", "chrome"))
    page = browser.new_page(viewport={"width": 960, "height": 540})
    for name in NAMES:
        scene, _, lang = name.partition(".")
        frames = Path(os.environ.get("FRAMES_DIR", tempfile.gettempdir())) / "spec-review-frames" / name
        shutil.rmtree(frames, ignore_errors=True)
        frames.mkdir(parents=True)
        page.goto((HERE / f"{scene}.html").as_uri() + (f"?lang={lang}" if lang else ""))
        page.wait_for_selector('body[data-ready="1"]')
        total = round(page.evaluate("window.DURATION") * FPS)
        for i in range(total):
            page.evaluate("t => window.render(t)", i / FPS)
            page.screenshot(path=str(frames / f"f{i:03d}.png"))
        ff = ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(frames / "f%03d.png")]
        subprocess.run(ff + ["-vf", "split[a][b];[a]palettegen=max_colors=128:stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=5", "-loop", "0", str(ASSETS / f"{name}.gif")], check=True)
        subprocess.run(ff + ["-pix_fmt", "yuv420p", "-vf", "scale=960:-2", str(ASSETS / f"{name}.mp4")], check=True)
        print(f"{name}: {total} frames in {frames}")
    browser.close()
