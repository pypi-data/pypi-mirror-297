import polars as pl

def help():
    print("""Dear User,

Thank you for choosing the NotificationList package. We sincerely appreciate your support.

Should you require any assistance or have any questions, please do not hesitate to reach out to Ranjeet Aloriya at ranjeet.aloriya@gmail.com. We are here to help!

Best regards,
Ranjeet Aloriya""")
    
def initial_unqid(file_path):
    df = pl.read_csv(file_path, encoding="latin", infer_schema_length=0)
    df = df.with_columns([pl.col(col).alias(col.upper()) for col in df.columns])
    df = df.select([pl.col(col).str.to_uppercase().alias(col) if df.schema[col] == pl.Utf8 else pl.col(col) for col in df.columns])
    df = df.sort(by=['FIRST NAME', 'LAST NAME', 'MIDDLE NAME'])
    serial_numbers = pl.arange(1, df.height + 1).cast(pl.Utf8)
    df = df.with_columns(serial_numbers.alias("S N")).select(["S N"] + df.columns)
    df = df.with_columns(
        pl.concat_str(
            [
                pl.col("FIRST NAME").fill_null(""),
                pl.col("LAST NAME").fill_null(""),
            ],
            separator=" ",
        ).alias("FIRST LAST"),
    )
    df = df.with_columns(
        pl.concat_str(
            [
                pl.col("FIRST NAME").fill_null(""),
                pl.col("MIDDLE NAME").fill_null(""),
                pl.col("LAST NAME").fill_null(""),
            ],
            separator=" ",
        ).alias("FULL NAME"),
    )
    df = df.with_columns(pl.col("FIRST LAST").str.replace_all(r'[^a-zA-Z]', ' '))
    df = df.with_columns(pl.col("FULL NAME").str.replace_all(r'[^a-zA-Z]', ' '))
    df = df.with_columns(pl.col("FIRST LAST").str.split(" ").list.unique().list.sort().list.join(" ").alias("FIRST LAST"))
    df = df.with_columns(pl.col("FULL NAME").str.split(" ").list.unique().list.sort().list.join(" ").alias("FULL NAME"))
    df = df.with_columns(pl.col("FIRST LAST").str.replace_all(r' ', ''))
    df = df.with_columns(pl.col("FULL NAME").str.replace_all(r' ', ''))
    df = df.join(df.group_by("FIRST LAST").agg(pl.col("S N").str.concat(",").alias("FIRST_LAST")),on="FIRST LAST")
    df = df.join(df.group_by("FULL NAME").agg(pl.col("S N").str.concat(",").alias("FUll_NAME")),on="FULL NAME")
    df = df.with_columns(pl.concat_str([df["FIRST_LAST"], df["FUll_NAME"]], separator=",").str.split(",").list.unique().list.sort().list.join(",").alias("id"))
    column_b = [
    ",".join(sorted({num for element in cell.split(",") for other in df['id'] if element in other.split(",") for num in other.split(",")}, key=int))
    for cell in df['id']
    ]

# Add Column B to the DataFrame
    df = df.with_columns(pl.Series("B", column_b))
    df = df.with_columns(pl.col("B").rank(method='dense').alias("Dense Rank"))
    unique_ids = [f"UNQ_{int(rank):08d}" for rank in df['Dense Rank']]
    df = df.with_columns(pl.Series("UNIQUE ID", unique_ids))
    df = df.drop(["S N", "FIRST LAST", "FULL NAME", "FIRST_LAST", "FUll_NAME", "id", "Dense Rank"])
    df = df.sort('UNIQUE ID')
    serial_numbers = pl.arange(1, df.height + 1).cast(pl.Utf8)
    df = df.with_columns(serial_numbers.alias("S N")).select(["S N"] + df.columns)
    df = df.select(["S N", "UNIQUE ID"] + [col for col in df.columns if col not in ["S N", "UNIQUE ID"]])
    return df