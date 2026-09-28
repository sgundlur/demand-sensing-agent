from .graph import build_graph

class DemandSensingAgent:
    def __init__(self): self.graph=build_graph()
    def run(self,forecast_date=None,horizon_days=31):
        return self.graph.invoke({"forecast_date":forecast_date,"horizon_days":horizon_days})
