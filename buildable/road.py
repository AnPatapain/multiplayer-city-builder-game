from class_types.road_types import RoadTypes

"""The road is define by the connection between them
    TL : road_connection[0] -> \ / <- TR : road_connection[1]
                                x    
    BL : road_connection[3] -> / \ <- BR : road_connection[2]
"""


class Road:
    def __init__(self, road_connection: []):
        # Control road_connection size
        if len(road_connection) < 4:
            for i in range(len(road_connection), 4, 1):
                road_connection.append(None)

        self.road_connection = road_connection
        self.road_type = RoadTypes.ALONE
        self.update_road()

    def set_connect(self, road, position):
        # Update one connection of a road
        self.road_connection[position] = road
        self.update_road()

    def get_road_connection(self):
        return self.road_connection

    def set_road_connection(self, road_connection):
        # Test and resize road Connection
        if len(road_connection) < 4:
            for i in range(len(road_connection), 4, 1):
                road_connection.append(None)

        self.road_connection = road_connection
        self.update_road()

    def get_road_type(self):
        return self.road_type

    def update_road(self):
        def update_1():
            # Test one connection Road
            for i in range(4):
                if self.road_connection[i]:
                    self.road_type = RoadTypes.ALONE + i

        def update_2():
            # Test diagonal road
            if self.road_connection[0] and self.road_connection[2]:
                self.road_type = RoadTypes.TL_TO_BR
                return

            if self.road_connection[1] and self.road_connection[3]:
                self.road_type = RoadTypes.TR_TO_BL
                return

            # Test angle road
            for i in range(4):
                if self.road_connection[i] and self.road_connection[(i+1)%4]:
                    self.road_type = RoadTypes.TR_TO_BL + i

        def update_3():
            # Test 3 road connection
            for i in range(4):
                if self.road_connection[i] and self.road_connection[(i+1)%4] and self.road_connection[(i+2)%4]:
                    self.road_type = RoadTypes.BL_TO_TL + i

        match sum(x is not None for x in self.road_connection):
            case 0:
                self.road_type = RoadTypes.ALONE
            case 1:
                update_1()
            case 2:
                update_2()
            case 3:
                update_3()
            case 4:
                self.road_type = RoadTypes.ALL_DIRECTION
            case _:
                print("Road error please update Road connection list")
                self.road_type = RoadTypes.ALONE
