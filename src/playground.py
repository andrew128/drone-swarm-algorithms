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
        self.setup_drones()
        self.taskMgr.add(self.update, "UpdateScene")

    def update(self, task):
        """Keep the scene rendering with fixed camera position"""
        self.camera.setPos(0, -20, 3)
        self.camera.lookAt(0, 0, 0)
        return Task.cont
    
    def setup_drones(self):
        # Create 5 drones in a line along the X axis
        self.drones = []
        spacing = 3  # Units between each drone
        
        for i in range(5):
            drone = self.loader.loadModel("box")
            drone.setScale(1, 1, 1)
            # Position each drone 3 units apart
            drone.setPos((i - 2) * spacing, 0, 0)  # Centered around 0
            drone.reparentTo(self.render)
            self.drones.append(drone)

# Create and run the simulation
sim = DroneSimulation()
sim.run()