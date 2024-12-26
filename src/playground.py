from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import Point3, loadPrcFileData
from abc import ABC, abstractmethod

# Abstract base class for movement algorithms
class DroneAlgorithm(ABC):
    @abstractmethod
    def update(self, drones, dt, time):
        """Update drone positions according to algorithm"""
        pass
    
    @abstractmethod
    def get_name(self):
        """Return algorithm name"""
        pass

# Example implementations
class LineFormation(DroneAlgorithm):
    def update(self, drones, dt, time):
        spacing = 3
        for i, drone in enumerate(drones):
            target = Point3((i - 2) * spacing, 0, 0)
            current_pos = drone.getPos()
            direction = target - current_pos
            if direction.length() > 0.1:
                direction.normalize()
                new_pos = current_pos + (direction * dt)
                drone.setPos(new_pos)
    
    def get_name(self):
        return "Line Formation"

class WaveMotion(DroneAlgorithm):
    def update(self, drones, dt, time):
        import math
        for i, drone in enumerate(drones):
            pos = drone.getPos()
            offset = math.sin(time * 2.0 + i * 0.5) * 0.5
            drone.setPos(pos.x, pos.y, 2 + offset)
    
    def get_name(self):
        return "Wave Motion"

class CircleFormation(DroneAlgorithm):
    def update(self, drones, dt, time):
        import math
        radius = 5
        for i, drone in enumerate(drones):
            angle = (i / len(drones)) * 2 * math.pi
            target = Point3(
                radius * math.cos(angle),
                radius * math.sin(angle),
                2
            )
            current_pos = drone.getPos()
            direction = target - current_pos
            if direction.length() > 0.1:
                direction.normalize()
                new_pos = current_pos + (direction * dt)
                drone.setPos(new_pos)
    
    def get_name(self):
        return "Circle Formation"

class DroneSimulation(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.setup_drones()
        self.setup_algorithms()
        self.time = 0
        self.taskMgr.add(self.update, "UpdateScene")
        self.accept("1", self.set_algorithm, [0])  # Bind key "1" to first algorithm
        self.accept("2", self.set_algorithm, [1])  # Bind key "2" to second algorithm
        self.accept("3", self.set_algorithm, [2])  # Bind key "3" to third algorithm

    def setup_algorithms(self):
        self.algorithms = [
            LineFormation(),
            WaveMotion(),
            CircleFormation()
        ]
        self.current_algorithm = self.algorithms[0]
        print("Available Algorithms:")
        for i, algo in enumerate(self.algorithms):
            print(f"{i + 1}: {algo.get_name()}")

    def set_algorithm(self, index):
        if 0 <= index < len(self.algorithms):
            self.current_algorithm = self.algorithms[index]
            print(f"Switched to: {self.current_algorithm.get_name()}")

    def update(self, task):
        """Update scene and drone positions"""
        self.camera.setPos(0, -20, 3)
        self.camera.lookAt(0, 0, 0)
        
        dt = globalClock.getDt()
        self.time += dt
        
        # Update drones using current algorithm
        self.current_algorithm.update(self.drones, dt, self.time)
        
        return Task.cont

    def setup_drones(self):
        self.drones = []
        spacing = 3
        
        for i in range(5):
            drone = self.loader.loadModel("box")
            drone.setScale(1, 1, 1)
            drone.setPos((i - 2) * spacing, 0, 0)
            drone.reparentTo(self.render)
            self.drones.append(drone)

# Create and run the simulation
sim = DroneSimulation()
sim.run()