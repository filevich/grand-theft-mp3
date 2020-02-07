import json
import subprocess
import sys

JSON_INPUT_FILE = 'sync.json'
defaultArgs = ["youtube-dl", "--extract-audio", "--audio-format", "mp3"]

# youtube-dl --extract-audio --audio-format mp3 <video URL>

# The main difference is that subprocess.run executes a command
# and waits for it to finish, while with subprocess.Popen you can
# continue doing your stuff while the process finishes and then 
# just repeatedly call subprocess.communicate yourself to pass 
# and receive data to your process.

# subprocess.run(["youtube-dl", "--extract-audio", "--audio-format", "mp3", "https://www.youtube.com/watch?v=n3VjKtROscQ"])
# VS:
# process = subprocess.Popen(['ls', '-a'], stdout=subprocess.PIPE)
# out, err = process.communicate()

# def filtre_mp3_files_only(arr):
#     for file in arr:
#         1+1

def parseRawCmdOutput(rawCmd):
    return rawCmd.decode("utf-8").strip()

def getDownloadedSongs():
    process = subprocess.Popen(['ls'], stdout=subprocess.PIPE)
    out, err = process.communicate()
    
    if err:
        sys.exit("OOPS: \n" + err)

    cleanOutput = parseRawCmdOutput(out)
    localFiles = cleanOutput.split("\n")

    # filtre *.mp3 files only
    return [filename for filename in localFiles if filename[-4:] == '.mp3']


# urlsArr : youtube string-url array 
def urlsToFilenames(urlsArr):
    print('getting resources\' names:')
    res = []
    args = ["youtube-dl", "--get-title", "--get-id", "--skip-download"]
    total = len(urlsArr)
    count = 0
    
    for url in urlsArr:
        count += 1
        progress = count / total * 100
        print(str(round(progress, 0))[:-2] + '%')
        process = subprocess.Popen(args + [url], stdout=subprocess.PIPE)
        out, err = process.communicate()
        
        if err:
            sys.exit("OOPS: \n" + err)
        
        resourceData = parseRawCmdOutput(out).split("\n")
        res.append(resourceData)

    return res


def download(urls):
    total = len(urls)
    count = 0
    print('Starting downloading ' + str(total) + ' songs')

    for song in urls:
        
        count += 1
        progress = count / total * 100
        print('>> Downloading ' + str(count) + ' of ' + str(total) + ' : ' + str(round(progress, 0))[:-2] + '%')

        process = subprocess.Popen(defaultArgs + [song], stdout=subprocess.PIPE)
        out, err = process.communicate()
        if err:
            sys.exit("OOPS: \n" + err)


# theseURLs : array of youtube urls to be download
# ignoringTheseFilenames : array of file names to be ignored if match any url's title
def safeDownload(theseURLs, ignoringTheseFilenames):

    fetchedNames = urlsToFilenames(theseURLs)
    
    ok = len(fetchedNames) != len(theseURLs)
    if ok: 
        sys.exit("OOPS: something went wrong\n")

    # calc how many song are unsynced ~ we are going to download
    unSyncedSongs = []
    for idx, song in enumerate(theseURLs):
        
        futureSongName = fetchedNames[idx][0]
        futureSongId = fetchedNames[idx][1]
        futureFilename = futureSongName + "-" + futureSongId + ".mp3"
        
        okDownloadIt = futureFilename not in ignoringTheseFilenames
        if okDownloadIt:
            unSyncedSongs.append(song)

    allSynced = len(unSyncedSongs) == 0
    
    if allSynced:
        print('There\'s nothing to download; it\'s all synced')
        return

    download(unSyncedSongs)


def main():
    
    # get the input data
    with open(JSON_INPUT_FILE, 'r') as file:
        data = json.load(file)
        inputData = data['download']

    # get list of downloaded songs
    downloaded = getDownloadedSongs()

    safeDownload(theseURLs=inputData, ignoringTheseFilenames=downloaded)


if __name__ == "__main__":
    main()