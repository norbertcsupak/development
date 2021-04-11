from pytube import YouTube
from moviepy.editor import *
import argparse
import moviepy.editor as mp
import re
import os
from tkinter import Tk
import threading
import time

root = Tk()
linkBuffer = []
semaphor = threading.Semaphore(0)
MAX_YOUTUBE_DL_THREADS = 5
maxthreads = threading.BoundedSemaphore(MAX_YOUTUBE_DL_THREADS)


parser = argparse.ArgumentParser(description='Process the file')
parser.add_argument('--targetd',type=str,help='target directory to  place the grabbed  files',required=True)
args = parser.parse_args()

def getClipboard():
    x = root.clipboard_get()
    return x

def watch_clipboard():
    print("creating clipboard module.....")
    new = getClipboard()
    while True:

        old = getClipboard()
        while old == new:
            new = getClipboard()
            time.sleep(0.1)
        if "www.youtube.com" in new:
            save_link(new)
            semaphor.release()
            print(new)
        
def save_link(link):
    linkBuffer.append(link)

class LinkWatcher:
    def __init__(self):
        self.watcher()

    def grab(self, link):
        youtube_link = link
        y = YouTube(youtube_link)
        t = y.streams.filter(only_audio=True).all()
        print(f'Starting to grab the link...')
        t[0].download(output_path=args.targetd)
        maxthreads.release()
        self.mp4tomp3()

    def mp4tomp3(self):
        tgt_folder = args.targetd
        for file in [n for n in os.listdir(tgt_folder) if re.search('mp4', n)]:
            full_path = os.path.join(tgt_folder, file)
            output_path = os.path.join(tgt_folder, os.path.splitext(file)[0] + '.mp3')
            clip = mp.AudioFileClip(full_path).subclip(10, )  # disable if do not want any clipping
            print(f'starting  to convert mp4 : {output_path}')
            clip.write_audiofile(output_path)
            if os.path.exists(full_path):
                print(f'Removing mp4 files after convert to mp3: {full_path}')
                os.remove(full_path)
            else:
                print("The file does not exist")

    def watcher(self):
        print("watching youtube links in clipboard ...")
        while True:
            semaphor.acquire()
            maxthreads.acquire()
            link = linkBuffer.pop(0)
            tr = threading.Thread(target=self.grab, args = ([link]))
            tr.start()


# create the event handler
if __name__ == "__main__":
    links_watcher = threading.Thread(target=LinkWatcher)
    links_watcher.start()
    watch_clipboard()
