from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
from constants.pipeline_functions import enriched_query,top_results,final_result,final_stream_result

class UserInput(TypedDict):
    query: str
    enriched_query: str
    top_results: list[str]
    final_result: str

graph=StateGraph(UserInput)

graph.add_node('enriched_query',enriched_query)
graph.add_node('top_results',top_results)
graph.add_node('final_result',final_result)

graph.add_edge(START,'enriched_query')
graph.add_edge('enriched_query','top_results')
graph.add_edge('top_results','final_result')
graph.add_edge('final_result',END)

workflow=graph.compile()
graph.compile()

def inference(query: str):
    initial_state = {
        "query": query
    }

    result = workflow.invoke(initial_state)
    return result["final_result"]

def inference_stream(query: str):
    initial_state = {
        "query": query
    }

    initial_state.update(enriched_query(initial_state))
    initial_state.update(top_results(initial_state))
    yield from final_stream_result(initial_state)