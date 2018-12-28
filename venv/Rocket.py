from SolidMotor import SolidMotor
import math

class Rocket :

    def __init__(self, propulsionElements: [SolidMotor], dryMass: float):
        self.propulsionElements = propulsionElements
        self.dryMass = dryMass
        self.gimbal = (0,0)

    def getCurrentMass(self, currentTime: float):
        mass = self.dryMass
        for propulsionElement in self.propulsionElements:
            mass+=propulsionElement.getCurrentMass(currentTime)
        return mass

    def getCurrentThrustVector(self, currentTime: float):
        vector = (0,0,0)
        for propulsionElement in self.propulsionElements:
            if not propulsionElement.isThrustVectorable:
                z = propulsionElement.getCurrentThrust(currentTime)
                vector = (vector[0], vector[1], vector[2] + z)
            else:
                alpha = math.radians(self.gimbal[0])
                beta = math.radians(self.gimbal[1])
                magnitude = propulsionElement.getCurrentThrust(currentTime)
                x = magnitude * math.cos(alpha) * math.cos(beta)
                z = magnitude * math.sin(alpha) * math.cos(beta)
                y = magnitude * math.sin(beta)
                vector = (vector[0] + x, vector[1] + y, vector[2] + z)
        return vector

    def startMainEngine(self, currentTime: float):
        self.propulsionElements[0].ignite(currentTime)


from SolidMotor import SolidMotor
def test() :
    rocket = Rocket([SolidMotor(.043, .060, r"C:\Users\Mitchell\PycharmProjects\untitled\Estes_F15.eng", 2.79, True)])
    rocket.gimbal = [5,5]
    print(rocket.getCurrentThrustVector(.5))
