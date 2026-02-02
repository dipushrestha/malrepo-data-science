CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    transaction_date TIMESTAMP NOT NULL,
    customer_id INT,
    amount DECIMAL(10, 2),
    currency VARCHAR(3)
);

CREATE TABLE IF NOT EXISTS market_data (
    ticker VARCHAR(10),
    date DATE,
    open_price DECIMAL(10, 2),
    close_price DECIMAL(10, 2),
    volume BIGINT,
    PRIMARY KEY (ticker, date)
);
