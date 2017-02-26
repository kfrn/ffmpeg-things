## Access derivative videos

#### General Notes
* If original source is progressive, replace `-vf 'yadif,format=pix_fmts=yuv420p'` with just `-pix_fmt yuv420p`, as `yadif` is the deinterlacing filter.
* CABAC is the [default entropy encoder](https://sites.google.com/site/linuxencoding/x264-ffmpeg-mapping) used by `libx264`. To enable explicitly, add `-coder 1`. To disable, use `--no-cabac` or `-coder 0`.

----

#### Archives NZ

**Specs**:
* H.264/AAC/MP4.
* Video: high profile @ L5, var bitrate, 1 pass, target 2 Mbps, max 20 Mbps.
* Audio: 192kbps, 48kHz.
* Colour space = Rec.601 (BT.601 PAL, aka BT.470BG).
  * See the [current H.264 standard](https://www.itu.int/rec/T-REC-H.264-201610-I/en): p.391 table entry 5, p.393 table entry 5, p.397 table entry 5. (Via [Stack Overflow](http://video.stackexchange.com/questions/16840/ffmpeg-explicitly-tag-h-264-as-bt-601-rather-than-leaving-unspecified)).

**Script**:  

```
ffmpeg -i pres_master.mov \
   -c:v libx264 -profile:v high -level:v 5.0 \
   -vf 'yadif,format=pix_fmts=yuv420p' \
   -color_primaries bt470bg -color_trc gamma28 -colorspace bt470bg \
   -c:a libfdk_aac -ar 48000 -b:a 192k \
   access_derivative.mp4
```

**Notes**:
* Approximation of the ADs we made in MediaEncoder at Archives NZ.
* GOP structure (M=3, N=14) not maintained. For info on setting i-frame & b-frame distance with `libx264`, see [here](https://sites.google.com/site/linuxencoding/x264-ffmpeg-mapping).
* Not setting bitrate, crf, preset, etc. Using libx264 [default settings](https://trac.ffmpeg.org/wiki/Encode/H.264) of crf = 23 and preset = medium.
  * To set bitrate of 2 Mbps, add `-b:v 1808k -bufsize 1808k` (2MB - 192K for audio).

----

#### UNC Chapel Hill, Wilson Round Library Special Collections

**Specs**:
* H.264, MP4 (5000kbps) [[source](http://library.unc.edu/wilson/sfc/audiovisual-preservation/technical-specifications/)]

**Script**:  

```
ffmpeg -i pres_master.mov \
   -c:v libx264 -vf 'yadif,format=pix_fmts=yuv420p' \
   -b:v 4872k -bufsize 4872k \
   -c:a libfdk_aac -b:a 128k \
   access_derivative_UNC.mp4
```

----

#### California Audiovisual Preservation Project (CAVPP)

**Specs**:
* H.264/AAC/MP4
* Bitrate: 1500 Kbps fixed
* Video: 720x540, 29.97 fps, progressive, 4:3 AR
  * 720x540 = ‘square-pixel SD’ for 525-line/‘NTSC’ video. Resized on the vertical dimension rather than the more common practice of resizing on the horizontal dimension (i.e. 640x480).
    * Not what I would do. I'd resize horizontally to avoid resampling scanlines. Therefore, the below script resamples to 640x480 ‘square-pixel SD’.
* Audio: AAC, 160 Kbps, 44.1 kHz.
* [Source (PDF)](https://calpreservation.org/wp-content/uploads/2013/10/CAVPPTargetAudioandVideo-Specs2013_IMLS.pdf)


**Script**:  

```
ffmpeg -i pres_master.mov \
   -s 640x480 -r 30000/1001 \
   -c:v libx264 -vf 'yadif,format=pix_fmts=yuv420p' \
   -b:v 1340k -bufsize 1340k \
   -c:a libfdk_aac -ar 44100 -b:a 160k \
   access_derivative_CAVPP.mp4
```

**Notes**:
* Script resamples to 640x480 rather than 720x540. So doesn't actually follow CAVPP's specs!
* Script works, but need 720x480/50i source video to test properly.

<!-- Basic deinterlace script
ffmpeg -i interlaced_uncomp.mov \
   -c:v libx264 \
   -preset veryfast \
   -vf 'yadif,format=pix_fmts=yuv420p' \
   access_copy.mp4
 -->
