# It's a work in progress :)

## How to
There are two "modes": Downloading a folder, and downloading all images matching a search term in an artist's gallery

### Folder
Fill `ids.txt` with FA album URLs. Example: http://www.furaffinity.net/gallery/spirale/folder/9862/Lucky-and-Chocolate-Charms.

One album per line.

To run the script: `python main.py album`

### Search in gallery
This will download any image with a title containing a search term.

Fill `ids.txt` with the following: `<artistname> <search term>`. Example: `ruaidri A Helping Hand`.

There has to be a space between the two. There may be spaces in the search term.

One artist+search term per line.
