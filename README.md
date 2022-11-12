# Khan Academy Video Translation

This project translates Khan Academy videos, evaluates translations, and contains a contribution platform to receive translation corrections. Try it out [here](https://chrome.google.com/webstore/detail/khan-academy-video-transl/gbpgbjnhccemhkjedfadjbekpmaoembh).

## Installation

Recommended Python version: Python 3.8.10.  
After cloning, install required packages in your virtual environment using [pip](https://pypi.org/project/pip/).

```bash
pip install -r requirements.txt
```
Note: Pytorch needs to be installed separately, see guide [here](https://pytorch.org/).
## Usage
7 arguments are taken: single_video, url, language, data_path, gen_output_video.  
single_video: A Boolean indicating whether you are translating one or multiple videos.  
url: A youtube link as a String if translating a single video, otherwise a path to a txt file with a unique youtube link on each line.  
language: The destination language code as a String; currently only 'zh-cn' (simplified Chinese) and 'es' (spanish) are supported.  
data_path: The path of the root folder which you would like the translation sentence data to be stored.
download_path: The path where videos will be be stored. Use the same path for each run to prevent redownloading videos.
translator: the translator you would like to use; current translators include 'deepl' and 'google'. 
gen_output_video: A Boolean indicating whether or not you want to generate translated videos.
```bash
# translate youtube.com/watch?v=NQSN00zL5gg to chinese using the deepl model
python3 main.py --single_video true --url 'youtube.com/watch?v=NQSN00zL5gg' --language zh-cn --data_path /home/user/data --download_path /home/user/downloaded_videos --tranlsator deepl --gen_output_video true

#translate multiple videos in /home/usr/Desktop/links.txt to spanish with google translate, storing data files in /home/user/Desktop/data
python3 main.py --single_video false --url /home/usr/Desktop/links.txt --language es --data_path /home/user/Desktop/data --download_path /home/user/downloaded_videos translator google gen_output_video True
```



## Issues
If Pafy gives 'KeyError: 'dislike_count'', navigate to the directory where Pafy is installed, and comment out line 54.  
If you get 'FileNotFoundError: [Errno 2] No such file or directory: 'ffprobe'', run: 
```bash
sudo apt install ffmpeg
```


Using the Extension and App
1. Navigate to a Khan Academy on YouTube
2. Press the extension, and the language you want to see or contribute with
3. Select 'Translate' to watch the video, or 'Contribute' if you notice an inaccurate translation

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


