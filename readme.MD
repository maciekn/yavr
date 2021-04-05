# Yet Another Video Recoder

A handmade script to deal with large-scale videos recoding commonly sourced from common cameras these days (mobile phones).
Mobile phones are quite generous when comes to video bandwith which effects in huge (though great in quality) video files. 

Idea behind YAVR is to :
- recode videos
- maintain their high quality 
- save storage size 
- **preserve** as much metadata as it is possible.

Tools I have found usually were quite weak in meeting all above points so I had to wrote my own.

## Requirements

YAVR to function properly required following applications to be achievable on the path:
- python3 (runtime environment)
- ffmpeg (recoding)
- exiftool (metadata handling)
- touch file attributes handling


## How does it work?
Well, no rocket science here. The tool uses widely available apps to recode files. The process is splitted into separate phases. This allows to execute them on different environments.
For example, it enables to isolate files to recode on one machine and then do the actual recoding on the other (for instance more powerful and headless) machine.

All steps may not include `--perform` switch to enable dry-run mode.

Example full execution:
```
python recode.py --perform /source/location /recoded/location phase1 > phase1.txt
python recode.py --perform /source/location /recoded/location phase2 < phase1.txt
python recode.py --perform /source/location /recoded/location phase3 < phase1.txt
python recode.py --perform /source/location /recoded/location phase4 < phase1.txt
```


### Phase 1 - scanning
The first phase scans provided source directory (recursively) looking for movies requiring recoding. 
As outcome, it produces a list of files which needs to be later provided for later phases as the point of reference.
The qualifying factor list is evolving, hovewer currently it looks for:
- files with average bitrate above 10Mbps
- not encoded by `Lavc` or `Lavc` (which means they were already recoded)

### Phase 2 - recoding
This is the most time-consuming part: file recoding. The list from phase 1 is used to recode videos from source to destination location.

### Phase 3 - metadata mapping
This phase maps copies over metadata from source files into recoded copies

### Phase 3.5 - verification
While there's no automated verification (though it would be nice) it is advised to check manually whether operation was successful as **the next step will be abrasive!**

### Phase 4 - overwrite
Overwrites source files with recoded copies. As simple as this. As so destructive!