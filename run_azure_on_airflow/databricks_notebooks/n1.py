dbutils.fs.ls("/mnt/bronze_layer")
# Define the path to the cleansed CSV file
cleansed_file_path = "/mnt/bronze_layer/rsgoutput.csv"




from pyspark.sql.types import StructType, StructField, IntegerType, StringType

# Define the schema for the CSV file
schema = StructType([
    StructField("roll_no", IntegerType(), True),  # Roll number (integer)
    StructField("name", StringType(), True),      # Name (string)
    StructField("marks", IntegerType(), True),    # Marks (integer)
    StructField("city", StringType(), True),      # City (string)
    StructField("age", IntegerType(), True)       # Age (integer), assuming age can be NULL
])

# Read the CSV file with the custom schema
df = spark.read.option("header", False).schema(schema).csv("/mnt/bronze_layer/rsgoutput.csv")  # Replace with your actual file path

# Show the DataFrame
df.show()

# Define the JDBC connection properties
jdbc_hostname = "rsgdbserver123.database.windows.net"
jdbc_port = 1433
jdbc_database = "rsgdb"
jdbc_url = f"jdbc:sqlserver://{jdbc_hostname}:{jdbc_port};database={jdbc_database}"

connection_properties = {
  "user" : "rsg",  # Your SQL auth username
  "password" : "Ketki@134133??",  # Your SQL auth password
  "driver" : "com.microsoft.sqlserver.jdbc.SQLServerDriver"
}

# Define the table name
table_name = "dbo.YourTableName"  # Replace with your actual table name

# Write the DataFrame to the Azure SQL Database
df.write.jdbc(url=jdbc_url, table=table_name, mode="append", properties=connection_properties)




