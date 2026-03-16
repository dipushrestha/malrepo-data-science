-- Report Queries

-- Executive summary
SELECT
    COUNT(*) AS total_transactions,
    SUM(transaction_amount) AS total_volume,
    AVG(transaction_amount) AS avg_transaction,
    COUNT(DISTINCT account_id) AS unique_accounts,
    COUNT(CASE WHEN is_fraud THEN 1 END) AS flagged_fraud,
    SUM(CASE WHEN is_fraud THEN transaction_amount ELSE 0 END) AS fraud_volume,
    ROUND(100.0 * COUNT(CASE WHEN is_fraud THEN 1 END) / NULLIF(COUNT(*), 0), 4) AS fraud_rate_pct
FROM transactions;

-- Top risky accounts
SELECT
    t.account_id,
    COUNT(*) AS txn_count,
    SUM(t.transaction_amount) AS total_volume,
    COUNT(CASE WHEN t.is_fraud THEN 1 END) AS fraud_count,
    MAX(p.probability) AS max_risk_score
FROM transactions t
LEFT JOIN predictions p ON t.transaction_id = p.transaction_id
GROUP BY t.account_id
HAVING COUNT(CASE WHEN t.is_fraud THEN 1 END) > 0
ORDER BY fraud_count DESC
LIMIT 50;
