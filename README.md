# _**Independent fact-checking organizations exhibit a departure from political neutrality**_
Welcome to the project page for our paper. This page serves as a user guide for the reproducibility of results and contains the fact-checking data from shortlisted independent fact-checking organizations.

## 🌟 What's New
🗓 [2024.06.28] Required python modules' versions to be updated soon 🔜
🗓 [2024.06.21] The project page has been built!

## 📂 Directory Structure

| **File/Folder**                   | **Description & Work-flow**                                                                                             |
|-------------------------------------|-------------------------------------------------------------------------------------------------------------|
| 📂 **Scrapped Data**                | Python scripts to scrape data and store in the `Scrapped Data/data` folder.                                 |
| 📂 **Cleaned Data**                 | Run notebooks `preprocessing_USA.ipynb` and `preprocessing_IN.ipynb` to get the preprocessed data into the `Cleaned Data` folder. |
| 📂 **RQ1/Claim_Norm_chatgpt**       | Run `RQ1/Claim_Norm_Prompt_ChatGPT.py` and `RQ1/Claim_Norm_Prompt_ChatGPT_5W.py` to return the Claim and What-Why sentences from the fact-check articles. |
| 📂 **RQ1/CosineScores**             | Running `RQ1/embed_all.py`, `RQ1/parallel_all_test.py`, and `RQ1/all_gen_cosine_new.py` in order returns the cosine similarity of the inter-organization articles published within a 15-day window. |
| 📂 **RQ2/Topic Sentiment Data**     | `RQ2/Entity_Image_ChatGPT.py` extracts entities and their populated image (positive, negative, or neutral) in this folder. |
| 📂 **RQ2/Top Topics**               | Enlists the top 100 entities with the label if these are political or not. This annotation is done manually. |
| 📄 **RQ2/RQ2_Org_Wise.ipynb**       | Returns the overall polarity (all political entities and dates) of organizations.                         |
| 📂 **RQ2/Graph Data**               | For each organization, `RQ2/Topic_Wise.ipynb` first finds the top 5 entities and returns PS data for all years and year-wise to plot the graph. |
| 📂 **RQ1/EntityIntersection**       | Contains entity mention data within the 15-day windows generated using the `RQ1/EntityCoverage.py` script.    |
| 📊 **Graphs**                       | Contains the .ipynb files to generate and save them into the same folder.                                   |
| 📂 **HumanEval**                    | Contains `Human_Annotation_Data.xlsx` file, which is evaluated by human annotators, and `HumanEval/HE_Scores.ipynb` shows the results of human evaluation. |
| 📜 **LICENSE**                      | MIT License Copyright (c) 2024 Singh et al.                                                                 |
| 📄 **README.md**                    | This must ring a bell.                                                                                       |


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

```
