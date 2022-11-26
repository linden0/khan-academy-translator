# Khan Academy Video Translation

This project translates Khan Academy videos, evaluates translations, and contains a contribution platform to receive translation corrections. Try it out [here](https://chrome.google.com/webstore/detail/khan-academy-video-transl/gbpgbjnhccemhkjedfadjbekpmaoembh). If you want to learn more about how this works, see [this](https://docs.google.com/document/d/1Et0Q74Ym-td6WVjxhCBnMAUpyijW8EUnwVttYoOLmYQ/edit?usp=sharing).

## Installation

Recommended Python version: Python 3.8.10/3.10  
After cloning, install required packages in your virtual environment using [pip](https://pypi.org/project/pip/).

```bash
pip install -r requirements.txt
```

## Usage
7 arguments are taken: single_video, url, language, data_path, download_path, translator, gen_output_video.  
* single_video
    * boolean indicating if translating one or multiple videos
* url
    * YouTube link if translating a single video, otherwise path to a txt file with line-separated YouTube links
    * if single video, make sure to use quotes
* language
    * ISO 639-1 language code of destination language
    * currently only 'zh-cn' (simplified Chinese) and 'es' (Spanish) are supported
* data_path
    * path of the root folder where translated videos and sentence data will be stored
* download_path
    * path where initial untranslated videos will be stored
    * use the same path for each run to avoid redownloading videos
* translator
    * the translator to be used, currently only 'deepl' and 'google' translate are available
* gen_output_video
    * boolean indicating if you would like to generate translated videos
    * 'False' typically used if you only want translated sentence data

## Examples
```bash
# translate youtube.com/watch?v=NQSN00zL5gg to chinese using the deepl model
python3 main.py --single_video true --url 'youtube.com/watch?v=NQSN00zL5gg' --language zh-cn --data_path /home/user/data --download_path /home/user/downloaded_videos --translator deepl --gen_output_video true

#translate multiple videos in /home/usr/Desktop/links.txt to spanish with google translate, storing data files in /home/user/Desktop/data
python3 main.py --single_video false --url /home/usr/Desktop/links.txt --language es --data_path /home/user/Desktop/data --download_path /home/user/downloaded_videos --translator google --gen_output_video True
```

## Issues
If Pafy gives 'KeyError: 'dislike_count'', navigate to the directory where Pafy is installed, and comment out line 54.  
If you get 'FileNotFoundError: [Errno 2] No such file or directory: 'ffprobe'', run:
```bash
sudo apt install ffmpeg
```


## Using the [Extension](https://chrome.google.com/webstore/detail/khan-academy-video-transl/gbpgbjnhccemhkjedfadjbekpmaoembh)
1. Navigate to a Khan Academy on YouTube
2. Press the extension, and select the language you want to see or contribute with
3. Select 'Translate' to watch the video, or 'Contribute' if you notice an inaccurate translation

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.