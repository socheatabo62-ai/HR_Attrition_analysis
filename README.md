# HR Attrition Dashboard

A Streamlit dashboard that shows which employees may resign, and why.
Data: IBM HR Analytics Employee Attrition & Performance (1,470 employees).
Model: Random Forest, scored with 5-fold cross-validation.

## Folder structure

```
HR_Attrition_analysis/
├── backend/
│   ├── data/original/      IBM CSV (never edited)
│   ├── data/cleaned/       cleaned copy (created automatically)
│   ├── exploration/        Kaggle notebook
│   ├── training/           train_model.py
│   ├── saved_model/        model, results and risk scores (created by training)
│   ├── services/           load_data, features, model_service, explain, risk_levels
│   └── config.py           paths, model inputs, risk cut-offs
├── frontend/
│   ├── app.py              Home page
│   ├── pages/              1_Overview ... 7_Retention_Cost
│   └── components/         filters, charts, data loading, small helpers
├── checks/                 tests
├── project_docs/           problem statement, scope, features
├── requirements.txt
└── README.md
```

## Run it (Windows PowerShell, from the project folder)

1. Create and activate a virtual environment (once):
   ```
   python -m venv .venv
   .venv\Scripts\activate
   ```
2. Install the packages (once):
   ```
   pip install -r requirements.txt
   ```
3. Train and save the model (optional, takes about 5 seconds):
   ```
   python backend/training/train_model.py
   ```
   If you skip this, the dashboard trains the model by itself the first time it opens.
4. Start the dashboard:
   ```
   streamlit run frontend/app.py
   ```
   Your browser opens at http://localhost:8501. Press Ctrl + C in the terminal to stop.

Mac / Linux: activate with `source .venv/bin/activate`.

## Pages

| Page | What the user can do |
|---|---|
| Home | See the loaded dataset and model, open any page, click a risk level |
| Overview | See totals, attrition rate, income and tenure charts |
| Attrition Analysis | Compare who leaves by job role, overtime, age, travel, income and more |
| Resignation Risk | See every employee's risk % and level, filter, search, download CSV |
| Risk Explanation | See why one employee has a high or low risk |
| Model Performance | See ROC-AUC, precision, recall, confusion matrix, important factors |
| What-If Simulator | Change overtime, pay, promotion... and see the risk change |
| Retention Cost | Enter a replacement cost and see the expected cost of resignations |

## Run the checks

```
python -m pytest
```

## Troubleshooting

- `ModuleNotFoundError: backend` or `frontend`: run the commands from the project
  folder (the one that contains `backend` and `frontend`).
- `Dataset not found`: the CSV must be at
  `backend/data/original/WA_Fn-UseC_-HR-Employee-Attrition.csv`.
- Streamlit not found: activate the virtual environment first (`(.venv)` must
  show at the start of the terminal line).
- A saved model made with another scikit-learn version is retrained automatically.

## Notes and limits

- Gender and marital status are not used by the model.
- Employees are identified by Employee Number (the dataset has no names).
- One public, fictional company; the model finds patterns, not causes.
- There is no login and no data upload; the dataset and model are files in the project.
