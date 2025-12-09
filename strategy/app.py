from road_strategy import RoadStrategy
from walk_strategy import WalkStrategy
from navigator import Navigator

loc1 = "Home"
loc2 = "Office"
nav = Navigator(RoadStrategy())
nav.get_directions(loc1, loc2)

nav.set_strategy(WalkStrategy())
nav.get_directions(loc1, loc2)

