-- Analytics Queries

-- Fraud by merchant category
SELECT
    merchant_category,
    COUNT(*) AS total_txns,
    COUNT(CASE WHEN is_fraud THEN 1 END) AS fraud_txns,
    ROUND(100.0 * COUNT(CASE WHEN is_fraud THEN 1 END) / NULLIF(COUNT(*), 0), 2) AS fraud_pct,
    AVG(CASE WHEN is_fraud THEN transaction_amount END) AS avg_fraud_amount
FROM transactions
GROUP BY merchant_category
ORDER BY fraud_pct DESC;

-- Hourly fraud pattern
SELECT
    EXTRACT(HOUR FROM timestamp) AS hour_of_day,
    COUNT(*) AS total_txns,
    COUNT(CASE WHEN is_fraud THEN 1 END) AS fraud_txns,
    ROUND(100.0 * COUNT(CASE WHEN is_fraud THEN 1 END) / NULLIF(COUNT(*), 0), 2) AS fraud_pct
FROM transactions
GROUP BY EXTRACT(HOUR FROM timestamp)
ORDER BY hour_of_day;

-- Monthly trend
SELECT
    DATE_TRUNC('month', timestamp) AS month,
    COUNT(*) AS total_txns,
    SUM(transaction_amount) AS total_volume,
    COUNT(CASE WHEN is_fraud THEN 1 END) AS fraud_count
FROM transactions
GROUP BY DATE_TRUNC('month', timestamp)
ORDER BY month;
