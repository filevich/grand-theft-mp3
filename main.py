import re
import json
import subprocess
import sys
import argparse
import os

defaultArgs = ["youtube-dl", "--extract-audio", "--audio-format", "mp3", "-o"]

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

def getLocallyDownloadedSongs(subfolder):
    process = subprocess.Popen(['ls', subfolder], stdout=subprocess.PIPE)
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


def download(entries, here):
    total = len(entries)
    count = 0

    for entry in entries:
        
        count += 1
        progress = count / total * 100
        print('  Downloading [' + str(count) + '/' + str(total) + '] ' + entry['name'])

        url = entry["url"]
        dwnPath = here + "/" + "%(title)s.%(ext)s"

        process = subprocess.Popen(defaultArgs + [dwnPath, url], stdout=subprocess.PIPE)
        out, err = process.communicate()
        if err:
            sys.exit("OOPS: \n" + err)


# theseEntries : array of entries to be download
# ignoringTheseFilenames : array of file names to be ignored if match any url's title
# here : path to subfolder dest
def safeDownload(theseEntries, ignoringTheseFilenames, here):
    changes = False

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
        print('  It\'s all synced in here.')
        return

    download(unSyncedSongs, here)
    return changes


def main(jsonInputFile, allInRoot):
    
    # get the input data
    with open(jsonInputFile, 'r') as file:
        data = json.load(file)

    changes = False

    for subfolder in data:

        subfolderWithNoLastSlash = subfolder[:-1] if subfolder.endswith('/') else subfolder
        dwnSubFolder = '.' if allInRoot else subfolderWithNoLastSlash

        # safe check: does `subfolder` actually exists?
        process = subprocess.Popen(["mkdir", "-p", dwnSubFolder], stdout=subprocess.PIPE)
        out, err = process.communicate()
        if err:
            sys.exit("OOPS: \n" + err)

        alreadyDownloaded = getLocallyDownloadedSongs(dwnSubFolder)

        print('\nSyncing subfolder "%s" (with %d songs)...' %(subfolder, len(data[subfolder])) )
        changes = changes or safeDownload(theseEntries=data[subfolder], ignoringTheseFilenames=alreadyDownloaded, here=dwnSubFolder)

    if changes:
        with open(jsonInputFile, 'w') as outfile:
            json.dump(data, outfile, indent=2)


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()

    parser.add_argument("jsonInputFile", nargs='?', default='sync.json', help="json input file with links to sync")
    # optional flags
    parser.add_argument("--allInRoot", action="store_true", help="download all songs in current dir skipping subfolders")
    args = parser.parse_args()

    main(args.jsonInputFile, args.allInRoot)