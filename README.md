# Magic to Improve the Quality of a Video Recording

_it seems like magic to me_

**tl;dr** : glue code to run a couple of machine learning algorithms/models (see [Tools](#tools) and [File List](#file-list)).

**Status 2024-08-18** : individual processes running (very slowly on a GPU-less computer) locally

**Caveat** : my goal was to see what I could do with one specific recording without going to far down the rabbit hole. While I'm familiar with (conventional) audio techniques, video/image processing isn't something I've spent much time with, so most of this is from a perspective of learning as I go along, can no doubt be significantly improved on. But I think the overall workflow more or less makes sense.

Parameters tweaks should make for easy improvement (trial & error time aside), out of ignorance I've simply used defaults. Different algorithms/models will be worth trying. If I were to take this further today, I'd try a combination of algorithms and interleaving the results (little bit of Python tweakage, give the frames odd/even numbered names or whatever).

## Prep

I assume I used [yt-dlp](https://github.com/yt-dlp/yt-dlp) to download the original video _(for which I've lost the link)_. I typical do a two-part operation :

- `yt-dlp -F <YouTube URL>` - lists available formats, with short ref numbers
- `yt-dlp -f <ref number> <YouTube URL>` - downloads video in that format

**Warning : this free download almost certainly contravenes YouTube's terms of service, so, er, be warned**

I (presumably) got the audio-only and video-only versions that looked best quality.

## Audio Cleanup

First pass, I tried various conventional tools. I forget which, but one will have been the noise reduction in [Audacity](https://www.audacityteam.org/). You give that a sample of the noise in the background, I assume it does an FFT. Then run again, I assume it runs a filter based on the FFT. This was remarkably useless on the audio I had from the video.

I did try a couple of open source ML-based tools, without success. Wait by the river until the body of the tool I want floats by...

Then I heard of [Eleven Labs' Voice Isolator](https://elevenlabs.io/voice-isolator). Because I anticipated this needing a bit of experimentation I signed up for their 'Creator' subscription, which cost $13.42 for the first month. It may even have been on the first run, I got a good result. It now says I've used 37% of my character quota, whatever that is. I've cancelled renewal for now (there are probably other bits I can use elsewhere, dunno yet).

## Video Cleanup

### Strategy

_you can make a silk purse out of a sow's ear if you have a model that has spent it's whole life comparing them_

After a little research, I settled on this processing sequence :

1. Extract individual frames as images from original video
2. Upscale/improve individual frames
3. Interpolate new frames
4. Render interpolated frames into video

For implementation, because typically ML=Python, it was the obvious choice of language.

This was bound to be processor-hungry and I don't have a usable GPU here, so I decided to :

- code up each step individually as regular Python
- test on a snippet of the video (400 frames, 50s)
- join code together
- convert into a notebook for HuggingFace and/or Colab

_At this point I brought in my colleagues ChatGPT4o, Cursor (via OpenAI API) and Claude 3.5 Sonnet. Henceforth plural personal pronouns may appear._

1 & 4 were pretty straightforward with `python-ffmpeg`. We haven't looked closely at the decoding/encoding format & parameters, they may well be suboptimal. I did suggest 'non-lossy' to the team, I don't know if they listened.

After a bit of hunting & trial trial trial & error error error, the following were chosen for 2 & 3 :

- Upscaling : **Real-ESRGAN** super-resolution ([paper](https://arxiv.org/abs/2107.10833)), ([original implementation](https://github.com/xinntao/Real-ESRGAN)). We used this [PyTorch implementation from GitHub](https://github.com/ai-forever/Real-ESRGAN)
- Interpolation : **RIFE** (Real-Time Intermediate Flow Estimation for Video Frame Interpolation) in the shape of [rife-ncnn-vulkan](https://github.com/nihui/rife-ncnn-vulkan) ([paper](https://arxiv.org/abs/2011.06294))

The former had a tweakable example, the latter actually has a standalone binary release **which works!**

- Other Techniques
- File List
- Background

* [verbose, disorganised notes](docs/2024-08-14_video-enhancement.md)

### Strategy

### Tools Used

### Filelist

## Background

A while ago [danbri](https://x.com/danbri) (/[danbri.org](https://danbri.org/)) asked me to see what I could do with an video of a presentation he & Edd _(TODO current link?)_ did about the [FOAF Project](https://en.wikipedia.org/wiki/FOAF) years ago. The a/v quality was terrible. I was reasonably confident I'd be able to improve the audio using conventional techniques, but this turned out to be far less successful than I thought. On the video side, I didn't have a clue at first.
