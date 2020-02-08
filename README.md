- parse your sync.json file
- download its content to ./

### requires
	- https://github.com/ytdl-org/youtube-dl/
	- ffmpeg or avconv and ffprobe or avprobe

### usage
	$ python3.7 main.py sync.json

with `./sync.json` looking like:

	{
	  "download": [
	    {
	      "url": "https://www.youtube.com/watch?v=OxnxJpFAzqg&feature=youtu.be",
	      "name": "Walking On A Dream x Yes Indeed (JStrain Mashup)"
	    },
	    {
	      "url": "https://www.youtube.com/watch?v=B3gbisdtJnA",
	      "name": "Shakira - Ciega, Sordomuda (Video Oficial)"
	    },
	    {
	      "url": "https://www.youtube.com/watch?v=n3VjKtROscQ",
	      "name": "Lizzo - Juice (Lyrics)"
	    },
	    {
	      "url": "https://www.youtube.com/watch?v=C-u5WLJ9Yk4",
	      "name": "Britney Spears - ...Baby One More Time"
	    }
	  ]
	}
