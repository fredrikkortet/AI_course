# Make sure to have the server side running in V-REP:
# in a child script of a V-REP scene, add following command
# to be executed just once, at simulation start:
#
# simExtRemoteApiStart(19999)
# then start simulation, and run this program.
#
# IMPORTANT: for each successful call to simxStart, there
# should be a corresponding call to simxFinish at the end!
import Lab1_Agents_Task1_World as World
import random
# connect to the server
robot = World.init()
memory = {"stuck":False,"distance":0.0,"time":0}
# print important parts of the robot
print(sorted(robot.keys()))
def standard(simulationTime):
    motorSpeed = dict(speedLeft=0, speedRight=0)
    if simulationTime<5000:
        motorSpeed = dict(speedLeft=1, speedRight=1.5)
    elif simulationTime<10000:
        motorSpeed = dict(speedLeft=-1.5, speedRight=-1.0)
    elif simulationTime<15000:
        print ("Turning for a bit...",)
        World.execute(dict(speedLeft=2, speedRight=-2),15000,-1)
        print ("... got dizzy, stopping!")
        print ("BTW, nearest energy block is at:",World.getSensorReading("energySensor"))
    else:
        motorSpeed = dict(speedLeft=0, speedRight=0)
    return motorSpeed

def rand():
    motorSpeed = dict(speedLeft=random.randint(-1000,1000), speedRight=random.randint(-1000,1000))
    return motorSpeed

def fixed(simulationTime):
    motorSpeed = dict(speedLeft=0, speedRight=0)
    if simulationTime<28000:
        motorSpeed = dict(speedLeft=2, speedRight=2)
        World.collectNearestBlock()
    elif simulationTime<30600:
        motorSpeed = dict(speedLeft=-1,speedRight=1)
        World.collectNearestBlock()
    elif simulationTime<58000:
        motorSpeed = dict(speedLeft=2, speedRight=2)
        World.collectNearestBlock()
    else:
        motorSpeed = dict(speedLeft=0, speedRight=0)
    return motorSpeed

def reflex():
    World.collectNearestBlock()
    motorSpeed = dict(speedLeft=3,speedRight=3)
    if  float(World.getSensorReading("ultraSonicSensorLeft"))< 0.4:
        motorSpeed = dict(speedLeft=3,speedRight=1)
        if float(World.getSensorReading("ultraSonicSensorRight")) < 0.4:
            motorSpeed = dict(speedLeft=0,speedRight=-3)
    elif float(World.getSensorReading("ultraSonicSensorRight")) < 0.4:
        motorSpeed = dict(speedLeft=1,speedRight=3)
    return motorSpeed

def mem(simulationTime):
    energy = World.getSensorReading("energySensor")
    left = float(World.getSensorReading("ultraSonicSensorLeft"))
    right = float(World.getSensorReading("ultraSonicSensorRight"))
    motorSpeed =dict(speedLeft=2,speedRight=2)
    if energy.distance < 0.4:
        World.collectNearestBlock()
        memory["time"]=simulationTime
    if memory["time"]+15000<simulationTime:
        memory["stuck"]= not memory["stuck"]
        memory["time"]=simulationTime
        print("changed")
    if memory["stuck"]:
        motorSpeed=reflex()
    else:
        if energy.direction < -0.3 or  energy.direction > 0.3:
            if energy.direction < -0.3:
                motorSpeed = dict(speedLeft=-1,speedRight=1)
            else:
                motorSpeed = dict(speedLeft=1, speedRight=-1)
        if right < 0.3:
            motorSpeed=dict(speedLeft=1,speedRight=-1)
        elif left < 0.3:
            motorSpeed=dict(speedLeft=-1,speedRight=0)
    return motorSpeed

def test():
    energy = World.getSensorReading("energySensor")
    left = World.getSensorReading("ultraSonicSensorLeft")
    right = World.getSensorReading("ultraSonicSensorRight")
    robotdir = float(World.robotDirection())
    motorSpeed = dict(speedLeft=1, speedRight=-1)
    print("energy: ",energy,"\n leftdir: ",left,"\n rightdir: ",right,"\n robotdir: ",robotdir, "\n Blocks: ",World.findEnergyBlocks())
    return motorSpeed
while robot: # main Control loop
    #######################################################
    # Perception Phase: Get Vinformation about environment #
    #######################################################
    simulationTime = World.getSimulationTime()
    if simulationTime%1000==0:
        # print some useful info, but not too often
        print ('Time:',simulationTime,\
               'ultraSonicSensorLeft:',World.getSensorReading("ultraSonicSensorLeft"),\
               "ultraSonicSensorRight:", World.getSensorReading("ultraSonicSensorRight"))
    ##############################################
    # Reasoning: figure out which action to take #
    ##############################################
    #motorSpeed = standard(simulationTime)
    #motorSpeed = rand()
    #motorSpeed = fixed(simulationTime)
    #motorSpeed = reflex()
    motorSpeed = mem(simulationTime)
    #motorSpeed = test()
    ########################################
    # Action Phase: Assign speed to wheels #
    ########################################
    # assign speed to the wheels
    World.setMotorSpeeds(motorSpeed)
    # try to collect energy block (will fail if not within range)
    if simulationTime%10000==0:
        print ("Trying to collect a block...",World.collectNearestBlock())
