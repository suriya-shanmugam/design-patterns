from strategy import RouteStrategy
class Navigator:
    def __init__(self, strategy:RouteStrategy):
        self._strategy = strategy
    
    def set_strategy(self, strategy:RouteStrategy):
        print(f"----Switching strategy from {type(self._strategy).__name__} to {type(strategy).__name__}------")
        self._strategy = strategy

    def get_directions(self, a, b):
        result = self._strategy.build_route(a,b)
        print(result)

