exec(open('./transformation.py').read())

df_clean.createOrReplaceTempView("df_clean")

result = spark.sql("""
SELECT
    CASE
        WHEN `Discount_%` < 0.25 THEN '0–0.25'
        WHEN `Discount_%` < 0.50 THEN '0.25–0.50'
        WHEN `Discount_%` < 0.75 THEN '0.50–0.75'
        ELSE '0.75–1.0'
    END AS discount_bucket,
    AVG(Profit) AS avg_profit,
    COUNT(*) AS total
FROM df_clean
WHERE `Discount_%` IS NOT NULL
GROUP BY discount_bucket
""")
result.display()
result.write.format("delta").saveAsTable("snitch.snitch_schema.discount_profit")
