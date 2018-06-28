# -*- coding: utf-8 -*-
# author: Jared Wilber
"""get_pomological_data.py

This script scrapes the USDA Pomological Watercolors Collection ()
and creates a dataframe with the following columns:
        - `painting_number`: Painting number as enumerated in collection.
        - `fruit`: Name of the primary fruit depicted in the painting.
        - `authors`: Author(s) of the given watercolor painting.
        - `subjects`: Broader classification of fruit(s) depicted in the painting.
        - `year`: Year painting was published.
        - `thumbnail_image`: link to thumbnail jpg of watercolor painting.
        - `image`: link to jpg image of watercolor painting.

Example:
    The function may be called from the cli with or without arguments:

        # call without arguments
        $ python get_pomological_data.py

        # call with arguments
        $ python get_pomological_data.py --start=20 --end=400 --csv_name fruits.csv --verbose 1

    Calling without arguments scrapes all of the watercolor painting data and stores 
    the information to a local csv titled `usda_pomological_watercolors.csv`.

"""

import argparse
import requests

import pandas as pd

from bs4 import BeautifulSoup

IMG_PREFIX = "https://naldc-legacy.nal.usda.gov/"


def get_pomological_data(start=0, end=7564, csv_name='usda_pomological_watercolors.csv', verbose=1):
    """
    Scrape U.S. Department of Agriculture Pomological Water Color Paintings.

    Parameters
    ----------
    start: int
        Image number from which to begin collecting paintings.
    end: int (default=7564)
        Image number for which to stop collecting paintings.
        Note, there are 7584 images total.
    csv_name: str (default='usda_pomological_watercolors.csv')
        Name of file to save dataframe to. Should end with '.csv'.
    verbose: int (default=1)
        If > 0, print scraping progress.

    Returns
    -------
    all_pomo_df: pandas.DataFrame
        DataFrame of all pomological water color paintings with associated info.
        By default, this is saved as to a local csv: 'usda_pomological_watercolors.csv'
    """
    BASE_URL = "https://naldc-legacy.nal.usda.gov/naldc/search.xhtml?start={img_num}&collectionFacet=USDA+Pomological+Watercolor+Collection"

    all_pomo_data = []

    for img_num in range(start, end, 20):

        # parse current page's html
        current_url = BASE_URL.format(img_num=img_num)
        if verbose > 0:
            print("Scraping images {}-{}".format(img_num, img_num + 20))
        page = requests.get(current_url)
        soup = BeautifulSoup(page.content, 'html.parser')

        # get search results for the given url
        search_results = soup.find_all('div', class_='grid_12')

        cells = search_results[0].find_all(class_="document blacklight-pdf")

        # get all relevant info for each painting
        for img in cells:

            # init dict for current image's info
            wc_painting = dict()

            # get name info
            name_info = img.find_all(class_="blacklight-extent_format_facet")[0].text.replace('\n', '').replace('\t', '').split('.')
            try:
                painting_num = name_info[0]
            except:
                painting_num = None
            try:
                fruit = name_info[1]
            except:
                fruit = None

            # get author info
            author_info = img.find_all(class_="blacklight-name_facet")
            try:
                authors = author_info[1].text
            except:
                authors = None

            # get subject info
            subject_info = img.find_all(class_="blacklight-subject")
            try:
                subjects = subject_info[1].text.replace('\n', '').replace('\t', '')
            except:
                subjects = None

            # get year info
            year_info = img.find_all(class_="blacklight-year_facet")
            try:
                year = year_info[1].text.replace('\n', '').replace('\t', '')
            except:
                year = None

            # get image info
            img_link = img.find_all(class_="blacklight-specimen_identifier_s")
            thumbnail_image = IMG_PREFIX + img_link[1].find_all('img')[0]['src'][3:]
            image = thumbnail_image.replace('thumbnail', 'screen')

            # store results
            wc_painting = {
                'painting_index': painting_num,
                'fruit': fruit,
                'authors': authors,
                'subjects': subjects,
                'year': year,
                'image': image,
                'thumbnail_image': thumbnail_image
            }

            # create dataframe from dict
            wc_df = pd.DataFrame(wc_painting, index=[0])

            # store info for current painting
            all_pomo_data.append(wc_df)

    # store all info to single dataframe
    all_pomo_df = pd.concat(all_pomo_data)

    # save results to csv
    all_pomo_df.to_csv(csv_name)

    print("Data successfully saved to {csv}".format(csv=csv_name))


def main(start, end, csv_name, verbose):
    """Run script conditioned on user-input."""
    print("Collecting Pomological Watercolors {s} throught {e}".format(s=start, e=end))
    return get_pomological_data(start=start, end=end, csv_name=csv_name, verbose=verbose)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="Scrape paintings from USDA Pomological Watercolors Collection."
    )
    parser.add_argument('--start', type=int, default=0,
                        help="Image number from which to begin collecting paintings.")
    parser.add_argument('--end', type=int, default=7564,
                        help="Image number for which to end collecting paintings.")
    parser.add_argument('--csv_name', default='usda_pomological_watercolors.csv',
                        help="Name of csv file to save data to.")
    parser.add_argument('--verbose', type=int, default=1, 
                        help="If > 0, print scraping progress..")

    args = vars(parser.parse_args())
    print(args)
    main(**args)
