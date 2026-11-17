-- Q: Which product categories drive the most revenue?
SELECT COALESCE(t.product_category_name_english, p.product_category_name) AS category,
       COUNT(DISTINCT oi.order_id) AS orders,
       ROUND(SUM(oi.price), 2) AS revenue,
       ROUND(100.0 * SUM(oi.price) / SUM(SUM(oi.price)) OVER (), 1) AS revenue_share_pct
FROM order_items oi
JOIN products p USING (product_id)
LEFT JOIN product_category_name_translation t USING (product_category_name)
GROUP BY 1
ORDER BY revenue DESC
LIMIT 15;
