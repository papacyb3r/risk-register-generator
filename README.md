# Risk Register Generator

Turn a simple CSV of risks into a prioritised risk register with scores, ratings and a heat map. No dependencies, just Python 3.8+.

## Quick start

~~~bash
python risk_register.py sample_risks.csv
python risk_register.py sample_risks.csv --out register.md
~~~

## Input format

| Column | Meaning |
|---|---|
| id | Unique risk identifier |
| risk | Short description |
| likelihood | 1 (rare) to 5 (almost certain) |
| impact | 1 (minor) to 5 (severe) |
| owner | Who is accountable |
| treatment | Mitigate, transfer, accept or avoid, with detail |

## How scoring works

Score = likelihood x impact (1 to 25), then:

| Rating | Score |
|---|---|
| Critical | 17 to 25 |
| High | 10 to 16 |
| Medium | 5 to 9 |
| Low | 1 to 4 |

Adjust the bands in the BANDS list at the top of the script to match your organisation's risk appetite.

## Output

A Markdown report with a summary count by rating, risks ranked by score, and a 5x5 heat map showing where each risk sits.

## Notes

All sample data is fictional. This tool supports risk assessment practice aligned with frameworks such as ISO/IEC 27005 and ISO/IEC 27001 clause 6.1.2, but it does not replace a full risk management process.

## Author

Papa, GRC, Risk & Cybersecurity Compliance Leader. [LinkedIn](https://www.linkedin.com/in/owoahene)
