# Data Dictionary

## Raw Data: `transactions.csv`

| Column | Type | Description |
|--------|------|-------------|
| transaction_id | int | Unique transaction identifier |
| account_id | int | Account identifier |
| transaction_amount | float | Transaction amount in USD |
| account_balance | float | Account balance at time of transaction |
| merchant_category | string | Merchant category (retail, food, travel, etc.) |
| transaction_type | string | Transaction type (debit, credit) |
| is_fraud | int | Fraud label (0=legitimate, 1=fraud) |
| timestamp | datetime | Transaction timestamp |

## Processed Features: `features.parquet`

All columns from raw data plus:

| Column | Type | Description |
|--------|------|-------------|
| log_amount | float | Log-transformed transaction amount |
| amount_zscore | float | Z-score of transaction amount |
| acct_avg_amount | float | Account average transaction amount |
| acct_std_amount | float | Account std dev of transaction amount |
| acct_txn_count | int | Account total transaction count |
| acct_max_amount | float | Account max transaction amount |
| amount_to_avg_ratio | float | Amount / account average ratio |
| amount_to_balance_ratio | float | Amount / account balance ratio |
| hour_of_day | int | Hour of transaction (0-23) |
| day_of_week | int | Day of week (0=Monday, 6=Sunday) |
| is_weekend | int | Weekend flag |
| is_business_hours | int | Business hours flag (9am-5pm) |
