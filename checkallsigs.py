#!/usr/bin/env python3
"""Simple script to check all PGP signatures in a HTTP download index.

Usage: checkallsigs.py http://download.example.com

It is assumed that the URL is that of a simple download index that lists links to files to download.
For each file that also have a ".sig" file, it downloads both files and checks the PGP signature
using gnupg's command line utility.
"""

from urllib.request import urlopen, urlretrieve
import argparse
import re
import subprocess
from tempfile import TemporaryDirectory
import os.path as op

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'url',
        help="URL of a download index where we check all PGP signatures"
    )
    return parser

def main(argv=None):
    args = get_parser().parse_args(argv)
    url = args.url
    if not url.endswith('/'):
        url += '/'
    contents = urlopen(args.url).read()
    # The [^.] is to avoid getting the ".." entry. so, nothing starting with a dot.
    hrefs = re.findall(br"href=\"([^.][^\"]+)\"", contents)
    filenames = sorted([b.decode() for b in hrefs])
    tocheck = []
    nosigcount = 0
    for fn, fnnext in zip(filenames, filenames[1:] + ['']):
        if fnnext == "%s.sig" % fn:
            tocheck.append((fn, fnnext))
        else:
            nosigcount += 1
    print("%d files without signatures" % nosigcount)
    for fn, sig in tocheck:
        print("Checking %s with %s. Downloading..." % (fn, sig))
        with TemporaryDirectory() as tmpdir:
            fnpath = op.join(tmpdir, fn)
            sigpath = op.join(tmpdir, sig)
            urlretrieve(url + fn, fnpath)
            urlretrieve(url + sig, sigpath)
            result = subprocess.call(['gpg', '--verify', sigpath])
            if result != 0:
                print("WARNING! WARNING! Signatures not matching for %s!" % sig)
                break
            else:
                print("OK")


if __name__ == '__main__':
    main()

