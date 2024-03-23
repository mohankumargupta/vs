import os
import requests
from pathlib import Path
from zipfile import ZipFile
import sys
from tempfile import TemporaryFile, TemporaryDirectory
from iterfzf import iterfzf
import subprocess


VSCODE_URL = "https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-archive"
#OUTPUT_FOLDER = "vscode-php`"

def download_file(url: str, output_file: Path):
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        if r.status_code != 200:
            pass
        r.raise_for_status()
        #with open(output_file, 'wb') as f:
        with output_file.open('wb') as f:
            for chunk in r.iter_content(chunk_size=4096): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)

def mkdir(dirname):
    Path(dirname).mkdir(parents=True, exist_ok=False)

def unzip(filename: Path, dirname: Path):
    with ZipFile(filename) as f:
        f.extractall(dirname)

def makeDataDirectories(dirname):
    datadir = Path(dirname).joinpath("data")
    tmpdir = datadir.joinpath("tmp")
    mkdir(datadir)
    mkdir(tmpdir)

def downloadsDirectory():
    homedirectory = Path.home()
    downloads = homedirectory.joinpath("Downloads")
    return downloads

def fzf_dict(d, multi):
    r"""This assumes keys must have no tabs, hence ``'\t'`` as a separator."""
    options = ('{0}\t{1}'.format(k, v) for k, v in d.items())
    for kv in iterfzf(options, multi=multi):
        yield kv[:kv.index('\t')]

def find_vscode_subdirectories(directory):
    vscode_subdirectories = []
    for item in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, item)) and item.startswith("vscode-"):
            vscode_subdirectories.append(item[len("vscode-"):])
    return vscode_subdirectories


def main():

    #my_data = ["apple", "banana", "cherry", "date"]
    #my_data.reverse()
    #selected_item = iterfzf(my_data)
    
    downloads = downloadsDirectory()
    #print(downloads)
    options = find_vscode_subdirectories(downloads)
    options.reverse()
    #print(options)
    selected_item = iterfzf(options, __extra__=["--exact"])
    print(f"Selected item: {selected_item}")
    vscode_binary = downloads.joinpath(f"vscode-{selected_item}").joinpath("Code.exe")
    print(vscode_binary)
    subprocess.Popen([vscode_binary])
    sys.exit(0)    
    