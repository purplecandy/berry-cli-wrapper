# Berry CLI - Wrapper

It's probably most stupid python program but it's my first so it deserves some recognition

# COMMANDS & GUIDE

There is no actual guide you just type the commands and wait for the results to load

### search [string] --limit

_if the passed string is 'prev' it will search the previous result but with next page_
This command is used to search movies
Example: search The lord of the rings
Options:
--limit=int
[By default the search will show 10 results, if limit=15 it will show 15 instead of 10]
\*make sure there is no space at the end
Example: search The lord of the rings--limit=10## Switch to another file

All your files are listed in the file explorer. You can switch from one to another by clicking a file in the list.

### movieinfo [int]

This command will give you the complete information about the movie such as Title,Release Year,Description,Genre,Torrents,Cast etc
Example: movieinfo 9540

- The id only accepts numbers
- The id can be used to download movies torrents

### download [int]

Download command let's you download torrents
Example: download 7540

- The id only accepts numbers, if you don't have the id please search the movie first, obtain the id and then search for download with the id

### help [command]

Anyways the help command is included if you ran into something......you probably won't everything is inside a try/except block.
