from strategy import RouteStrategy
class RoadStrategy(RouteStrategy):
    def build_route(self, a, b):
        return f"Road Route from {a} to {b} : Drive I-95, takes 30 mins"
