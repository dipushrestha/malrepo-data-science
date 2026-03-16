-- Staging model for raw transactions
WITH source AS (
    SELECT * FROM {{ source('raw', 'transactions') }}
),

cleaned AS (
    SELECT
        transaction_id,
        account_id,
        CAST(transaction_amount AS DECIMAL(12,2)) AS transaction_amount,
        CAST(account_balance AS DECIMAL(14,2)) AS account_balance,
        LOWER(TRIM(merchant_category)) AS merchant_category,
        LOWER(TRIM(transaction_type)) AS transaction_type,
        COALESCE(is_fraud, FALSE) AS is_fraud,
        CAST(timestamp AS TIMESTAMP) AS transaction_timestamp,
        EXTRACT(HOUR FROM timestamp) AS hour_of_day,
        EXTRACT(DOW FROM timestamp) AS day_of_week
    FROM source
    WHERE transaction_amount >= 0
      AND timestamp IS NOT NULL
)

SELECT * FROM cleaned
