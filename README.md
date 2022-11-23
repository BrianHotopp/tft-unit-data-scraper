# tft-unit-data-scraper
Scrape mobalytics champion cheat sheet for champion/trait data.
To use:
- clone the repository and call the script:
```
usage: main.py [-h] [--raw-data-dir RAW_DATA_DIR] output_dir

scrapes data from the mobafire champions cheat sheet and outputs it to the specified directory

positional arguments:
  output_dir            the directory to output the data to

options:
  -h, --help            show this help message and exit
  --raw-data-dir RAW_DATA_DIR
                        the directory to save the raw data to
```
The script outputs two files:
- `champions.json` - a list of champions with various data about them (traits, cost, attack damage, health, etc.)
- `traits.json` - a list of traits and their breakpoints
See [here](./examples/champs_1669231606.json) for an example of the champions file output.
See [here](./examples/traits_1669231606.json) for an example of the traits file output.

