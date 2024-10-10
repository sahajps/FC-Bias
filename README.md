# _**Independent fact-checking organizations exhibit a departure from political neutrality**_
Welcome to the project page for our paper. This page serves as a user guide for the reproducibility of results and contains the fact-checking data from shortlisted independent fact-checking organizations.

## 🌟 What's New
🗓 Dynamic polarity score (PS) plot project: [Dyanmic-Plot-FC-Bias](https://github.com/sahajps/Dyanmic-Plot-FC-Bias)

## 📂 Directory Structure

| **File/Folder**                   | **Description & Work-flow**                                                                                             |
|-------------------------------------|-------------------------------------------------------------------------------------------------------------|
| 📂 **Scrapped Data**                | Python scripts to scrape data and store in the `Scrapped Data/data` folder.                                 |
| 📂 **Cleaned Data**                 | Run notebooks `Preprocessing_USA.ipynb` and `Preprocessing_IN.ipynb` to get the preprocessed data into the `Cleaned Data` folder. |
| 📂 **RQ1/Claim Norm Data**       | Run `RQ1/Claim_Norm_Prompt_ChatGPT.py` and `RQ1/Claim_Norm_Prompt_ChatGPT_5W.py` to return the Claim and What-Why sentences from the fact-check articles. |
| 📂 **RQ1/Cosine Scores**             | Running `RQ1/Embeddings_Calc.py`, `RQ1/Parallel_Pairing.py`, and `RQ1/Cosine_Sim_Calc.py` in order returns the cosine similarity of the inter-organization articles published within a 15-day window. |
| 📂 **RQ2/Entity Sentiment Data**     | `RQ2/Entity_Image_ChatGPT.py` extracts entities and their populated image (positive, negative, or neutral) in this folder. |
| 📂 **RQ2/Top Entity**               | `RQ2/Top_Entity.ipynb` enlists the top 100 entities per organization. Then these entities are labeled if these are political or not. This annotation is done manually. |
| 📄 **RQ2/Org_Wise.ipynb**       | Prints the overall polarity (all political entities and dates) of organizations.                         |
| 📂 **RQ2/Graph Data**               | For each organization, `RQ2/Entity_Wise.ipynb` first finds the top 5 entities and returns PS data for all years and year-wise to plot the graph. |
| 📂 **RQ1/Entity Intersection**       | Contains entity mention data within the 15-day windows generated using the `RQ1/Entity_Coverage.py` script.    |
| 📊 **Graphs**                       | Contains the `*.ipynb` files to generate and save them into the same folder.                                   |
| 📂 **Human Evaluation**                    | Contains `Human_Annotation_Data.xlsx` file, which is evaluated by human annotators, and `Human Evaluation/HE_Scores.ipynb` shows the results of human evaluation. |

## Dataset

### Scrapped Data
This is row data scrapped directly from the oragnization's webpages. The data is stored as .xlsx file format in folder the said, each entry has the following format:

```bash
"links": link to news article
"date": date of publication
"title": title of the article
"text": detailed article
```

Note #1: The list of URLs reflects the pages available at the time of scraping. You might need to update this list if you scrape data again in the future.

Note #2: Organizations may change their website layouts from time to time. If this happens, you may need to update the scraper code accordingly.

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

If you find this project useful, please cite it using the following bibtex: 

```sh
@article{singh2024independent,
  title={Independent fact-checking organizations exhibit a departure from political neutrality},
  author={Singh, Sahajpreet and Masud, Sarah and Chakraborty, Tanmoy},
  journal={arXiv preprint arXiv:2407.19498},
  year={2024}
}
```
