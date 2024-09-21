"""

------------------------------------------------------------

C\bCH\bHA\bAN\bNG\bGE\bEL\bLO\bOG\bG
\tVersion 5.6.12


D\bDE\bES\bSC\bCR\bRI\bIP\bPT\bTI\bIO\bON\bN
\tThis update introduces the following changes:
\t\t1. Reformat code and organize imports

\tDetails:
\t\t- Reformatted code to be more readable and removed unused imports.


\tFor more details, visit the wiki: https://script-ware.gitbook.io

------------------------------------------------------------

C\bCH\bHA\bAN\bNG\bGE\bEL\bLO\bOG\bG
\tVersion 5.6.11


D\bDE\bES\bSC\bCR\bRI\bIP\bPT\bTI\bIO\bON\bN
\tThis update introduces the following changes:
\t\t1. Detect and raise an error for private gofile folders

\tDetails:
\t\t- Private gofile folders will now raise an error when attempting to download them instead of crashing CDL


\tFor more details, visit the wiki: https://script-ware.gitbook.io

------------------------------------------------------------

C\bCH\bHA\bAN\bNG\bGE\bEL\bLO\bOG\bG
\tVersion 5.6.1


D\bDE\bES\bSC\bCR\bRI\bIP\bPT\bTI\bIO\bON\bN
\tThis update introduces the following changes:
\t\t1. Fixes issue with --sort-all-downloads
\t\t2. Improves sort status visibility

\tDetails:
\t\t- The sort status is now display under hash, along with other statuses
\t\t- --sort-all-downloads is disabled by default, thus only cdl downloads are sorted without the flag
\t\t- The sort_folder can not be the same as the scan_dir


\tFor more details, visit the wiki: https://script-ware.gitbook.io

------------------------------------------------------------

C\bCH\bHA\bAN\bNG\bGE\bEL\bLO\bOG\bG
\tVersion 5.6.0


D\bDE\bES\bSC\bCR\bRI\bIP\bPT\bTI\bIO\bON\bN
\tThis update introduces the following changes:
\t\t1. Updated the sorting progress UI to display more information.
\t\t2. Removed unused functions from progress bars.

\tDetails:
\t\t- The sorting UI now displays the progress of each folder as it is being processed, including the number of files that have been sorted and the percentage of the folder that has been processed.
\t\t- The sorting UI now also shows what folders are in the queue to be sorted.


\tFor more details, visit the wiki: https://script-ware.gitbook.io

------------------------------------------------------------

C\bCH\bHA\bAN\bNG\bGE\bEL\bLO\bOG\bG
\tVersion 5.5.1

D\bDE\bES\bSC\bCR\bRI\bIP\bPT\bTI\bIO\bON\bN
\tThis update introduces the following changes:
\t\t1. small fixes for sorting system



\tDetails:
\t\t- use - instead of _ for new arguments
\t\t- fix bug where purge_dir is called for each file, instead of each directory when done


\tFor more details, visit the wiki: https://script-ware.gitbook.io

------------------------------------------------------------

C\bCH\bHA\bAN\bNG\bGE\bEL\bLO\bOG\bG
\tVersion 5.5.0

D\bDE\bES\bSC\bCR\bRI\bIP\bPT\bTI\bIO\bON\bN
\tThis update introduces the following changes:
\t\t1. Finalizes new sorting feature
\t\t2. add scanning directory for sorting
\t\t3. adds progress bar for sorting



\tDetails:
\t\t- skips need to scan db if sort_cdl_only is false
\t\t- progress bar for current progress of sorting files,incremented for each folder
\t\t- allow for setting a different folder to scan that is independent of the download folder

\tFor more details, visit the wiki: https://script-ware.gitbook.io

------------------------------------------------------------

"""
