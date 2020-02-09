![Screenshot 1](https://i.imgur.com/kf2rsTW.jpg)

- parse your sync.json file
- download its content to ./

### requires
- https://github.com/ytdl-org/youtube-dl/
- ffmpeg or avconv and ffprobe or avprobe

### usage
	$ python3.7 main.py sync.json
	
	$ python3.7 main.py --help
	usage: main.py [-h] [--allInRoot] [jsonInputFile]

	positional arguments:
	  jsonInputFile  json input file with links to sync

	optional arguments:
	  -h, --help     show this help message and exit
	  --allInRoot    download all songs in current dir skipping subfolders


### recommended
in your term rc file: `alias sync="python ~/Workspace/python/grand-theft-mp3/main.py"`


with `./sync.json` looking like:

	{
	  "./": [
	    {
	      "url": "https://www.youtube.com/watch?v=OxnxJpFAzqg&feature=youtu.be"
	    },
	    {
	      "url": "https://www.youtube.com/watch?v=B3gbisdtJnA"
	    },
	    {
	      "url": "https://www.youtube.com/watch?v=n3VjKtROscQ"
	    },
	    {
	      "url": "https://www.youtube.com/watch?v=C-u5WLJ9Yk4",
	      "name": "Britney Spears - ...Baby One More Time"
	    }
	  ],
	  "classical": [
	    {
	      "url": "https://www.youtube.com/watch?v=oy2zDJPIgwc",
	      "name": "Eine Kleine Nachtmusik - Mozart"
	    }
	  ]
	}
