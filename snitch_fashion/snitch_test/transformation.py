from pyspark.sql.functions import coalesce, lit, when, col, try_to_timestamp, expr

df = spark.read.csv(
    "/Volumes/snitch/default/raw/Snitch_Fashion_Sales_Uncleaned.csv",
    header=True,
    inferSchema=True,
)

df_clean = (
    (
        df.withColumn(
            "City", when(col("City") == "bengaluru", "Bangalore").otherwise(col("City"))
        )
        .withColumn(
            "City", when(col("City") == "hyderbad", "Hyderabad").otherwise(col("City"))
        )
        .withColumn(
            "City", when(col("City") == "Hyd", "Hyderabad").otherwise(col("City"))
        )
        .withColumn(
            "Units_Sold",
            when(col("Units_Sold") < 0, lit(None)).otherwise(col("Units_Sold")),
        )
        .withColumn(
            "Discount_%",
            when(col("Discount_%") > 1, lit(None)).otherwise(col("Discount_%")),
        )
    )
    .withColumn(
    "date_format_uncertain",
    col("Order_Date").rlike("^[0-9]{2}-[0-9]{2}-[0-9]{4}$")
)
.withColumn(
    "Order_Date",
    coalesce(
        try_to_timestamp(col("Order_Date")),
        expr("try_to_timestamp(Order_Date, 'dd-MM-yyyy')"),
        expr("try_to_timestamp(Order_Date, 'MM-dd-yyyy')"),
        expr("try_to_timestamp(Order_Date, 'yyyy/MM/dd')"),
    ),
))
# Order_ID är inte unik — flera rader delar samma ID med olika kunder och produkter.
# Ingen deduplicering görs i silver. Surrogatnyckel hanteras i gold vid behov.