-- Q: Does late delivery hurt review scores?
SELECT CASE
         WHEN julianday(order_delivered_customer_date) > julianday(order_estimated_delivery_date)
         THEN 'late' ELSE 'on_time' END AS delivery_status,
       COUNT(*) AS orders,
       ROUND(AVG(r.review_score), 2) AS avg_review
FROM orders o
JOIN order_reviews r USING (order_id)
WHERE o.order_delivered_customer_date IS NOT NULL
GROUP BY 1;
