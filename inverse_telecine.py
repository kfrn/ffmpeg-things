#!/usr/bin/python3

import fnmatch
import os
import subprocess
from sys import argv
from sys import exit

if len(argv) <= 1:
    print("Please enter an argument to the script. Exiting")
    exit()
else:
    input = argv[1]

def basic_ffmpeg_ivtc_command(input, output):
    return "ffmpeg -hide_banner -i '" + input + "' -c:v libx264 -vf 'fieldmatch,yadif,decimate' '" + output + "'"

def concat_ffmpeg_ivtc_command(concat_file, output):
    return "ffmpeg -hide_banner -f concat -safe 0 -i " + concat_file + " -c:v libx264 -vf 'fieldmatch,yadif,decimate' " + output

def strip_file_extension(input):
    return os.path.splitext(input)[0]

def output_filename(input):
    if os.path.isfile(input):
        return "%s_ivtc.mp4" % strip_file_extension(input)
    elif os.path.isdir(input):
        return ("%s_ivtc.mp4" % input).strip("./")

def create_file_for_concat(input):
    txtfile = open("%s/temp.txt" % input, "w+")
    for file in sorted(os.listdir(input)):
        if '.VOB' in file:
            txtfile.write("file '%s' \n" % (file))

def delete_interim_files(input):
    os.remove("%s/temp.txt" % input)

def create_ivtc_file(input):
    if os.path.isfile(input):
        print("You've input a single file: %s" % input)
        output = output_filename(input)
        ffmpeg_ivtc_command = basic_ffmpeg_ivtc_command(input, output)
        print("The output file & path will be: %s" % output)
        print("Calling the following ffmpeg command: \n %s" % ffmpeg_ivtc_command)
        subprocess.run(ffmpeg_ivtc_command, shell=True)
    elif os.path.isdir(input):
        print("You've input a directory: %s" % input)
        create_file_for_concat(input)
        concat_file = "%s/temp.txt" % input
        output_path = input + "/" + output_filename(input)
        ffmpeg_concat_command = concat_ffmpeg_ivtc_command(concat_file, output_path)
        print("The output file & path will be: %s" % output_path)
        print("Calling the following ffmpeg command: \n %s" % ffmpeg_concat_command)
        subprocess.run(ffmpeg_concat_command, shell=True)
        delete_interim_files(input)
        print("Done! Your finished file is %s" % output_filename(input))

create_ivtc_file(input)
