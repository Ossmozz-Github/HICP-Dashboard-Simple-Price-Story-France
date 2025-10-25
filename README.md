# 💶 HICP Dashboard — France (Simple Price Story)

**Scope:** 🇫🇷 France · Monthly · Not seasonally adjusted (HICP/IPCH) · One national series (no `geo` column)

## Narrative question (plain words)
**What really happened to prices in France over time, and which everyday categories pushed them up or down?**  
We want to (1) find the **peak** and the **current level**, (2) see which **categories** (CP01..CP12) sit **above/below** the headline (CP00),  
(3) check which categories are **volatile** or **stable**, and (4) see if **seasonality changed after 2020**.

## What the app shows
- **0_Data_Quality** — columns, types, missing values, duplicates, date coverage  
- **1_Introduction** — our problem (why this study) + quick data facts for France  
- **2_Overview** — headline CP00 (year-over-year %, month-over-month %) with KPIs and date filter (sidebar)  
- **3_Categories** — compare selected categories (CP01..CP12) to the headline; labels shown (no CP codes in UI)  
- **4_Volatility** — which categories move the most (volatility) and how persistent they are  
- **5_Seasonality** — average MoM before 2020 vs after 2020, month by month  
- **6_Conclusions** — stitched summary that answers the narrative question for France

## Quick start
```bash
python -m venv venv
# macOS/Linux
source venv/bin/activate
# Windows
venv\Scripts\activate

pip install -r requirements.txt
streamlit run app.py
````

## Link of the dataset
    
https://www.data.gouv.fr/datasets/indice-des-prix-a-la-consommation-harmonises-mensuels/