# It's a work in progress!
(.. ish. It works now, but could be improved)

## How to
First, in "a" and "b" cookies in `config.json`. How to find them:
1. Log into fa.net
2. Open the console / inspect window
3. Find the fa.net cookies. Usually this is in the "Application" tab
4. Copy the `a` and `b` cookie values into config.json

There are two "modes": Downloading an actual folder, and downloading all images matching a search term in an artist's gallery

### Folder
Fill `ids.txt` with FA album URLs.

One album per line.

To run the script: `python main.py album`

### Search in gallery
Most artists don't put their comics in a folder, they just name them ComicName page X/Y. For downloading these comics, this mode can be used. This will download any image with a title containing a search term in an artist's gallery.

Fill `ids.txt` with the following: `<artistname> <search term>`. Example: `ruaidri A Helping Hand`.

There has to be a space between the two. There may be spaces in the search term.

One artist+search term per line.

To run the script: `python main.py search`
