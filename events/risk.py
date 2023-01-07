import random as rd

class Risk:
    def __init__(self, fire_risk, dest_risk):
        self.fire_risk = fire_risk
        self.dest_risk = dest_risk
        self.fire_risk_status = 0 if fire_risk else -1
        self.dest_risk_status = 0 if dest_risk else -1
        self.update = False


    def risk_progress(self):
        if 0 <= self.fire_risk_status < 100:     #risk increases as soon as the building is created

            if rd.randint(0, 100) < self.fire_risk:      #every type of building has different odds
                self.fire_risk_status += 10
                self.update = True


        if 0 <= self.dest_risk_status < 100:  # risk increases as soon as the building is created

            if rd.randint(0, 100) < self.dest_risk:  # every type of building has different odds
                self.dest_risk_status += 10
                self.update = True


    def reset_fire_risk(self):
        if self.fire_risk > 0:
            self.fire_risk_status = 0

    def reset_dest_risk(self):
        if self.dest_risk > 0:
            self.dest_risk_status = 0

    def is_on_fire(self) -> bool:
        return self.fire_risk_status >= 100

    def is_destroyed(self) -> bool:
        return self.dest_risk_status >= 100

    def get_fire_status(self) -> int:
        print(self.fire_risk_status)
        return self.fire_risk_status

    def get_dest_status(self) -> int:
        return self.dest_risk_status

    def is_update(self):
        return self.update

    def updated(self):
        self.update = False