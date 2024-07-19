# Scrappy notes 2024-08-19

So far, `main.py` appears to be working properly locally.

#### Housekeeping

`.gitignore` tweaked to allow the data dirs but not their contents. An empty `.gitkeep` file created in each so (hopefully) the dirs will be replicated.

I've also tweaked

```
def delete_files(folder):
```

in `main.py` so `.*` files aren't deleted.

### Convert .py to .ipynb

[colab-convert](https://github.com/MSFTserver/colab-convert) looked handy.

But it (`colab-convert==2.0.5`) failed :

```
colab-convert src/main.py src/main.ipynb
...
UnboundLocalError: cannot access local variable 'main_metadata' where it is not associated with a value
```

So I forked & cloned & fixed the source _("...and I will call him George.")_ : https://github.com/danja/colab-convert

I can't be bothered looking up how to get this bit running inside the venv, isn't needed. Just from a regular terminal:

```
colab-convert /home/danny/foaf-archive-support/video-magic/src/main.py /home/danny/foaf-archive-support/video-magic/src/main.ipynb
```

`main.ipynb` looks promising. I now need to sort out the other Colab-specific bits.

Restart session, hmm
