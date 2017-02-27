## Inverse telecine

#### Page contents:
* [Single input](#single-input)
* [Multiple inputs](#multiple-inputs)
* [IVTC settings](#ivtc-settings)
* [Comparison GIFs](#comparison-gifs)

An **inverse telecine** procedure reverses the [3:2 pull down](https://en.wikipedia.org/wiki/Three-two_pull_down) process. It restores 29.97fps interlaced video to the original film source's frame rate of 24fps.
* Output framerate will actually be 23.976 fps.

### Single input

Basic script:
```
ffmpeg -i inputfile \
       -c:v libx264 \
       -vf "fieldmatch,yadif,decimate" \
       ivtc_output.mp4
```
* [Source](https://forum.doom9.org/showthread.php?t=172289) for basis of command

<!-- TEST:
ffmpeg -i *.VOB -c:v libx264 -preset veryslow -vf "fieldmatch,yadif,decimate" ivtc_output.mp4 -->

### Multiple inputs

i.e., `.VOB`s from DVD.

#### 1. List files inline

```
ffmpeg -i concat:first.VOB\|second.VOB\|third.VOB \
       -c:v libx264 \
       -vf "fieldmatch,yadif,decimate" \
       ivtc_concat_output.mp4
```

#### 2. List files in `.txt`

```
ffmpeg -f concat -safe 0 -i inputs.txt \
       -c:v libx264 \
       -vf "fieldmatch,yadif,decimate" \
       ivtc_concatlist_output.mp4
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

  # Set variables if no arguments are passed in: file extension is VOB and output filename is "ivtc_output"
  extension=${1:-"VOB"}
  filename=${2:-"ivtc_output"}

  # Transcode individual files
  for item in *.$extension;
    do ffmpeg -i $item -c:v libx264 \
              -vf "fieldmatch,yadif,decimate" \
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

### IVTC settings

* ffmpeg does a pretty good job of IVTC via the filterchain `-vf "fieldmatch,yadif,decimate"`, but results also depend on the encoding speed, the qualities of the source, etc.  
In particular, at high encoding speeds it's reasonably common for some frames not to be successfully deinterlaced.  
**⤷** In this case, ffmpeg prints a message like `[Parsed_fieldmatch_0 @ 0x34d63e0] Frame #20 at 1.23394 is still interlaced`.

* The [original post](https://forum.doom9.org/showthread.php?t=172289) where I got info on IVTC in ffmpeg used `yadif=deint=interlaced`, which only deinterlaces frames marked as interlaced. (See [ffmpeg docs](https://ffmpeg.org/ffmpeg-filters.html#yadif-1)). The `yadif` default is to deinterlace all frames. I had better results with `yadif`'s defaults. The `yadif=deint=interlaced` output looked pretty good, but had some artefacting that wasn't visible in the `yadif` default output (see GIFs below).

* `yadif` also has a mode that outputs one frame for each field (`yadif=mode=1`), which may look better than the default mode (`yadif=mode=0`, which outputs one frame for each frame). Results were also good.

### Comparison GIFs

Original video:  
![Original video](./images/original_video.gif "Original video")

IVTC with `yadif` defaults:  
![IVTC with yadif defaults](./images/ivtc_video_yadif-defaults.gif "IVTC with yadif defaults")

IVTC with `yadif=deint=interlaced`:  
![IVTC with yadif=deint=interlaced](./images/ivtc_video_yadif-deint-interlaced.gif "IVTC with yadif=deint=interlaced")

IVTC with `yadif=mode=1`:  
![IVTC with yadif=mode=1](./images/ivtc_video_yadif-mode-1.gif "IVTC with yadif=mode=1")
