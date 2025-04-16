from langgraph.graph import StateGraph
from langchain_core.runnables import RunnableLambda
from src.agents.state import GraphState

# Nodes
from src.agents.nodes.router_node import router_node
from src.agents.nodes.info_node import info_node_runnable
from src.agents.nodes.availability_node import availability_node_runnable
from src.agents.nodes.response_node import response_node_runnable

# Wrap the router function in a RunnableLambda
router_node_runnable = RunnableLambda(router_node)

# Build the graph
graph = StateGraph(GraphState)

graph.add_node("router", router_node_runnable)
graph.add_node("info_node", info_node_runnable)
graph.add_node("availability_node", availability_node_runnable)
graph.add_node("response_node", response_node_runnable)

# Conditional routing based on router_node output
graph.add_conditional_edges(
    "router",
    {
        "info_node": "info_node",
        "availability_node": "availability_node",
        "both_node": "info_node",  # First goes to info, then continues to response
        "end": "response_node"
    }
)

# Define the edges from tools to final response
graph.add_edge("info_node", "response_node")
graph.add_edge("availability_node", "response_node")

# Entry and exit points
graph.set_entry_point("router")
graph.set_finish_point("response_node")

# Compile the graph
graph_runnable = graph.compile()
