#This is a script that takes client provided MTS files, and makes a transcoded and
#renamed version of the MTS files on a local directory.
#The files can then be imorted into Premiere Pro or Avid Media Composer.
#Normally I would use Adobe Media Encoder or Davinci Resolve Lite to transcode
#this sort of file.

import os
import subprocess
root_dir = '/Volumes/Client_Drive'
dest_root = '/Volumes/Our_Drive'
FFMPEG_PATH = '/usr/bin/ffmpeg'



#Returns a list of directories that contain .MTS files from the root_dir.

def find_dir_with_mts(root_dir):
    directories = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".MTS"):
                directories.append(root)
    directories_set = set(directories)
    directories = list(directories_set)
    return directories


#Recreates on a destination drive part of the path of the MTS directies
#(Day 1/Cam A/Roll 3) and omits unneccessary directories.
#It also prepend's .MTS file names with the partial path.
#It then uses FFMPEG to create ProRes files with the prepended filename,
#and in the recreated path on the destination drive.

#This will only work with the correct number of directories on the sources drive.
#It needs to be more interactive, allow for different directory structures,
#show you what it will do before it does it.
#It could also have the option of doing a rename and copy with no FFMPEG transcode.

#It would be great if this could retain or create a reelname / timecode.

def make_folders_on_dest_drive(source_dirs, dest_root):
    for dirs in source_dirs:
        temp = dirs.split('/')
        temp = temp[2:6]
        prepend = temp
        prepend = '_'.join(prepend)
        prepend = prepend + '_'
        temp.insert(0, '')
        new_path = '/'.join(temp)
        new_path = dest_root + new_path
        os.makedirs(new_path)
        mts = os.listdir(dirs)
        temp_path = new_path + "/"
        for i in mts:
            temp_source = dirs + '/' + i
            print temp_source
            name = ''.join(i.split('.')[:-1])
            output = '{}.mov'.format(name)
            output = prepend + output
            output = temp_path + output
            subprocess.call([FFMPEG_PATH, '-i', temp_source, '-c:v', 'prores', '-profile:v', '1', '-c:a', 'pcm_s16le', output])


a = find_dir_with_mts(root_dir)
make_folders_on_dest_drive(a, dest_root)