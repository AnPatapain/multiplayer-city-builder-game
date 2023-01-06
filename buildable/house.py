from buildable.building import Buildings

class Houses(Buildings):

        def __init__(self, max_occupants, building_size, cost,HasWater, Tax_Multi,dest_risk, fire_risk):
            Buildings.__init__(self, max_occupants, building_size, cost)
            self.HasWater = HasWater
            self.Tax_Multi = Tax_Multi
            self.dest_risk = dest_risk
            self.fire_risk = fire_risk

        # all Houses are listed in this class
        #bui_SmallTent = Houses(5, '1x1', 10, False, False, False, 1)
        #bui_LargeTent = Houses(7, '1x1', 10, False, False, False, 1)
        #bui_SmallShack = Houses(9, '1x1', 10, False, False, False, 1)
        #bui_LargeShack = Houses(11, '1x1', 10, False, False, False, 1)
        #bui_SmallHovel = Houses(13, '1x1', 10, False, False, False, 2)
        #bui_LargeHovel = Houses(15, '1x1', 10, False, False, False, 2)
        #bui_SmallCasa = Houses(17, '1x1', 10, False, False, False, 2)
        #bui_LargeCasa = Houses(19, '1x1', 10, False, False, False, 2)