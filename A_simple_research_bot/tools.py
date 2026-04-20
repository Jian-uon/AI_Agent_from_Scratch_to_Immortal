from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import tool
from datetime import datetime
import wikipedia

_search = DuckDuckGoSearchRun()

@tool
def search_tool(query: str) -> str:
    """Search the web for information."""
    return _search.run(query)


def save_to_txt(data: str, filename:str = "research_output.txt"):
    timestamp= datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"---Research Output ---\n Timestamp:{timestamp}\n\n{data}\n\n"
    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)

    return f"Data successfully saved to {filename}"

@tool
def save_tool(data: str) -> str:
    """Save information to a local text file."""
    return save_to_txt(data)