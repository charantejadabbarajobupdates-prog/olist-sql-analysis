-- Q: How many customers from each first-purchase cohort come back in later months?
WITH first_orders AS (
    SELECT c.customer_unique_id,
           MIN(strftime('%Y-%m', o.order_purchase_timestamp)) AS cohort_month
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    GROUP BY c.customer_unique_id
),
activity AS (
    SELECT DISTINCT c.customer_unique_id,
           strftime('%Y-%m', o.order_purchase_timestamp) AS active_month
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
)
SELECT f.cohort_month,
       a.active_month,
       COUNT(DISTINCT a.customer_unique_id) AS customers
FROM first_orders f
JOIN activity a USING (customer_unique_id)
GROUP BY 1, 2
ORDER BY 1, 2;
