import tempfile
from scraper import scrape_page
from pathlib import Path
import shutil
import os
import argparse
if __name__ == '__main__':
    """
    This script scrapes data from the mobafire champions cheat sheet and outputs it to the specified output directory.
    """
    parser = argparse.ArgumentParser(description='scrapes data from the mobafire champions cheat sheet and outputs it to the specified directory') 
    # the directory to save the raw data to -- if none is provided, the raw html data will not be saved
    parser.add_argument('--raw-data-dir', type=str, help='the directory to save the raw data to; if none is provided defaults to the OS temp directory')
    parser.add_argument('output_dir', type=str, help='the directory to output the data to')
    args = parser.parse_args()
    url = "https://www.mobafire.com/teamfight-tactics/champions"
    # if provided, the raw data dir must exist
    if args.raw_data_dir is not None:
        if not os.path.isdir(args.raw_data_dir):
            raise Exception("The raw data directory does not exist")
    else:
        # if not provided, create a temp dir
        args.raw_data_dir = tempfile.mkdtemp()
    # the output directory must exist
    if not os.path.isdir(args.output_dir):
        raise Exception("The output directory does not exist")
    raw_save_folder = Path(args.raw_data_dir) 
    cleaned_save_folder = Path(args.output_dir)
    # scrape the data
    raw_html_path, champs_path, traits_path = scrape_page(url, raw_save_folder, cleaned_save_folder)
    print(f"Successfully scraped {url}")
    if args.raw_data_dir:
        print(f"Saved raw data to {raw_html_path}")
    print(f"Saved champs data to {champs_path}")
    print(f"Saved traits data to {traits_path}")

