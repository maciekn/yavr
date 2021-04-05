import shutil
import subprocess
import json
import recodetools as rt


# exiftool "-FileModifyDate<CreateDate"


def _os_call(args, dry_run):
    if dry_run:
        print("Calling " + " ".join(args))
    else:
        retval = subprocess.call(args)
        if retval != 0:
            raise Exception("Cannot call " + args)


def _os_call_output(args, dry_run):
    if dry_run:
        print("Calling " + " ".join(args))
    else:
        return subprocess.check_output(args).decode()


def map_metadata(src, dest, dry_run):
    rewrite_exif_args = [rt.get_exiftool(), '-overwrite_original_in_place', "-ee", '-tagsfromfile', src, "-all:all", "-FileModifyDate<CreateDate", dest]
    _os_call(rewrite_exif_args, dry_run)
#    _os_call([rt.get_touch(), '-r', src, dest], dry_run)

# -y -i src -movflags use_metadata_tags -map 0 -c:v libx264 -crf 21 -c:a copy -copy_unknown -map_metadata 0 dest
# -y -i src -movflags use_metadata_tags -map 0 -c copy -copy_unknown -c:v libx264 -crf 21

#Hardware encoder
# ffmpeg -i src -movflags use_metadata_tags -map 0 -c copy -copy_unknown -c:v hevc_qsv -vf "transpose=dir=2" -preset fast -global_quality 25 dest
def recode_file(src, dest, dry_run=True):
    args = [rt.get_ffmpeg(), '-y', '-i', src, '-movflags', 'use_metadata_tags', '-map', '0',
             '-c', 'copy', '-copy_unknown',
            '-c:v', 'libx265', '-crf', '28',
            dest]
    _os_call(args, dry_run)


def commit_changes(src, dest, dry_run=True):
    print("Moving {} to {}".format(dest, src))
    if not dry_run:
        shutil.move(dest, src)


def trim_file(directory, outdir, file, entry, finish, dry_run=True):
    src = directory + file
    dest = outdir + file
    # ffmpeg -i video.mp4 -ss 00:01:00 -to 00:02:00 -c copy cut.mp4

    args = [rt.get_exiftool(), '-y', '-i', src, '-ss', entry]
    if finish is not None:
        args.extend(['-to', finish])
    args.extend(['-c', 'copy', '-copy_unknown', '-map_metadata', '0', dest])

    _os_call(args, dry_run)
    # _map_metadata(dest, src, dry_run)


def should_recode_file(file):
    if 'AvgBitrate' not in file or 'Mbps' not in file['AvgBitrate']:
        return None
    bitrate = float(file['AvgBitrate'].split(' ')[0])
    if bitrate < 10:
        return None
    compressor = None
    if 'CompressorName' in file:
        compressor = file['CompressorName']
    elif 'Encoder' in file:
        compressor = file['Encoder']

    if compressor:
        if 'Lavc' in compressor:
            return None
        if 'Lavf' in compressor:
            return None

    return file['SourceFile'], compressor, bitrate


def find_files_to_convert_based_on_encoder(dest):
    args = [rt.get_exiftool(), '-compressorname', '-AvgBitrate', '-encoder', '-s',  # give tag name
            # '-f',  # force tag, even if not existing
            '-j',  # json out
            '-i', '@eaDir',  # ignore dir
            '-ext', 'mov', '-ext', 'mp4', '-ext', 'mts',
            '-r',  # recursive
            dest]
    retval = _os_call_output(args, False)
    out = json.loads(retval)
    filtered = [should_recode_file(f) for f in out]
    return [f for f in filtered if f]
