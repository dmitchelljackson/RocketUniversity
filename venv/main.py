import pybullet as p
import time
import pybullet_data
import pybullet_utils
import Rocket
from rocket import Rocket
from rocket_utils import createTestRocket

frameSize = 1./240

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.8)

planeId = p.loadURDF("plane.urdf")

startPos = [0, 0, 3]
boxId, rocket = createTestRocket(startPos)

currentTime = 0.
rocket.startMainEngine(currentTime)

for i in range(10000):
    newMass = rocket.getCurrentMass(currentTime)
    p.changeDynamics(boxId, -1, newMass)
    thrust = rocket.getCurrentThrustVector(currentTime)
    position = p.getBasePositionAndOrientation(boxId)
    if thrust != 0:
        p.applyExternalForce(boxId, -1, thrust, [0, 0, 0], 2)
    p.stepSimulation()
    time.sleep(frameSize * 5)
    currentTime += frameSize

p.disconnect()


def printInfo(position, mass: float, thrust: float):
    print("Position: ")
    print(position)
    print("Mass: ")
    print(mass)
    print("Thrust:")
    print(thrust)