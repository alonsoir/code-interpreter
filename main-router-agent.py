from langchain.agents import AgentExecutor
from langchain.agents import AgentType, initialize_agent
from langchain.agents import Tool
from langchain.chat_models import ChatOpenAI
from langchain_experimental.tools import PythonREPLTool
from langchain import hub
from langchain_experimental.agents import create_csv_agent
from langchain.agents import create_openai_functions_agent
from dotenv import load_dotenv

load_dotenv()
pythontools = [PythonREPLTool()]
instructions = """You are an agent designed to write and execute python code to answer questions.
   You have access to a python REPL, which you can use to execute python code.
   If you get an error, debug your code and try again.
   Only use the output of your code to answer the question. 
   You might know the answer without running any code, but you should still run the code to get the answer.
   If it does not seem like you can write code to answer the question, just return "I don't know" as the answer.
   """
base_prompt = hub.pull("langchain-ai/openai-functions-template")
prompt = base_prompt.partial(instructions=instructions)
agentpython = create_openai_functions_agent(
    ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0), pythontools, prompt
)
agent_pythonexecutor = AgentExecutor(
    agent=agentpython, tools=pythontools, verbose=True
)

csv_agent = create_csv_agent(
        ChatOpenAI(temperature=0, model="gpt-3.5-turbo"),
        "titanic.csv",
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    )


# Crea el router de agentes
router_agent = initialize_agent(
    tools=[
        Tool(
            name="PythonCodeAgent",
            func=agent_pythonexecutor.invoke,
            description="""useful when you need to transform natural language and write from it python and execute the python code,
                          returning the results of the code execution,
                          DO NOT SEND PYTHON CODE TO THIS TOOL""",
        ),
        Tool(
            name="CSVAgent",
            func=csv_agent.run,
            description="""useful when you need to answer question over titanic.csv file,
                             takes an input the entire question and returns the answer after running pandas calculations""",
        ),
    ],
    llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo"),
    agent_type=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
)

# Usa el router de agentes para ejecutar una tarea
router_agent.run(
    {
        "input": "generate and save in current working directory 15 QRcodes that point to www.udemy.com/course/langchain, you have qrcode package installed already"
    }
)

# Usa el router de agentes para hacer una pregunta sobre el archivo CSV
# router_agent.run({"input": "print how many people have more than 3 siblings"})
