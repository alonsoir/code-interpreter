from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_openai import ChatOpenAI, OpenAI
from dotenv import load_dotenv
from langchain.document_loaders import PagedPDFSplitter


def loadPDF():
    loader = PagedPDFSplitter("mycv.pdf")
    data = loader.load()
    print(data)


def main():
    print("hello! This is a langchain agent tryin to solve answers from csv files.")
    agent = create_csv_agent(
        OpenAI(temperature=0),
        "titanic.csv",
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    )
    agent.run("how many rows are there?")
    agent.run("how many people have more than 3 siblings")
    agent.run("whats the square root of the average age?")

    agent = create_csv_agent(
        ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"),
        ["titanic.csv", "tested.csv"],
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
    )
    agent.run("how many rows in the age column are different between the two dfs?")


if __name__ == "__main__":
    load_dotenv()
    main()
    loadPDF()
