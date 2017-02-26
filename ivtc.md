## Inverse telecine

Inverse telecine: restore 29.97fps video to original film frame rate of 24fps. 
* Output framerate will actually be 23.976 fps.

### Single input

```
ffmpeg -i inputfile \
       -c:v libx264 \
       -vf fieldmatch,yadif=deint=interlaced,decimate \
       deinterlaced_output.mp4
```
* [Source](https://forum.doom9.org/showthread.php?t=172289) for command

<!-- TEST:
ffmpeg -i VTS_01_1.VOB -c:v libx264 -preset veryfast -vf fieldmatch,yadif=deint=interlaced,decimate deinterlaced_output.mp4 -->

### Multiple inputs

i.e., `.VOB`s from DVD.

#### 1. List files inline

```
ffmpeg -i concat:first.VOB\|second.VOB\|third.VOB \
       -c:v libx264 \
       -vf fieldmatch,yadif=deint=interlaced,decimate \
       deinterlaced_concat_output.mp4
```

<!-- TEST:
ffmpeg -i concat:VTS_01_1.VOB\|VTS_01_2.VOB -c:v libx264 -preset veryfast -vf fieldmatch,yadif=deint=interlaced,decimate deinterlaced_concat.mp4 -->
<!-- ffmpeg -i concat:VTS_01_0.VOB\|VTS_01_1.VOB -c:v libx264 -preset veryfast -vf fieldmatch,yadif=deint=interlaced,decimate deinterlaced_concat_just2.mp4 -->

#### 2. List files in `.txt`

```
ffmpeg -f concat -safe 0 -i inputs.txt \
       -c:v libx264 \
       -vf fieldmatch,yadif=deint=interlaced,decimate \
       deinterlaced_concat_output.mp4
```

where _inputs.txt_ contains the list of VOBs/other files to concat, in the format:

<blockquote>file './first.VOB'  
file './second.VOB'  
. . .  
file './last.VOB'</blockquote>

<!-- TEST:
ffmpeg -f concat -safe 0 -i inputs.txt -c:v libx264 -preset veryfast -vf fieldmatch,yadif=deint=interlaced,decimate deinterlaced_concat_list.mp4 -->

**Note**: Of the first two methods, ffmpeg seemed happier with no.1 (inline concat) than no. 2 (`.txt` input). Unsure why.

#### 3. Use a loop to work iteratively

The ffmpeg wiki entry on concatenation [lists three methods](https://trac.ffmpeg.org/wiki/Concatenate#demuxer) by which you can avoid creating a list file and do the whole thing in a single line. However, I did not yet get any of them to work for IVTC + concat.  
My current solution is the following:

#### 4. Automate via bash script

```
#!/bin/bash

function IVTCfiles() {

  # Set variables if no arguments are passed in: file extension is VOB and output filename is "output"
  extension=${1:-"VOB"}
  filename=${2:-"output"}
  echo $filename

  # Transcode individual files
  for item in *.$extension;
    do ffmpeg -i $item -c:v libx264 \
              -vf fieldmatch,yadif=deint=interlaced,decimate \
              "${item%.$extension}_ivtctemp.mp4";
    echo "Created '${item%.$extension}_ivtctemp.mp4'";
    done

  # Concat outputs to one MP4 file
  ffmpeg -f concat -safe 0 -i \
    <(for f in ./*ivtctemp.mp4; do echo "file '$PWD/$f'"; done) \
      -map 0 -c copy \
      $filename.mp4;
  echo "Individual IVTCed files concatenated into $filename.mp4";

  # Delete interim MP4s
  for g in ./*ivtctemp.mp4;
    do echo "Deleting $g ..." && rm -v $g;
    done
}

# Call function: IVTCfiles [<extension> <outputfilename>]
IVTCfiles VOB mybestfile
```
