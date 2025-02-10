# TangaraCopy

Copy (and transcode) media files to a Tangara SD card.

Tangara Copy, copyright 2025 by [Brian Enigma](https://brianenigma.com), is licensed under Creative Commons Attribution-ShareAlike 4.0 International. To view a copy of this license, visit https://creativecommons.org/licenses/by-sa/4.0/

Project Website: https://github.com/BrianEnigma/TangaraCopy

## What

TangaraCopy lets you copy your music library to an SD card. It transcodes unsupported files, as needed, to mp3.

## Why

I love that the [Tangara](https://cooltech.zone/tangara/) is basically an Open Source re-imagining of the iPod. I pre-ordered it [on CrowdSupply](https://www.crowdsupply.com/cool-tech-zone/tangara) back in 2024. My music library has gone through a few iterations over the years, from flat-files on a filesystem (Winamp or similar), to iTunes, and back to flat files ([PlexAmp](https://www.plex.tv/plexamp/)). Something I didn't 100% catch was a fairly large incompatibility between my library and the codecs on the Tangara.

Because of this history, a large percentage of my music library is m4a (AAC) formatted, which is a codec the Tangara doesn't support.

The path of least resistance forward is, when copying to the Tangara SD card, copy mp3 files as-is, but transcode the AAC audio to mp3. That is what this script does.

## Prerequisites

- Python 3
- [ffmpeg](https://ffmpeg.org) in the path, built with [lame](https://lame.sourceforge.io) support.

## Configuring

Copy `config-example.py` to `config.py`. It looks a little something like this:

```
FOLDERS = {
    "/Volumes/Plex/Music/": "/Volumes/Tangara/Media/Music"
}
EXTENSIONS_COPY = [
    '.mp3'
]
EXTENSIONS_TRANSCODE = [
    '.m4a'
]
FFMPEG_GLOBAL_OPTIONS = ["-hide_banner", "-loglevel", "error"]
FFMPEG_ENCODE_OPTIONS = ["-b:a", "192k"]
```

The main item in the config you should edit is:

- `FOLDERS` is a map from source folder to destination folder. Files (and folders) are recursively copied from source to destination. They are transcoded as required.

The remainder of the settings are generally fine when left as-is. Advanced users can edit them as needed:

- `EXTENSIONS_COPY` is a list of file extension to simply copy over as-is.
- `EXTENSIONS_TRANSCODE` is a list of file extension to transcode into mp3.
- Unrecognized extensions are not copied.
- `FFMPEG_GLOBAL_OPTIONS` is a list of options to give before the input file. By default, these are flags to quietly transcode.
- `FFMPEG_ENCODE_OPTIONS` is a list of options to give between the input and output files. By default, this says to encode at 192K.

## Running

After editing your configuration, simply run `./tangaracopy.py`

As a quick test, you can use the `-c` flag, which will stop after that many files. For example `./tangaracopy.py -c 50` will only copy 50 files to the destination.

## Known Issues

- This is a copy script, not a sync script. Files that have since been deleted or changed in the source folder do not get updated or deleted in the destination folder. This kind of sync is out-of-scope for this particular project.
- It is possible that if you interrupt the script, you will get a corrupt or truncated file. The next time you run it, it will detect this file as existing and not attempt to overwrite it. If you do this, please note the album where you interrupted the script and delete it from the destination.
