from strategy import RouteStrategy 
class WalkStrategy(RouteStrategy):
    def build_route(self, a, b):
        return f"Walking from {a} to {b}: Walk through the park, takes 2 hours"
