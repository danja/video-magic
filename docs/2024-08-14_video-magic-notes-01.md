## Plan

_you can make a silk purse out of a sow's ear if you have a model that has spent it's whole life comparing them_

1. Extract individual frames as images from original video
2. Upscale/improve individual frames
3. Interpolate new frames
4. Render interpolated frames into video

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

Last things for tonight (23:30, 27.6°C in the office, Spain 2, England 1)

```

pip freeze > requirements.txt

```

gitty bits...

Food, couch, Hawaii 5-0 (on Rai 4 lingua originale).

---

*...continued 40 hours later...*

Ok, so this upscaling will take a lot of time on my CPU-only office machine, and I expect the interpolation will take at least as long, ie. days in total.

But before planting things on Colab or wherever, it would make sense to figure out the next bit locally too. Just do a few seconds to sanity-check.

I have noted down Linux commands to maximise performance on a machine like this (with the help of Claude), but I won't bother right now unless I obviously need to.

Hmm. I didn't note the frame rate...

Ok, the original vid is 40 mins = 2400s. I got 19257 frames. 19257/2400 ~= 8 fps? For a very old camera that does sound ballpark.

Taking 5s for each frame to upscale.

How long would 10s of the original take? 10x8x5 = 400s = ~7 mins. Yeah.

*(I am outrageously bad at basic arithmetic, need to spell things out to stand a chance of getting sums right)*

Er, 80 frames..?

Here we go then, in `upscale-many.py`,
```

for i in range(1, 80):

```

*(also rubbish memory, `history| grep python`)*

```

python src/upscale-many.py

```

```

Processed 79 frames (7.90%) in 708.31 seconds

```

*Heh, out by one error. You should see my C code.*

I'd better test by gluing the new frames into a vid.

Ask Claude.

I'd better start by lifting the following out of `extract-frames.py`, note her in case I need it later:

```

// use absolute paths

video_path = os.path.abspath('data/input/orig-vid-only.mp4')
output_folder = os.path.abspath('data/frames')

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    ( ... )

```

#### Reglue vid prompt

>> I have used the code below to extract frames from a video file. Can you please generate corresponding code that will join together images 1-80 back into a video in a non-lossy format and save it in the 'data/output' directory.
*[source of src/extract-frames.py]*

Yay! First pass it gave me the result at 25 fps. Claude told me the parameter to change it back to the original 8.

Runs very fast.

I'm not entirely convinced of the other encoding parameters Claude gave me, but they will do for now.

Time for dogwalk #2. I might as well run the upscale script a bit longer while we are out.

```

for i in range(1, 401):

```

I've not done the sums. Just feels right.

I remixed to vid, that worked.

The result is very Mr.Blobby, but no worse. Is enough time to get an idea if it's doing any good.

Hmm, I'm confused. I ran `images-vid.py` on the original frames, that looks a lot longer in time.

Yeah, the original comes out at 50s, the upscaled 16s. Repeat.

Ok Claude. Thank you Claude, you remembered markdown format :

# Explanation of Video Length Discrepancy

When creating a video from a series of images, the output video length can vary based on several factors:

1. **Frame Rate**: If you're not explicitly setting a frame rate, ffmpeg might be inferring one based on the input. Smaller images might be interpreted as having a lower frame rate, resulting in a longer video.

2. **Codec Behavior**: Some codecs might handle different image sizes differently, potentially affecting the output duration.

3. **Container Format**: The container format (like .avi) can influence how the video is packaged and interpreted.

To address these issues and ensure consistent output regardless of image size, while maintaining a lossless quality and using the .avi format, we need to:

1. Explicitly set the input frame rate
2. Use a lossless codec compatible with .avi
3. Ensure the output frame rate matches the input frame rate

Here's an updated script that should produce consistent results:

...

Ok, after a bit of tweaking, and getting confused about which code file I was looking at (at 1:25 on an empty stomach), it is now behaving. Really can't tell if things are any better.

But you definitely can make a silk purse out of a sow's ear if you have a model trained on lots of silk purses.

Ok, so far so good.

I now eat.

---

Next day. I upgraded Ubuntu mantic to noble, that broke the venv.
Took a while to fix.

---

Another day.

`main.py` is successfully doing the end-to-end process. Now to get it up on Colab.

Moving to a new file of scrappy notes...

----

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

### Venv broke after Ubuntu update manic -> noble

```bash
sudo apt update
sudo apt upgrade

danny@danny-desktop:~$ python --version
Python 3.12.3

danny@danny-desktop:~$ pip --version
pip 24.1.2 from /home/danny/.local/lib/python3.12/site-packages/pip (python 3.12)

danny@danny-desktop:~$ sudo python -m pip install --upgrade pip
error: externally-managed-environment

sudo apt install python3-pip
...
python3-pip is already the newest version (24.0+dfsg-1ubuntu1).

mv /home/danny/foaf-archive-support/video-magic /home/danny/foaf-archive-support/video-magic_

python3 -m venv /home/danny/foaf-archive-support/video-magic

cd /home/danny/foaf-archive-support/video-magic
source bin/activate

 ls
bin  include  lib  lib64  pyvenv.cfg
```

Python had been updated in the upgrade so I copied everything except those new env dirs & file from the old version into the new.
Then:

```
pip install -r requirements.txt
...
ERROR: THESE PACKAGES DO NOT MATCH THE HASHES FROM THE REQUIREMENTS FILE. If you have updated the package versions, please update the hashes. Otherwise, examine the package contents carefully; someone may have tampered with them.
```

Oops.

Claude suggests :

```
pip install hashin
hashin -r requirements.txt packagename==version
```

Looks promising. A little reading later-

```
cp requirements.txt requirements_bad-hash.txt
hashin -v --update-all -r requirements.txt
...
Invalid version: '0.5.13-hg'
```

That ran correctly after I'd removed these from `requirements.txt` :

```
sympy==1.13.0
RealESRGAN @ git+https://github.com/sberbank-ai/Real-ESRGAN.git@362a0316878f41dbdfbb23657b450c3353de5acf
```

So I'll do those manually :

```
pip install sympy
pip install git+https://github.com/sberbank-ai/Real-ESRGAN.git
```

It failed on hashes again with ESRGAN, which was pulling in loads of dependencies.

The `requirements.txt` at https://github.com/ai-forever/Real-ESRGAN is pretty short:

```
numpy
opencv-python
Pillow
torch>=1.7
torchvision>=0.8.0
tqdm
huggingface-hub
```

So I'll install these manually.

```
pip install torch>=1.7
...
ERROR: THESE PACKAGES DO NOT MATCH THE HASHES FROM THE REQUIREMENTS FILE.
```

```
torch==2.3.1
torchvision==0.18.1

hashin -v -r requirements.txt torch==2.3.1
```

Same error. But there is such a big dependency tree I didn't fancy doing it all manually. So we made a helper script to run pip on

```
python src/install-requirements.py pytorch-requirements.txt
```

That did get things a bit further, but failed again.

**D'oh! Purge the cache, dude!**

```
pip cache purge
Files removed: 602
...
pip install torch>=1.7
```

That _appears_ to have run without incident (note to self: use `pip -v` in future).

```
pip install -v git+https://github.com/sberbank-ai/Real-ESRGAN.git
```

That worked. Ok, I'd better :

```
pip freeze > requirements.txt
```

Oops, it's not `ffmeg` but :

```
pip install ffmpeg-python
```
