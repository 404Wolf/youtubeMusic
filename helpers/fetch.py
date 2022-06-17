import pytube
import asyncio
import os

async def fetch(url: str, filepath=None):
    """
    Download audio of youtube video and automaticaly inject metadata

    Args:
        url (str): URL of video to download.
        filepath (str, optional): Filepath up to the name of file. File extension automatically added.
    """
    stream = pytube.YouTube(url) # fetch youtube video
    stream = stream.streams.filter(only_audio=True, mime_type="audio/mp4") # fetch all versions of video/audio
    stream = sorted(stream, key=lambda stream: stream.filesize, reverse=True) # sort by filesize
    stream = stream[0] # choose largest file
    stream.download() # download file
    stream.filetype = stream.mime_type.split("/")[1] # obtain file extension

    # if given a specified filepath then use it
    if isinstance(filepath, str):
        os.rename(f"{stream.title}.{stream.filetype}", f"{stream.filepath}.{stream.filetype}")