import os
import sys

import recoders as r
import argparse



parser = argparse.ArgumentParser()
parser.add_argument("src", help="Source directory")
parser.add_argument("dst", help="Converted files directory")
parser.add_argument("phase", help="phase1(locate)|phase2(convert)|phase3(map metadata)|phase4(overwrite)")
parser.add_argument("--perform", action="store_true",
                    help="does actual changes")

args = parser.parse_args()

srcdir = os.path.abspath(args.src)
dstdir = os.path.abspath(args.dst)


if args.phase == "phase1":
    for (srcfile, c, b) in r.find_files_to_convert_based_on_encoder(srcdir):
        print(os.path.relpath(srcfile, srcdir).replace("\\", "/"))
elif args.phase == "phase2":
    for file in sys.stdin:
        f = file.strip()
        filenames = f.split('\t')
        srcfile = os.path.abspath(os.path.join(srcdir, filenames[0]))
        dstfile = os.path.abspath(os.path.join(dstdir, filenames[-1]))
        if args.perform:
            os.makedirs(os.path.dirname(dstfile), exist_ok=True)
        r.recode_file(srcfile, dstfile, not args.perform)
elif args.phase == "phase3":
    for file in sys.stdin:
        f = file.strip()
        srcfile = os.path.abspath(os.path.join(srcdir, f))
        dstfile = os.path.abspath(os.path.join(dstdir, f))
        r.map_metadata(srcfile, dstfile, not args.perform)
elif args.phase == "phase4":
    for file in sys.stdin:
        f = file.strip()
        srcfile = os.path.abspath(os.path.join(srcdir, f))
        dstfile = os.path.abspath(os.path.join(dstdir, f))
        r.commit_changes(srcfile, dstfile, not args.perform)

