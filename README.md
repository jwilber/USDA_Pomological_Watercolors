# USDA_Pomological_Watercolors

This repo stores data from the [USDA Pomologogical Watercolor Collection](https://usdawatercolors.nal.usda.gov/pom/home.xhtml).

![Collage of watercolor paintings](https://www.garrickadenbuie.com/images/project/ggpomological/pom-examples.jpg)

The following information is provided:

## data/images/*

Image directory containing a `.jpg` for each individual painting.
There are 7584 paintings in total.


## data/usda_pomological_watercolors.csv

| Column | Description | Data Type |
|---|---|---|
| `painting_number` | Painting number as enumerated in collection. | number |
| `fruit` | Pomological name of the primary fruit depicted in the painting..| number |
| `authors` |  Author(s) of the given watercolor painting. | text |
| `subjects` | Broader classification of fruit(s) depicted in the painting. (e.g. 'apple') | text |
| `year` | Year painting was published. | number |
| `thumbnail_image` | Link to thumbnail jpg of watercolor painting. | text |
| `image` | Link to jpg image of watercolor painting. | text |

## scripts/get_pomological_data.py

Python script used to scrape the data from [usda](https://naldc-legacy.nal.usda.gov/naldc/search.xhtml?start=0&collectionFacet=USDA+Pomological+Watercolor+Collection)

Example:

```
# call without arguments
$ python get_pomological_data.py

# call with arguments
$ python get_pomological_data.py --start=20 --end=400 --csv_name fruits.csv --verbose 1
```

Calling without arguments scrapes all of the watercolor painting data and stores 
the information to a local csv titled `usda_pomological_watercolors.csv`.
