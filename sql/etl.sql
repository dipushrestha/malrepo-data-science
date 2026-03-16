-- ETL Queries for FinAnalytics

-- Daily transaction summary
CREATE TABLE IF NOT EXISTS daily_summary AS
SELECT
    DATE(timestamp) AS txn_date,
    COUNT(*) AS total_transactions,
    SUM(transaction_amount) AS total_amount,
    AVG(transaction_amount) AS avg_amount,
    COUNT(CASE WHEN is_fraud THEN 1 END) AS fraud_count,
    SUM(CASE WHEN is_fraud THEN transaction_amount ELSE 0 END) AS fraud_amount
FROM transactions
GROUP BY DATE(timestamp)
ORDER BY txn_date;

-- Account risk scores
SELECT
    account_id,
    COUNT(*) AS txn_count,
    AVG(transaction_amount) AS avg_amount,
    MAX(transaction_amount) AS max_amount,
    STDDEV(transaction_amount) AS std_amount,
    COUNT(CASE WHEN is_fraud THEN 1 END)::FLOAT / NULLIF(COUNT(*), 0) AS fraud_rate
FROM transactions
GROUP BY account_id
HAVING COUNT(*) >= 10
ORDER BY fraud_rate DESC;
