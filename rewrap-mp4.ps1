# Batch script to rewrap mp4 files to mkv.

$inputfiles = ls *.mp4 # Gets all mp4 files in current folder

foreach ($file in $inputfiles) {
    Write-Host 'Input file is:' $file 
    $output = [io.path]::ChangeExtension($file, '.mkv')
    Write-Host 'Output file will be:' $output
    ffmpeg -i $file -map 0 -c copy $output
}
