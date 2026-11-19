"""Settings shared by the backend (data, model) and the frontend (dashboard)."""
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent
ROOT = BACKEND_DIR.parent

RAW_CSV = BACKEND_DIR / "data" / "original" / "WA_Fn-UseC_-HR-Employee-Attrition.csv"
CLEAN_CSV = BACKEND_DIR / "data" / "cleaned" / "hr_cleaned.csv"
MODEL_FILE = BACKEND_DIR / "saved_model" / "attrition_model.joblib"
RESULTS_JSON = BACKEND_DIR / "saved_model" / "model_results.json"
SCORES_CSV = BACKEND_DIR / "saved_model" / "risk_scores.csv"

# Columns removed from the data:
#  - same value for every employee (no information)
#  - Gender and MaritalStatus: left out so risk scores are not based on them
DROP_COLUMNS = ["EmployeeCount", "Over18", "StandardHours", "Gender", "MaritalStatus"]

# ---- model inputs --------------------------------------------------------
NUMERIC = [
    "Age", "DailyRate", "DistanceFromHome", "Education", "EnvironmentSatisfaction",
    "HourlyRate", "JobInvolvement", "JobLevel", "JobSatisfaction", "MonthlyIncome",
    "MonthlyRate", "NumCompaniesWorked", "PercentSalaryHike", "PerformanceRating",
    "RelationshipSatisfaction", "StockOptionLevel", "TotalWorkingYears",
    "TrainingTimesLastYear", "WorkLifeBalance", "YearsAtCompany",
    "YearsInCurrentRole", "YearsSinceLastPromotion", "YearsWithCurrManager",
]
BINARY = ["OverTime"]  # Yes / No
CATEGORIES = {
    "BusinessTravel": ["Non-Travel", "Travel_Rarely", "Travel_Frequently"],
    "Department": ["Sales", "Research & Development", "Human Resources"],
    "EducationField": ["Life Sciences", "Medical", "Marketing",
                       "Technical Degree", "Other", "Human Resources"],
    "JobRole": ["Sales Executive", "Research Scientist", "Laboratory Technician",
                "Manufacturing Director", "Healthcare Representative", "Manager",
                "Sales Representative", "Research Director", "Human Resources"],
}
FEATURES = NUMERIC + BINARY + list(CATEGORIES)  # original (readable) feature names

# ---- risk levels (probability of resigning) -------------------------------
HIGH_CUT = 0.30     # risk >= 30%  -> High
MEDIUM_CUT = 0.15   # risk >= 15%  -> Medium, otherwise Low

# ---- model settings ------------------------------------------------------
N_FOLDS = 5
RANDOM_STATE = 42
RF_PARAMS = dict(n_estimators=300, max_depth=8, min_samples_leaf=3,
                 random_state=RANDOM_STATE, n_jobs=-1)

LABELS = {
    "Age": "Age", "DailyRate": "Daily rate", "DistanceFromHome": "Distance from home",
    "Education": "Education level", "EnvironmentSatisfaction": "Environment satisfaction",
    "HourlyRate": "Hourly rate", "JobInvolvement": "Job involvement",
    "JobLevel": "Job level", "JobSatisfaction": "Job satisfaction",
    "MonthlyIncome": "Monthly income", "MonthlyRate": "Monthly rate",
    "NumCompaniesWorked": "Companies worked for", "PercentSalaryHike": "Last salary hike (%)",
    "PerformanceRating": "Performance rating",
    "RelationshipSatisfaction": "Relationship satisfaction",
    "StockOptionLevel": "Stock option level", "TotalWorkingYears": "Total working years",
    "TrainingTimesLastYear": "Trainings last year", "WorkLifeBalance": "Work-life balance",
    "YearsAtCompany": "Years at company", "YearsInCurrentRole": "Years in current role",
    "YearsSinceLastPromotion": "Years since last promotion",
    "YearsWithCurrManager": "Years with current manager", "OverTime": "Overtime",
    "BusinessTravel": "Business travel", "Department": "Department",
    "EducationField": "Education field", "JobRole": "Job role",
}
