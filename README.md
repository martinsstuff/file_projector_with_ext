# About the Program:

**Warning:** The program will irrecoverably delete any item in the target_directory which isn't also present in the source_directory. I have only done very limited testing on the program, I can't guarantee that there might not be a bug where a folder path is interpreted incorrectly!

**The program was developed for personal use, I take no responsibility for anything going wrong.**

---

"Projects" files and directories from one directory to another. It does so by copying and removing files in accordance with the source directory.

It also appends an extension to all files. Wonder what that could be useful for?

I wrote the program because Windows' file symlinks didn't work for what I wanted to do. I suspect that it would've been much easier on \*nix, at least the script wouldn't need to do all the file monitoring stuff and could just set up symlinks.

Configuration is currently done in the script itself. Change the folders and extension before usage.

Info:
- Compares file contents using MD5 (because blake3 isn't in the standard library) ONLY on the initial sync.
- Has a monitoring function that does stuff based on file modification dates.
- Monitoring function is kinda sketchy, but I made it wait 5 seconds and do a full resync on error.
- The monitor also makes sure the last modification date is >2 seconds to avoid copying files being actively modified.
