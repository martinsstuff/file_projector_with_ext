# file_projector_with_ext
"Projects" files and directories from one directory to another. It does so by copying and removing files in accordance with the source directory.

It also appends an extension to all files. Wonder what that could be useful for?

\*I wrote the program to work on Windows because symlinks for files suck there. Would be 10000 times easier on \*nix, just a tiny shell script probably.

Configuration is currently done in the script itself. Change the folders and extension before usage.

Info:
- Compares file contents using MD5 (because blake3 isn't in the standard library) ONLY on the initial sync.
- Has a monitoring function that does stuff based on file modification dates.
- Monitoring function is kinda sketchy, but I made it wait 5 seconds and do a full resync on error.
- The monitor also makes sure the last modification date is >2 seconds to avoid copying files being actively modified to.

Some cleanup and testing still necessary :)
