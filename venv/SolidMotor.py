import bisect
import numpy
import scipy

class SolidMotor:

    def __init__(self, dryMass: float, propellantMass: float, raspPath: str, ignitionDelay: float = 0, isThrustVectorable: bool = False):
        self.dryMass = dryMass
        self.propellantMass = propellantMass
        self.thrustDict : dict = loadRaspPath(raspPath)
        self.isThrustVectorable = isThrustVectorable
        self.ignitionDelay = ignitionDelay
        self.ignitionTime = -1

    def ignite(self, currentTime):
        self.ignitionTime = currentTime

    def getCurrentThrust(self, currentTime: float):
        burnTime = currentTime - (self.ignitionTime + self.ignitionDelay)
        if (burnTime <= 0):
            return 0
        else:
            return calculateThrustForTime(burnTime, self.thrustDict)

    def getCurrentMass(self, currentTime: float):
        elaspedBurnTime = currentTime - (self.ignitionTime + self.ignitionDelay)

        if(elaspedBurnTime >= 0):
            return self.dryMass + self.propellantMass

        totalBurnTime = list(self.thrustDict.keys())[len(self.thrustDict.keys()) - 1]
        # assume linear burn rate
        return self.dryMass + (self.propellantMass * (elaspedBurnTime / totalBurnTime))

def loadRaspPath(raspPath: str):
    string = open(raspPath).read()
    lines = string.split("\n")
    thrustDict = {}
    for line in lines:
        if (line.startswith(";")):
            continue
        else:
            words = line.split(" ")
            try:
                thrustDict.update({float(words[0]): float(words[1])})
            except ValueError:
                continue
    return thrustDict


def calculateThrustForTime(burnTime: float, thrusts: [{float, float}]):
    measurementTimes = list(thrusts.keys())
    lastMeasurementTimeIndex = bisect.bisect_left(measurementTimes,burnTime)
    nextMeasurementTimeIndex = lastMeasurementTimeIndex + 1

    if(nextMeasurementTimeIndex == len(thrusts)):
        return 0
    if(lastMeasurementTimeIndex == len(thrusts)):
        return 0

    lastMeasurementTime = measurementTimes[lastMeasurementTimeIndex]
    nextMeasurementTime = measurementTimes[nextMeasurementTimeIndex]

    lastThrust = 0
    nextThrust = 0
    if (lastMeasurementTime == None):
        lastMeasurementTime = 0
        lastThrust = 0
    elif(lastMeasurementTime > burnTime) :
        nextThrust = thrusts[lastMeasurementTime]
        nextMeasurementTime = lastMeasurementTime
        lastMeasurementTime = 0
    else:
        lastThrust = thrusts[lastMeasurementTime]

    nextThrust = thrusts[nextMeasurementTime]

    m = slope(lastMeasurementTime, lastThrust, nextMeasurementTime, nextThrust)
    b = intercept(lastMeasurementTime, lastThrust, nextMeasurementTime, nextThrust)

    return m * burnTime + b

def slope(x1, y1, x2, y2):
    return (y2-y1)/(x2-x1)

def intercept(x1, y1, x2, y2):   # y1 = mx1 + q -> q = y1 - mx1
    m = slope(x1, y1, x2, y2)
    q = y1 - m * x1
    return q
