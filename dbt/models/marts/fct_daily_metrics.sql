-- Daily metrics fact table
WITH transactions AS (
    SELECT * FROM {{ ref('stg_transactions') }}
),

daily_agg AS (
    SELECT
        DATE(transaction_timestamp) AS metric_date,
        COUNT(*) AS total_transactions,
        COUNT(DISTINCT account_id) AS unique_accounts,
        SUM(transaction_amount) AS total_volume,
        AVG(transaction_amount) AS avg_transaction_amount,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY transaction_amount) AS median_amount,
        MAX(transaction_amount) AS max_amount,
        COUNT(CASE WHEN is_fraud THEN 1 END) AS fraud_count,
        SUM(CASE WHEN is_fraud THEN transaction_amount ELSE 0 END) AS fraud_volume,
        ROUND(
            100.0 * COUNT(CASE WHEN is_fraud THEN 1 END) / NULLIF(COUNT(*), 0),
            4
        ) AS fraud_rate_pct
    FROM transactions
    GROUP BY DATE(transaction_timestamp)
)

SELECT
    metric_date,
    total_transactions,
    unique_accounts,
    total_volume,
    avg_transaction_amount,
    median_amount,
    max_amount,
    fraud_count,
    fraud_volume,
    fraud_rate_pct,
    -- Rolling averages
    AVG(total_transactions) OVER (ORDER BY metric_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS txn_7d_avg,
    AVG(fraud_rate_pct) OVER (ORDER BY metric_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS fraud_rate_7d_avg
FROM daily_agg
ORDER BY metric_date
