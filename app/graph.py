from langgraph.graph import StateGraph, START, END
from .state import DemandSensingState
from .node import load_inputs, run_m2_forecast, compare_m1, explain, insights, alerts

def build_graph():
    g=StateGraph(DemandSensingState)
    g.add_node("load_inputs",load_inputs)
    g.add_node("m2_forecast",run_m2_forecast)
    g.add_node("compare_m1",compare_m1)
    g.add_node("explain",explain)
    g.add_node("insights",insights)
    g.add_node("alerts",alerts)
    g.add_edge(START,"load_inputs"); g.add_edge("load_inputs","m2_forecast")
    g.add_edge("m2_forecast","compare_m1"); g.add_edge("compare_m1","explain")
    g.add_edge("explain","insights"); g.add_edge("insights","alerts"); g.add_edge("alerts",END)
    return g.compile()
