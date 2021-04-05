A collection of trial and error generated spells for tools. Generally - nothing to see here ;)

Updating file modified dates by metadata's create date with exiftool:
```
exiftool "-FileModifyDate<CreateDate"
```

Trial& error - isolated working ffmpeg spells
```
ffmpeg -y -i src -movflags use_metadata_tags -map 0 -c:v libx264 -crf 21 -c:a copy -copy_unknown -map_metadata 0 dest
ffmpeg -y -i src -movflags use_metadata_tags -map 0 -c copy -copy_unknown -c:v libx264 -crf 21
```

Hardware encoder attempt
```
ffmpeg -i src -movflags use_metadata_tags -map 0 -c copy -copy_unknown -c:v hevc_qsv -vf "transpose=dir=2" -preset fast -global_quality 25 dest
```
