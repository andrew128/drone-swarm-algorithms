import sys
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from panda3d.core import Point3, Vec3, AmbientLight, DirectionalLight
from panda3d.core import loadPrcFileData
import random
import math

# Configure the window
loadPrcFileData("", """
    window-title Drone Simulation
    show-frame-rate-meter 1
    win-size 1280 720
""")

class DroneSimulation(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        # Set up the environment
        # self.setup_scene()
        # self.setup_lighting()
        # self.setup_camera()
        
        # Initialize drone parameters
        # self.num_drones = 5
        # self.drones = []
        # self.drone_speeds = []
        # self.drone_targets = []
        # self.create_drones()
        
        # Add update task
        # self.taskMgr.add(self.update, "update")
        
        # Set up keyboard controls
        # self.accept("escape", sys.exit)
        # self.accept("arrow_left", self.rotate_camera, [-1])
        # self.accept("arrow_right", self.rotate_camera, [1])
        
    def setup_scene(self):
        """Set up the basic environment"""
        # Load the ground plane
        self.ground = self.loader.loadModel("models/plane")
        self.ground.setScale(100, 100, 1)
        self.ground.setPos(0, 0, -5)
        self.ground.reparentTo(self.render)
        
        # Create some simple obstacles
        self.create_obstacles()
    
    def create_obstacles(self):
        """Create sample obstacles in the environment"""
        self.obstacles = []
        # Create a few sample buildings/obstacles
        for _ in range(5):
            obstacle = self.loader.loadModel("models/box")
            x = random.uniform(-50, 50)
            y = random.uniform(-50, 50)
            height = random.uniform(10, 30)
            obstacle.setPos(x, y, height/2)
            obstacle.setScale(5, 5, height)
            obstacle.reparentTo(self.render)
            self.obstacles.append(obstacle)
    
    def setup_lighting(self):
        """Set up basic lighting"""
        # Ambient light
        alight = AmbientLight('ambient')
        alight.setColor((0.3, 0.3, 0.3, 1))
        alnp = self.render.attachNewNode(alight)
        self.render.setLight(alnp)
        
        # Directional light (sun)
        dlight = DirectionalLight('directional')
        dlight.setColor((0.8, 0.8, 0.8, 1))
        dlnp = self.render.attachNewNode(dlight)
        dlnp.setHpr(45, -45, 0)
        self.render.setLight(dlnp)
    
    def setup_camera(self):
        """Set up the camera position"""
        self.camera.setPos(0, -100, 50)
        self.camera.lookAt(Point3(0, 0, 0))
    
    def create_drones(self):
        """Create the drone models"""
        for i in range(self.num_drones):
            # Create a simple drone model (using a sphere for now)
            drone = self.loader.loadModel("models/sphere")
            drone.setScale(0.5)
            drone.setPos(
                random.uniform(-20, 20),
                random.uniform(-20, 20),
                random.uniform(10, 30)
            )
            drone.reparentTo(self.render)
            
            # Set random initial speed
            speed = random.uniform(0.1, 0.3)
            
            # Set random initial target position
            target = Point3(
                random.uniform(-40, 40),
                random.uniform(-40, 40),
                random.uniform(10, 30)
            )
            
            self.drones.append(drone)
            self.drone_speeds.append(speed)
            self.drone_targets.append(target)
    
    def update(self, task):
        """Update drone positions and behavior"""
        dt = globalClock.getDt()
        
        for i, drone in enumerate(self.drones):
            # Get current position and target
            current_pos = drone.getPos()
            target_pos = self.drone_targets[i]
            
            # Calculate direction to target
            direction = target_pos - current_pos
            distance = direction.length()
            
            # If close to target, get new target
            if distance < 1:
                self.drone_targets[i] = Point3(
                    random.uniform(-40, 40),
                    random.uniform(-40, 40),
                    random.uniform(10, 30)
                )
            else:
                # Normalize direction and apply speed
                direction.normalize()
                new_pos = current_pos + direction * self.drone_speeds[i] * dt * 20
                
                # Basic collision avoidance with other drones
                for j, other_drone in enumerate(self.drones):
                    if i != j:
                        separation = new_pos - other_drone.getPos()
                        if separation.length() < 2:
                            new_pos += separation.normalize() * dt * 10
                
                drone.setPos(new_pos)
        
        return Task.cont
    
    def rotate_camera(self, direction):
        """Rotate the camera around the scene"""
        current_pos = self.camera.getPos()
        angle = math.pi / 60 * direction
        x = current_pos.getX() * math.cos(angle) - current_pos.getY() * math.sin(angle)
        y = current_pos.getX() * math.sin(angle) + current_pos.getY() * math.cos(angle)
        self.camera.setPos(x, y, current_pos.getZ())
        self.camera.lookAt(Point3(0, 0, 0))

# Create and run the simulation
sim = DroneSimulation()
sim.run()