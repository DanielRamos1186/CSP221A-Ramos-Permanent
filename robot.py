from abc import ABC, abstractmethod

class Robot(ABC):
    manufacturer = "Cyberdyne"
    population = 0

    def __init__(self, name, battery=100):
        self.name = name
        self.battery = battery
        Robot.population += 1