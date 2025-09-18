from langgraph.graph import StateGraph
from nodes.format_classifier_output import format_classifier_output

# Define the graph
graph = StateGraph()

# Add the formatter node
graph.add_node("formatter", format_classifier_output)

# Set entry and exit points
graph.set_entry_point("formatter")
graph.set_finish_point("formatter")

# Compile the graph
compiled_graph = graph.compile()