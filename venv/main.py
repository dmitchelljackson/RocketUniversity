import pybullet as p
import time
import pybullet_data
import pybullet_utils
from SolidMotor import SolidMotor
from Rocket import Rocket

frameSize = 1./240

physicsClient = p.connect(p.GUI)#or p.DIRECT for non-graphical version
p.setAdditionalSearchPath(pybullet_data.getDataPath()) #optionally
p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")

visualShift = [0,0,0]
collisionShift = [0,0,0]
inertiaShift = [0,0,-.25]
startPos = [0,0,42.5]

meshScale=[.1,.1,1]
visualShapeId = p.createVisualShape(shapeType=p.GEOM_MESH,fileName="cube.obj", rgbaColor=[1,1,1,1], specularColor=[0.4,.4,0], visualFramePosition=visualShift, meshScale=meshScale)
collisionShapeId = p.createCollisionShape(shapeType=p.GEOM_MESH, fileName="cube.obj", collisionFramePosition=collisionShift,meshScale=meshScale)

boxId = p.createMultiBody(baseMass=1,baseInertialFramePosition=inertiaShift,baseCollisionShapeIndex=collisionShapeId, baseVisualShapeIndex = visualShapeId, basePosition = startPos, useMaximalCoordinates=False)

motor = SolidMotor(.043 + .988, .060, r"C:\Users\Mitchell\PycharmProjects\untitled\Estes_F15.eng", 2.79)

currentTime = 0.
motor.ignite(currentTime)

for i in range (10000) :
    newMass = motor.getCurrentMass(currentTime)
    p.changeDynamics(boxId, -1,newMass)
    thrust = motor.getCurrentThrust(currentTime)
    position = p.getBasePositionAndOrientation(boxId)
    if(thrust != 0) :
        p.applyExternalForce(boxId, -1, [0,0,thrust], [0,0,0], 2)
    p.stepSimulation()
    time.sleep(frameSize)
    currentTime+=frameSize

p.disconnect()


def printInfo(position, mass: float, thrust: float):
    print( "Position: ")
    print(position)
    print("Mass: ")
    print(mass)
    print("Thrust:")
    print(thrust)