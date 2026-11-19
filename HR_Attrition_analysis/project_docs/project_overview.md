# HR Attrition Analytics Dashboard

## Problem statement
Small businesses often manage employee information manually, in paper files or
separate spreadsheets. Records are scattered, building even a simple report takes
time, and owners usually learn that an employee is leaving only when the person
resigns, when it is too late to act. Replacing an employee costs time, money and
experience. In the IBM HR dataset, 237 of 1,470 employees (16%) left, a small group
that is hard to spot by hand.

This project builds a Streamlit dashboard that organizes HR data in one place,
shows useful statistics and charts, and predicts each employee's resignation risk
so HR can plan retention actions early.

## Objectives
1. Show employee and salary statistics in one organized dashboard.
2. Show attrition by job role, overtime, age group, business travel and income.
3. Predict each employee's resignation risk (Low / Medium / High) with a Random Forest.
4. Explain which factors raise or lower an employee's risk.
5. Reduce manual work with filters and CSV export.

## Target users
HR staff, administrators and business owners. All see the same dashboard (no login).

## Scope
In: dashboard-only Streamlit app; IBM HR dataset and a saved model stored as files in
the project; statistics, risk list, explanation, model results, what-if, cost estimate.
Out: login, data upload, adding/editing employees, attendance, leave requests,
department management, predicting when someone will resign, live data, cloud deployment.

## Features (description: user can ...)
| # | Feature | Priority | Description (user can ...) |
|---|---|---|---|
| 1 | Home | Must have | see which dataset and model are loaded, open any page, and click a risk level to go straight to those employees |
| 2 | Overview | Must have | see total employees, how many left, the attrition rate, average income and tenure, with charts by department |
| 3 | Attrition Analysis | Must have | compare who leaves and who stays by job role, overtime, age group, travel, income and more |
| 4 | Resignation Risk | Must have | see every employee (by number) with a risk % and a Low / Medium / High level, highest first |
| 5 | Filters | Must have | narrow pages to a department, job role, overtime group, age range or employee group |
| 6 | Risk Explanation | Should have | pick one employee and see which factors push their risk up or down |
| 7 | Model Performance | Should have | see how well the model predicts and which factors matter most |
| 8 | Export | Should have | download the filtered risk list as a CSV file |
| 9 | What-If Simulator | Nice to have | change an employee's overtime, pay or promotion and see how the risk changes |
| 10 | Retention Cost | Nice to have | enter a replacement cost and see the expected cost of likely resignations |

## Results from the saved model (5-fold cross-validation)
- ROC-AUC 0.81; accuracy 86%; precision 58%; recall 43% (flagged High = risk 30%+).
- Employees rated High actually left 58% of the time, Medium 22%, Low 5%
  (overall 16%).
- A Logistic Regression comparison scored a similar ROC-AUC (0.82), so the
  Random Forest is chosen for its explanations, not because it is far better.

## Limitations
One public, fictional company dataset; the model finds patterns, not causes; risk
scores are estimates for starting conversations, not verdicts; no authentication
(prototype).
