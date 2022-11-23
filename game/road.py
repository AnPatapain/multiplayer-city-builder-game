
"""The road is define by the connection between them
    TL : road_connection[0] -> \ / <- TR : road_connection[1]
                                x    
    BL : road_connection[3] -> / \ <- BR : road_connection[2]
"""

class Road :
    def __init__(self, road_connection) :
        self.road_connection = road_connection