# NBNO.py
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This is a Python script for downloading books and other media from the National Library of Norway (NB.no).

### Running in Docker
Bind a local folder to `/data` to access files that are downloaded.  
Arguments mentioned below are added consecutively at the end of, for example, the following:  
`docker run --rm -v /home/nbno/nbno/:/data ghcr.io/lanjelin/nbnopy:latest --id digibok_200709..etc --title --pdf`  

### Running without Docker
To run this code, you need Python 3.7 or newer, pillow, and requests.

Linux and Mac normally come with Python installed.
For Windows, download Python from [python.org](https://www.python.org/downloads/), including 'Add Python 3.xx to PATH'

To check the version of Python, run `python --version`(Windows), `python3 --version`(Mac/Linux), from the command line.

To install pillow and requests, run `python3 -m pip install -r requirements.txt` from the same folder where the downloaded files from here are located.

### Arguments
The only required argument is the ID, which can be found by clicking Refer/Quote and then copying all the text and numbers after no-nb_ e.g., digitidsskrift_202101..etc --> `python3 nbno.py --id digitidsskrift_202101..etc`

The following are supported:
 - Books (digibok)
 - Newspapers (digavis)
 - Pictures (digifoto)
 - Periodicals (digitidsskrift)
 - Maps (digikart)
 - Letters and Manuscripts (digimanus)
 - Notes (digibok)
 - Music Manuscripts (digimanus)
 - Posters (digifoto)
 - Program Report (digiprogramrapport)

```
use: nbno.py [-h] [--id <ID>] [--cover] [--pdf] [--f2pdf] [--url] [--error]
              [--v] [--resize <int>] [--start <int>] [--stop <int>]

required argument:
  --id <ID>    The ID of the content to be downloaded

optional arguments:
  -h, --help      show this help message and exit
  --cover         Set to download covers
  --title         Set to automatically fetch the title of the book
  --pdf           Set to create a PDF of the images downloaded
  --f2pdf         Set to create a PDF of images in an existing folder
  --url           Set to print the URL of each part
  --error         Set to print HTTP error codes
  --v             Set to print more info
  --resize <int>  Percentage of original image size
  --start <int>   Page number to start from
  --stop <int>    Page number to stop at
```