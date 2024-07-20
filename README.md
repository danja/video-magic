# Magic to Improve the Quality of a Video Recording

_indistinguishable to me_

**tl;dr** : glue code to run a couple of machine learning algorithms/models on the visuals (see [Tools](#tools) and [File List](#file-list))

Audio cleaning isn't included in the code, a pay-for service was used for now. But that may follow, if and when it's needed.

**Status 2024-08-20** : full process running locally and on Colab on a snippet of the video (very slowly on a GPU-less computer), this README in-progress

**Caveat** : my goal was to see what I could do with one specific recording without getting lost down the rabbit hole. In agile-speak, a spike. While I'm familiar with (conventional) audio techniques and (some) ML, I haven't spent much time around video/image processing, so most of this is from a perspective of learning as I go along, ie. it can no doubt be significantly improved on. But I think the overall workflow makes sense as a starting point. And, as far as it goes, it works.

_Parameter tweaks should make for easy improvement (trial & error time aside), out of ignorance I've simply used defaults. Different algorithms/models will be worth trying. If I were to take this further today, I'd start with a combination of upscaling algorithms and interleaving the results prior to interpolation (little bit of Python tweakage, give the frames odd/even numbered names or whatever)._

## Installation

_I need to double-check this_

With Python 3 installed :

```
git clone https://github.com/danja/video-magic.git

cd video-magic

pip install -r requirements.txt
```

Then the individual scripts can be run, eg.

```
python src/main.py
```

Check inside the `.py` files for paths etc.

Only tested on Ubuntu 2024.04.

The `.py` files lag behind the [Colab Notebook](src/video-magic_colab.ipynb)

### See Also

- [verbose, disorganised notes 01](docs/2024-08-14_notes-01.md)
- [verbose, disorganised notes 02](docs/2024-08-19_notes-02.md)
- [verbose, disorganised notes 03](docs/2024-08-20_notes-03.md)
- [todo](docs/todo.md)

## Sourcing a Video

I assume I used [yt-dlp](https://github.com/yt-dlp/yt-dlp) to download the original video _(for which I've lost the link)_. I typically do a two-part operation :

- `yt-dlp -F <YouTube URL>` - lists available formats, with short ref numbers
- `yt-dlp -f <ref number> <YouTube URL>` - downloads video in that format

**Warning : this free download almost certainly contravenes YouTube's terms of service, so, er, be warned**

I (presumably) got the audio-only and video-only versions that looked best quality.

While `ffmpeg` is the Swiss army knife, for convenience I use [Kdenlive](https://kdenlive.org/en/) for regular video editing. I hadn't used it on this machine before, got a `Failed to create wl_display...`. Solution to that for me was to tell it to use X11 (not Wayland) :

```
QT_QPA_PLATFORM=xcb

# check
loginctl show-session $(loginctl | grep $(whoami) | awk '{print $1}') -p Type
```

## Audio Cleanup

First pass, I tried various conventional tools. I forget which, but one will have been the noise reduction in [Audacity](https://www.audacityteam.org/). You give that a sample of the noise in the background, I assume it does an FFT. Then run again, runs a filter based on the FFT. This wasn't much use on the audio I had from this video, ymmv.

I did try a couple of open source ML-based tools, without success. _Wait by the river until the body of the tool I want floats by..._ [Eleven Labs' Voice Isolator](https://elevenlabs.io/voice-isolator) appeared. Because I anticipated this needing a bit of experimentation I signed up for their 'Creator' subscription, which cost $13.42 for the first month. It may even have been on the first run, I got a good result. It now says I've used 37% of my character quota, whatever that is. I've cancelled renewal for now (there are almost certainly other bits I can use elsewhere).

Post-processing, it may be worth doing a little classic tweaking of equalization and compression to further emphasize voices. In the context of room or hall, adding slight reverb _might_ help the perceived quality, a better psychoacoustic match for the visuals.

## Video Cleanup

_you **can** make a silk purse out of a sow's ear if you have a model that spent its formative weeks comparing them_

### Strategy

After minimal research, I settled on this processing sequence :

1. Extract individual frames as images from original video
2. Upscale/improve individual frames
3. Interpolate new frames
4. Render interpolated frames into video

For implementation, because typically ML==Python, it was the obvious choice of language.

This was bound to be processor-hungry and I don't have a usable GPU here, so I decided to :

- code up each step individually as regular Python
- test locally on a snippet of the video (400 frames, 50s)
- join code together
- convert into a notebook for HuggingFace and/or Colab
- run at speed...

_At this point I brought in my colleagues ChatGPT4o, Cursor (using OpenAI API) and Claude 3.5 Sonnet. Henceforth plural personal pronouns may appear._

### Tools Used

1 & 4 were pretty straightforward with `python-ffmpeg`. We haven't looked closely at the decoding/encoding format & parameters, they may well be suboptimal. I did suggest 'non-lossy' to the team, I don't know if they listened.

After a bit of hunting & trial trial trial & error error error, the following were chosen for 2 & 3 :

- Upscaling : **Real-ESRGAN** super-resolution ([paper](https://arxiv.org/abs/2107.10833)), ([original implementation](https://github.com/xinntao/Real-ESRGAN)). We used this [PyTorch implementation from GitHub](https://github.com/ai-forever/Real-ESRGAN)
- Interpolation : **RIFE** (Real-Time Intermediate Flow Estimation for Video Frame Interpolation) in the shape of [rife-ncnn-vulkan](https://github.com/nihui/rife-ncnn-vulkan) ([paper](https://arxiv.org/abs/2011.06294))

The former had a tweakable example, the latter actually has a standalone binary release **which works!**

- Other Techniques

- Background

### File List

## Background

A while ago [danbri](https://x.com/danbri) (/[danbri.org](https://danbri.org/)) asked me to see what I could do with an video of a presentation he & Edd _(TODO current link?)_ did about the [FOAF Project](https://en.wikipedia.org/wiki/FOAF) years ago. The a/v quality was terrible. I was reasonably confident I'd be able to improve the audio using conventional techniques, but this turned out to be far less successful than I thought. On the video side, I didn't have a clue at first.
