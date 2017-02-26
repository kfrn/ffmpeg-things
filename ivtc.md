## Inverse telecine

Inverse telecine: restore 29.97fps video to original film frame rate of 24fps. (Output framerate will actually be 23.976 fps).

#### Single input:  

```
ffmpeg -i inputfile \
       -c:v libx264 \
       -vf fieldmatch,yadif=deint=interlaced,decimate \
       deinterlaced_output.mp4
```
* [Source](https://forum.doom9.org/showthread.php?t=172289) for command

<!-- TEST:
ffmpeg -i VTS_01_1.VOB -c:v libx264 -preset veryfast -vf fieldmatch,yadif=deint=interlaced,decimate deinterlaced_output.mp4 -->

#### Multiple inputs:

I.e., `.VOB`s from DVD.

##### 1. List files inline

```
ffmpeg -i concat:first.VOB\|second.VOB\|third.VOB \
       -c:v libx264 \
       -vf fieldmatch,yadif=deint=interlaced,decimate \
       deinterlaced_concat_output.mp4
```

<!-- TEST:
ffmpeg -i concat:VTS_01_1.VOB\|VTS_01_2.VOB -c:v libx264 -preset veryfast -vf fieldmatch,yadif=deint=interlaced,decimate deinterlaced_concat.mp4 -->
<!-- ffmpeg -i concat:VTS_01_0.VOB\|VTS_01_1.VOB -c:v libx264 -preset veryfast -vf fieldmatch,yadif=deint=interlaced,decimate deinterlaced_concat_just2.mp4 -->

##### 2. List files in `.txt`

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

##### 3. Use a loop work iteratively - TBA

<!-- The all-in-one method, [using a loop](https://trac.ffmpeg.org/wiki/Concatenate#demuxer). The following will concat, transcode and IVTC all `.VOB` files in a directory:

```
ffmpeg -f concat -safe 0 \
       -i <(for f in ./*.VOB; do echo "file '$PWD/$f'"; done) \
       -c:v libx264 \
       -vf fieldmatch,yadif=deint=interlaced,decimate \
       deinterlaced_output.mp4

```

TEST 1:
ffmpeg -f concat -safe 0 -i <(for f in ./*.VOB; do echo "file '$PWD/$f'"; done) -c:v libx264 -preset ultrafast -vf fieldmatch,yadif=deint=interlaced,decimate deinterlaced_output_loop.mp4
// The above doesn't seem to concat :(

TEST 2
ffmpeg -f concat -safe 0 -i <(find . -name '*.VOB' -printf "file '$PWD/%p'\n") -c:v libx264 -preset ultrafast -vf fieldmatch,yadif=deint=interlaced,decimate deinterlaced_output_loop_test2.mp4
// in prog

TEST 3
ffmpeg -f concat -safe 0 -i <(printf "file '$PWD/%s'\n" ./*.VOB) -c:v libx264 -preset ultrafast -vf fieldmatch,yadif=deint=interlaced,decimate deinterlaced_output_loop.mp4

**Note**: Preferred method is no. 3, but of the first two, ffmpeg seemed happier with no.1 (inline concat) than no. 2 (`.txt` input). Unsure why. -->
