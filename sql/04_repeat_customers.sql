-- Q: What share of customers buy more than once?
WITH per_customer AS (
    SELECT c.customer_unique_id, COUNT(DISTINCT o.order_id) AS n_orders
    FROM orders o
    JOIN customers c USING (customer_id)
    WHERE o.order_status = 'delivered'
    GROUP BY 1
)
SELECT COUNT(*) AS customers,
       SUM(n_orders > 1) AS repeat_customers,
       ROUND(100.0 * SUM(n_orders > 1) / COUNT(*), 2) AS repeat_rate_pct
FROM per_customer;
