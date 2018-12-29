from solid_motor import SolidMotor
import math


class Rocket:

    def __init__(self, propulsionElements: [SolidMotor], dryMass: float):
        self.propulsionElements = propulsionElements
        self.dryMass = dryMass
        self.gimbal = (0, 0)

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
                alpha = math.radians(self.gimbal[0] * -1)
                beta = math.radians(self.gimbal[1] * -1)
                magnitude = propulsionElement.getCurrentThrust(currentTime)
                z = magnitude * math.cos(alpha) * math.cos(beta)
                x = magnitude * math.sin(alpha) * math.cos(beta)
                y = magnitude * math.sin(beta)
                vector = (vector[0] + x, vector[1] + y, vector[2] + z)
                print(vector)
        return vector

    def startMainEngine(self, currentTime: float):
        self.propulsionElements[0].ignite(currentTime)



