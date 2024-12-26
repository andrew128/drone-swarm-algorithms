from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import Point3, loadPrcFileData

# Configure the window
loadPrcFileData("", """
    window-title Drone Simulation
    show-frame-rate-meter 1
    win-size 1280 720
""")

class DroneSimulation(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.setup_test_block()
        self.taskMgr.add(self.update, "UpdateScene")

    def update(self, task):
        """Keep the scene rendering with fixed camera position"""
        self.camera.setPos(0, -20, 3)
        self.camera.lookAt(0, 0, 0)
        return Task.cont
    
    def setup_test_block(self):
        self.test = self.loader.loadModel("box")
        self.test.setScale(1, 1, 1)
        self.test.setPos(0, 0, 0)
        self.test.reparentTo(self.render)

# Create and run the simulation
sim = DroneSimulation()
sim.run()