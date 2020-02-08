import json
import subprocess
import sys
import argparse

defaultArgs = ["youtube-dl", "--extract-audio", "--audio-format", "mp3", "-o", "%(title)s.%(ext)s"]

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

def getLocallyDownloadedSongs():
    process = subprocess.Popen(['ls'], stdout=subprocess.PIPE)
    out, err = process.communicate()
    
    if err:
        sys.exit("OOPS: \n" + err)

    cleanOutput = parseRawCmdOutput(out)
    localFiles = cleanOutput.split("\n")

    # filtre *.mp3 files only
    return [filename for filename in localFiles if filename[-4:] == '.mp3']


def fetchName(url):
    args = ["youtube-dl", "--get-title", "--get-id", "--skip-download"]
    process = subprocess.Popen(args + [url], stdout=subprocess.PIPE)
    out, err = process.communicate()
    
    if err:
        sys.exit("OOPS: \n" + err)
    
    return parseRawCmdOutput(out).split("\n")


def download(entries):
    total = len(entries)
    count = 0
    print('Starting downloading ' + str(total) + ' songs')

    for entry in entries:
        
        count += 1
        progress = count / total * 100
        print('Downloading ' + str(count) + ' of ' + str(total) + ' : ' + str(round(progress, 0))[:-2] + '%')

        process = subprocess.Popen(defaultArgs + [entry["url"]], stdout=subprocess.PIPE)
        out, err = process.communicate()
        if err:
            sys.exit("OOPS: \n" + err)


# theseEntries : array of entries to be download
# ignoringTheseFilenames : array of file names to be ignored if match any url's title
def safeDownload(theseEntries, ignoringTheseFilenames):
    changes = False
    print('Syncing...')

    # calc how many song are unsynced ~ we are going to download
    unSyncedSongs = []
    for idx, entry in enumerate(theseEntries):

        if "url" not in entry:
            sys.exit("OOPS: there's an entry without a `url`\n")

        if "name" not in entry:
            entry["name"], _ = fetchName(entry["url"])
            changes = True
        
        okDownloadIt = str(entry["name"] + ".mp3") not in ignoringTheseFilenames
        
        if okDownloadIt:
            unSyncedSongs.append(entry)

    allSynced = len(unSyncedSongs) == 0
    
    if allSynced:
        print('There\'s nothing to download; it\'s all synced')
        return

    download(unSyncedSongs)
    return changes


def main(jsonInputFile):
    
    # get the input data
    with open(jsonInputFile, 'r') as file:
        data = json.load(file)
        inputData = data['download']

    alreadyDownloaded = getLocallyDownloadedSongs()

    changes = safeDownload(theseEntries=inputData, ignoringTheseFilenames=alreadyDownloaded)

    if changes:
        with open(jsonInputFile, 'w') as outfile:
            json.dump({'download': inputData}, outfile, indent=2)


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()

    parser.add_argument("jsonInputFile", nargs='?', default='sync.json', help="json input file with links to sync")
    # optional args
    # parser.add_argument("--verbosity", help="increase output verbosity")
    args = parser.parse_args()

    # if args.verbosity:
    #     print("verbosity detected", args.verbosity)            

    main(args.jsonInputFile)