import json
import subprocess

JSON_FILE_NAME = 'sync.json'

# youtube-dl --extract-audio --audio-format mp3 <video URL>

# The main difference is that subprocess.run executes a command
# and waits for it to finish, while with subprocess.Popen you can
# continue doing your stuff while the process finishes and then 
# just repeatedly call subprocess.communicate yourself to pass 
# and receive data to your process.

# subprocess.run(["youtube-dl", "--extract-audio --audio-format mp3 https://www.youtube.com/watch?v=n3VjKtROscQ"])
# VS:
# process = subprocess.Popen(['ls', '-a'], stdout=subprocess.PIPE)
# out, err = process.communicate()

def main():
    with open(JSON_FILE_NAME) as json_file:
        data = json.load(json_file)
        for song in data['download']:
            subprocess.run(["youtube-dl", "--extract-audio", "--audio-format", "mp3", "https://www.youtube.com/watch?v=n3VjKtROscQ"])

if __name__ == "__main__":
    main()