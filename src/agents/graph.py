from langgraph.graph import StateGraph
from langchain_core.runnables import RunnableLambda, RunnableParallel
from src.agents.state import GraphState

# Nodes
from src.agents.nodes.router_node import router_node
from src.agents.nodes.info_node import info_node_runnable
from src.agents.nodes.availability_node import availability_node_runnable
from src.agents.nodes.response_node import response_node_runnable

# Wrap router logic in a RunnableLambda
router_node_runnable = RunnableLambda(router_node)

# Create a parallel runnable for 'both_node' execution
# This will run info and availability nodes in parallel
both_node_runnable = RunnableParallel({
    "info_node": info_node_runnable,
    "availability_node": availability_node_runnable
}).with_config(run_name="both_node")

# Build the state graph
graph = StateGraph(GraphState)

# Add all nodes to the graph
graph.add_node("router", router_node_runnable)
graph.add_node("info_node", info_node_runnable)
graph.add_node("availability_node", availability_node_runnable)
graph.add_node("response_node", response_node_runnable)
graph.add_node("both_node", both_node_runnable)

# Define conditional routing logic from the router
graph.add_conditional_edges(
    "router",
    {
        "info_node": info_node_runnable,
        "availability_node": availability_node_runnable,
        "both_node": both_node_runnable,
        "end": response_node_runnable
    }
)

# Define transitions from each node to the final response node
graph.add_edge("info_node", "response_node")
graph.add_edge("availability_node", "response_node")
graph.add_edge("both_node", "response_node")  # Collect results after parallel execution

# Set entry and finish points
graph.set_entry_point("router")
graph.set_finish_point("response_node")

# Compile the graph to make it executable
compiled_graph = graph.compile()

# Print the graph structure in ASCII format to visualize it
print(compiled_graph.get_graph().draw_ascii())
