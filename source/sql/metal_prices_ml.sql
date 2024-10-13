CREATE OR REPLACE VIEW metal_prices_ml AS
SELECT
    id,
    timestamp,
    silver_price AS "XAGUSD",
    gold_price AS "XAUUSD",
    palladium_price AS "XPDUSD",
    platinum_price AS "XPTUSD"
FROM metal_prices_analytics
ORDER BY timestamp DESC
LIMIT 12;
