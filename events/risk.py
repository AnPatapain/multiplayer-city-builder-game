import random as rd

class Risk:
    def __init__(self, fire_risk, dest_risk):
        self.fire_risk = fire_risk
        self.dest_risk = dest_risk
        self.fire_risk_status = 0 if fire_risk else -1
        self.dest_risk_status = 0 if dest_risk else -1
        self.overlay_update = False
        self.network_update = False


    def risk_progress(self):
        if 0 <= self.fire_risk_status < 100:     #risk increases as soon as the building is created

            if rd.randint(0, 100) < self.fire_risk:      #every type of building has different odds
                self.fire_risk_status += 10
                self.overlay_update = True
                self.network_update = True


        if 0 <= self.dest_risk_status < 100:  # risk increases as soon as the building is created

            if rd.randint(0, 100) < self.dest_risk:  # every type of building has different odds
                self.dest_risk_status += 10
                self.overlay_update = True
                self.network_update = True


    def reset_fire_risk(self):
        if self.fire_risk > 0:
            self.fire_risk_status = 0
            self.overlay_update = True

    def reset_dest_risk(self):
        if self.dest_risk > 0:
            self.dest_risk_status = 0
            self.overlay_update = True

    def is_on_fire(self) -> bool:
        return self.fire_risk_status >= 100

    def is_destroyed(self) -> bool:
        return self.dest_risk_status >= 100

    def get_fire_status(self) -> int:
        return self.fire_risk_status

    def get_dest_status(self) -> int:
        return self.dest_risk_status

    def is_overlay_update(self):
        return self.overlay_update

    def is_network_update(self):
        return self.network_update

    def overlay_updated(self):
        self.overlay_update = False

    def network_updated(self):
        self.network_update = False

    def set_level(self, fire, damage):
        self.fire_risk_status = fire
        self.dest_risk_status = damage
        self.overlay_update = True