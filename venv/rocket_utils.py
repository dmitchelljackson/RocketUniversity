from rocket import Rocket
from solid_motor import SolidMotor
import pybullet as p


def createRocket(propulsionElements: [SolidMotor], dryMass: float, centerOfGravityZOffsetPercentage: float, startLocation: tuple) :
    visualShift = [0, 0, 0]
    collisionShift = [0, 0, 0]
    inertiaShift = [0, 0, centerOfGravityZOffsetPercentage]

    meshScale = [.1, .1, 1]
    visualShapeId = p.createVisualShape(shapeType=p.GEOM_MESH, fileName="cube.obj", rgbaColor=[1, 1, 1, 1],
                                        specularColor=[0.4, .4, 0], visualFramePosition=visualShift,
                                        meshScale=meshScale)
    collisionShapeId = p.createCollisionShape(shapeType=p.GEOM_MESH, fileName="cube.obj",
                                              collisionFramePosition=collisionShift, meshScale=meshScale)

    boxId = p.createMultiBody(baseMass=1, baseInertialFramePosition=inertiaShift,
                              baseCollisionShapeIndex=collisionShapeId, baseVisualShapeIndex=visualShapeId,
                              basePosition=startLocation, useMaximalCoordinates=False)

    rocket = Rocket(propulsionElements, dryMass)

    return boxId, rocket


def createTestRocket(startPosition: tuple):
    motor = SolidMotor(.043, .060, r"C:\Users\Mitchell\PycharmProjects\untitled\Estes_F15.eng", 1, True)
    return createRocket([motor], .988, -.33, startPosition)
