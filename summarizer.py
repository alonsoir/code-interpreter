from dotenv import load_dotenv
from langchain.agents import initialize_agent, Tool
from langchain.utilities import WikipediaAPIWrapper
from langchain_openai import ChatOpenAI


# Summarize an unknown amount of text
# What if you have an unknown amount of text you need to summarize? This may be a verticalize use case (like law or medical) where more research is required as you uncover the first pieces of information.

# We're going to use agents below, this is still a very actively developed area and should be handled with care. Future agents will be able to handle a lot more complicated tasks.

def main():
    print("hello summarizer")
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    wikipedia = WikipediaAPIWrapper()
    tools = [
        Tool(
            name="Wikipedia",
            func=wikipedia.run,
            description="Useful for when you need to get information from wikipedia about a single topic",
        ),
    ]

    agent_executor = initialize_agent(
        tools, llm, agent="zero-shot-react-description", verbose=True
    )
    query = {
        "input": "Can you please provide a quick summary of Napoleon Bonaparte? \
                              Then do a separate search and tell me what the commonalities are with Serena Williams"
    }
    output = agent_executor.invoke(query)
    print(output)


if __name__ == "__main__":
    load_dotenv()
    main()
