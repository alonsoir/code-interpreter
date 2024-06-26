import base64

from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor
from langchain_experimental.tools import PythonREPLTool
from langchain.agents import create_openai_functions_agent
from langchain_openai import ChatOpenAI


def main():
    print("Starting...")
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

    agent_pythonexecutor.invoke({"input": "What is the 10th fibonacci number?"})
    agent_pythonexecutor.invoke(
        {
            "input": "Cual es la mejor manera de instalar PyTorch si tengo osx y quiero usar pipenv?"
        }
    )
    agent_pythonexecutor.invoke(
        {
            "input": """Understand, write a single neuron neural network in PyTorch.
Take synthetic data for y=2x. Train for 1000 epochs and print every 100 epochs.
Return prediction for x = 5"""
        }
    )
    agent_pythonexecutor.invoke(
        {
            "input": """generate and save in current working directory 1 qrcodes that point to https://www.aironman2k.wordpress.com"""
        }
    )


def generate_base64(code):
    # Convertir el código a base64
    encoded_code = base64.b64encode(code.encode("utf-8")).decode("utf-8")
    print(encoded_code)


if __name__ == "__main__":
    load_dotenv()
    main()
