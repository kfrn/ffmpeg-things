### ffmpeg-things

Various ffmpeg scripts and notes. Here you can find:

* [access_copy](./access_copy.md): scripts that produce access derivative files with the specs given by several institutions.
* [deinterlacing](./deinterlacing.md): a superficial look at the different ffmpeg deinterlacers.
* [inverse_telecine.md](./inverse_telecine.md): how to use ffmpeg to IVTC a file, including bash script. (Added to [ffmprovisr](https://amiaopensource.github.io/ffmprovisr/#inverse-telecine))
* [inverse_telecine.py](./inverse_telecine.py): springing off the above, this is a Python script that takes in a single file (or folder of .VOBs) and applies IVTC (+ concats, if necessary).
   * Yea, you can do it in Bash easily, I just felt like writing some Python.
   * Run using `python3 inverse_telecine.py <input>`
* [rewrap-mp4](./rewrap-mp4.ps1): a basic PowerShell script for batch processing using ffmpeg. (Added to [ffmprovisr](https://amiaopensource.github.io/ffmprovisr/#batch_processing_win)).
