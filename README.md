# Vime
Visual Model Evaluation

## Dependencies
- numpy
- pandas
- matplotlib
- seaborn

## Usage in 2 Steps
Step1: Convert the fomat of raw data into sample data (e.g. win_rata/data/exp1.txt). Note that only three components are required: `Left Model`, `Right Model`, `Win Rate`.

Step2: Run `txt_to_fig.py` to get the heatmap visualization, and run `txt_to_csv.py` to get the tabular visualization (do not fotget to change the path).

## Components
### Win Rate
- **check**: It will compute the win rate automatically according to the data in contraposition if the data is missing.

- **model_sort**: Sort the models name alphabetically.

- **vector**: Whether save the vectorgraph.

## Todo
- Primary v.s. All visulization
- One model with time passing
- Diversity in dirrerent models visulization
- ...