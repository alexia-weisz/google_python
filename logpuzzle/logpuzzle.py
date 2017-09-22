#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""
def sort_url(url):
    match = re.search(r'-\w+-(\w+)\.\w+', url)
    if match:
        return match.group(1)
    else:
        return url

def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""
    # +++your code here+++
    with open(filename, 'r') as f:
        server_name = filename.split('_')[-1]
        start_url = 'http://{}'.format(server_name)
        all = f.read()
        match = re.findall(r'"GET (\S+puzzle\S+)', all)
        url_dict = {}
        if match:
            for m in match:
                url_dict[start_url + m] = 1
            match = sorted(url_dict.keys(), key=sort_url)
            duplicates = []
            for i in range(1, len(match)):
                if match[i] == match[i-1]:
                    duplicates.append(match[i])
            for duplicate in duplicates:
                match.remove(duplicate)
        else:
            print('No matches found.')
    return match

def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """
    # +++your code here+++
    # create directory if it doesn't exist
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # create index.html file
    newfile = os.path.join(dest_dir, 'index.html')
    with open(newfile, 'w') as f:
        f.write('<verbatim>\n')
        f.write('<html>\n')
        f.write('<body>\n')

        for i, im_url in enumerate(img_urls):
            newfile = 'img{}'.format(str(i).zfill(len(str(len(img_urls)))))
            print('Retreiving ', im_url)
            urllib.urlretrieve(im_url, os.path.join(dest_dir, newfile)) #download images to newfile
            html_line = '<img src="{}">'.format(newfile) 
            f.write(html_line) # write new image name into html file
        f.write('\n')
        f.write('</body>\n')
        f.write('</html>\n')

def main():
    args = sys.argv[1:]

    if not args:
        print 'usage: [--todir dir] logfile '
        sys.exit(1)

    todir = ''
    if args[0] == '--todir':
        todir = args[1]
        del args[0:2]

    img_urls = read_urls(args[0])

    if todir:
        download_images(img_urls, todir)
    else:
        print '\n'.join(img_urls)

if __name__ == '__main__':
    main()
