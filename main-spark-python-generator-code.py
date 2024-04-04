from dotenv import load_dotenv
from langchain_experimental.agents.agent_toolkits import create_spark_dataframe_agent
from langchain_openai import OpenAI
from pyspark.sql import SparkSession


def main():
    print("hello from spark world!!!")
    # Run this command to create your spark context
    # ./sbin/start-connect-server.sh --packages org.apache.spark:spark-connect_2.12:3.4.0
    # Run this command to know if there is a java pid using this 15002 port.
    # lsof -iTCP -sTCP:LISTEN -n -P | grep 15002
    # Be sure that this client runs the same version than spark server, in this example, i have in my local spark-3.4.0.
    # Check Pipfile to change versions if your cluster is above or below.
    spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
    # spark = SparkSession.builder.getOrCreate()
    csv_file_path = "titanic.csv"
    df = spark.read.csv(csv_file_path, header=True, inferSchema=True)
    df.show()
    agent = create_spark_dataframe_agent(llm=OpenAI(temperature=0), df=df, verbose=True)
    agent.run("how many rows are there?")
    agent.run("how many people have more than 3 siblings")
    agent.run("whats the square root of the average age?")
    agent.run("Crea un fichero parquet a partir del fichero titanic.csv")
    agent.run(
        """
    who bought the most expensive ticket?
    You can find all supported function types in https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/dataframe
    """
    )
    spark.stop()


if __name__ == "__main__":
    load_dotenv()
    main()
