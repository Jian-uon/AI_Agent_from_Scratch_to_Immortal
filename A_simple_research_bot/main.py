from dotenv import load_dotenv
from pydantic import BaseModel, SecretStr
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_agent
import os
from tools import search_tool, save_tool


load_dotenv()


class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]


parser = PydanticOutputParser(pydantic_object=ResearchResponse)

system_prompt = f"""
你是一个科研助手，你将帮助我生成研究论文。
回答用户的提问并可以使用必要的工具。
把输出按照这个格式打包好，注意不要提供其他的文字
{parser.get_format_instructions()}
"""

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=SecretStr(os.getenv("DEEPSEEK_API_KEY") or ""),
    base_url="https://api.deepseek.com/v1",
)

agent = create_agent(model=llm, tools=[search_tool, save_tool], system_prompt=system_prompt)

query = input("What can I help you research? ")
raw_response = agent.invoke({"messages": [{"role": "user", "content": query}]})

try:
    output_text = raw_response["messages"][-1].content
    structured_response = parser.parse(output_text)
    print(structured_response)
except Exception as e:
    print("Error parsing response:", e, "Raw Response -", raw_response)
