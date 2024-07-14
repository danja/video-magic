## Plan

1. extract frames from original vid
2. Upscale/improve individual frames
3. Interpolate new frames into better video

### First Pass

I've lost the link to the original vid... but do have a video-only download from YouTube using... I forget it's name, will be in the history on music room machine. It gives a bunch of alternate versions in various formats, presumably I chose the one that looked best...

`ffmpeg` is probably the tool for pulling out the frames.

```
   python src/extract-frames.py
```

Ok, a little path tweaking and that appears to have worked, maybe. Very quick. Lots of files, final one being `frame_19257.png`. Doesn't look like it's the final frame in the original video, but good enough for now.

Not sure about this either - it's 160x120 px. Not entirely implausible, the vid is very old. But still, good enough for now.

Ok, for upscaling, Real-ESRGAN looked promising. Try that on a single frame.

```
   python src/upscale-single.py
```

Ok, it tried CUDA on my very old GPU card, suggested I get a legacy version build for that. But it's a rubbish card anyway, CPU good enough for now.

Yay! That actually worked! _insert screenshots_.

Output is 640x480. It's nicely smoothed some of the image, some is still very chunky, and the text in the image ("O'Reilly") is _less_ legible, but I reckon it's worth proceeding, doing a small batch to see how it fares with interpolation.

Ok, at the point where I should save this elsewhere. Done a `backup.sh` to copy onto 2nd drive on this machine, plus a GitHub repo. `.gitignore` includes the data dir, I don't want to risk hitting the file size limits or whatever.

Soon I should add a `requirements.txt`

Ouch. It's taking about 20s per frame. Sums... about 107 hours for 19257 frames.

Other models at https://drive.google.com/drive/folders/16PlVKhTNkSyWFx52RPb2hXPIQveNGbxS including a x2. Lets do this.

The example code has :

```
model.load_weights('weights/RealESRGAN_x4.pth', download=True)
``

Tweaked to x2, that Just Worked.

Down to ~5s per frame. That seems more feasible, about a day on this CPU. On Colab..?

The result, 320x240px *insert screenshots* is way less pixelated. I *think* the faces have about the same amount of detail, only smoother. Text is again mangled, not a worry.

https://github.com/MSFTserver/colab-convert









### Setup

_in home/danny/foaf-archive-support_

```

python3 -m venv video-magic

```

I will want a `.gitignore` soon, just so I can tell Cursor to ignore it when analysing the whole codebase.

I asked Cursor about the environment :

```

my_project/
├── src/
│ └── main.py
├── venv/
├── .env
└── ...

python3 -m venv venv
source venv/bin/activate

      pip install -r requirements.txt

# .env

HUB_BASE_URL=https://api.notefile.net
HUB_AUTH_TOKEN=your_auth_token
HUB_PROJECT_UID=your_project_uid
HUB_PRODUCT_UID=your_product_uid

      import os

from dotenv import load_dotenv

load_dotenv()

hub_base_url = os.getenv('HUB_BASE_URL')
hub_auth_token = os.getenv('HUB_AUTH_TOKEN')
hub_project_uid = os.getenv('HUB_PROJECT_UID')
hub_product_uid = os.getenv('HUB_PRODUCT_UID')

print(f"Base URL: {hub_base_url}")
print(f"Auth Token: {hub_auth_token}")
print(f"Project UID: {hub_project_uid}")
print(f"Product UID: {hub_product_uid}")

pip install python-dotenv

python src/main.py

```

AI also suggested, I don't know if I'll need this, we'll see :

```

pip install python-dotenv

```

Create a .env file in the root of your project:

```

# .env

HUB_BASE_URL=https://api.notefile.net
HUB_AUTH_TOKEN=your_auth_token
HUB_PROJECT_UID=your_project_uid
HUB_PRODUCT_UID=your_product_uid

```

use as:

```

import os
from dotenv import load_dotenv

load_dotenv()

hub_base_url = os.getenv('HUB_BASE_URL')
hub_auth_token = os.getenv('HUB_AUTH_TOKEN')
hub_project_uid = os.getenv('HUB_PROJECT_UID')
hub_product_uid = os.getenv('HUB_PRODUCT_UID')

print(f"Base URL: {hub_base_url}")
print(f"Auth Token: {hub_auth_token}")
print(f"Project UID: {hub_project_uid}")
print(f"Product UID: {hub_product_uid}")

```

**nota bene** - must be in .gitignore

### ffmpeg

```

pip install ffmpeg-python

```

#### Real-ESRGAN

[PyTorch implementation of a Real-ESRGAN model](https://github.com/ai-forever/Real-ESRGAN) on GitHub.

```

pip install git+https://github.com/sberbank-ai/Real-ESRGAN.git

```

took a very long time, I think it pulled loads of CUDA libs, even though I don't have a usable GPU in this machine.

---

```

sudo -i
QT_QPA_PLATFORM=xcb
flatpak run io.github.tntwise.REAL-Video-Enhancer

```

https://github.com/TNTwise/REAL-Video-Enhancer/issues/8

https://askubuntu.com/questions/1086529/how-to-give-a-flatpak-app-access-to-a-directory

https://docs.flatpak.org/en/latest/sandbox-permissions.html

https://docs.flatpak.org/en/latest/flatpak-command-reference.html

---

flatpak-spawn --host cp /run/host/root/Videos/output-video.avi_640x480.mp4 ~/output-video.avi_640x480.mp4

sudo -E flatpak enter 177213 sh
cp /root/Videos/output-video.avi_640x480.mp4 /home/danny/flatpak-exports/output-video.avi_640x480.mp4
exit
```
