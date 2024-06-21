# Quantifying Political Neutrality in Independent Fact-Checking Beyond the Left-Right Spectrum
This project page is for our said paper, the page represents a user-guide for reproducibilty of results and contains the fact-checking data from shortlished independent fact-checking organizations.

## What's New

[2024.06.21] The project page has been built!

## WorkfLow

#### Step 1: Run .py files given in the Scrapped Data folder to scrap the fact-checking data directly from the offcial websites of independent fact-checking organizations
```bash
python3 <python_file_name>
```
#### Step 2: Run notebooks named preprocessing_USA.ipynb and preprocessing_IN.ipynb to get the preprocessed into Cleaned Data folder


## Dataset

### Scrapped Data
This is row data scrapped directly from the oragnization's webpages. The data is stored as .xlsx file format in folder the said, each entry has the following format:

```bash
"links": link to news article
"date": date of publication
"title": title of the article
"text": detailed article
```

### Cleaned Data
Cleaned data contains same data as Scrapped Data with basic text preprocessing and conversion of date to day, month and year.

```bash
"links": link to news article
"date_year": year of publication
"date_month": month of publication
"date_day": day of publication
"title": title of the article
"text": detailed article
```

## Citation

If you find this project useful, please cite it using the following format: 

```bash
@inproceedings{,
  author       = {},
  title        = {},
  booktitle    = {},
  pages        = {},
  publisher    = {},
  year         = {},
  url          = {}
}

```
