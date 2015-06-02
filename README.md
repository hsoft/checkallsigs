# checkallsigs.py

Simple script to check all PGP signatures in a HTTP download index.

It is assumed that the URL is that of a simple download index that lists links to files to download.
For each file that also have a ".sig" file, it downloads both files and checks the PGP signature
using gnupg's command line utility.

## Requirements

* Python 3.3+
* [GnuPG][gnupg]

## Usage

You can run the script right off the repo:

    ./checkallsigs.py http://download.example.com

## Why?

Most of us take measures to avoid being compromised, but what if we fail? Someone could exploit
the trust that people have in us and our software and insert malicious code in them stealthily.

To prevent that, we sign our packages, but how can we regularly check that signatures are still
valid? That someone didn't break into our system? With this little script.

[gnupg]: https://www.gnupg.org/

