## Inverse telecine

An **inverse telecine** procedure reverses [3:2 pull down](https://en.wikipedia.org/wiki/Three-two_pull_down) - it restores 29.97fps interlaced video to the original film source's frame rate of 24fps.
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
ffmpeg -i *.VOB -c:v libx264 -preset veryslow -vf fieldmatch,yadif=deint=interlaced,decimate ivtc_output.mp4 -->

### Multiple inputs

i.e., `.VOB`s from DVD.

#### 1. List files inline

```
ffmpeg -i concat:first.VOB\|second.VOB\|third.VOB \
       -c:v libx264 \
       -vf fieldmatch,yadif=deint=interlaced,decimate \
       deinterlaced_concat_output.mp4
```

#### 2. List files in `.txt`

```
ffmpeg -f concat -safe 0 -i inputs.txt \
       -c:v libx264 \
       -vf fieldmatch,yadif=deint=interlaced,decimate \
       deinterlaced_concat_output.mp4
```

where _inputs.txt_ contains the list of VOBs/other files to concat, in the format:

<blockquote>file './first.VOB'<br>  
file './second.VOB'<br>   
. . .<br>   
file './last.VOB'</blockquote>

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

**Note**: ffmpeg does a pretty good job of IVTC with the filter `-vf fieldmatch,yadif=deint=interlaced,decimate`, but I've observed that results also depend on the encoding speed, the qualities of the source, etc.  
In particular, at high encoding speeds, it's reasonably common for some frames not to be successfully deinterlaced.  
**⤷** In this case, ffmpeg prints a message like `[Parsed_fieldmatch_0 @ 0x34d63e0] Frame #20 at 1.23394 is still interlaced`.
