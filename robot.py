from abc import ABC, abstractmethod
import logging

logging.basicConfig(level=logging.INFO)

class InsufficientBatteryError(Exception):
    def __init__(self, name, required, available):
        message = f"{name} needs {required}% battery for this task but only has {available}%"
        super().__init__(message)
        self.name = name
        self.required = required
        self.available = available

class Robot(ABC):
    manufacturer = "Cyberdyne"
    population = 0

    def __init__(self, name, battery=100):
        self.name = name
        self.battery = battery
        Robot.population += 1

    @property
    def battery(self):
        return self._battery

    @battery.setter
    def battery(self, value):
        if value < 0:
            value = 0
        if value > 100:
            value = 100
        self._battery = value

    def __str__(self):
        return f"{self.name} ({self.battery}% battery)"

    def __repr__(self):
        return f"Robot(name={self.name!r}, battery={self.battery!r})"

    @classmethod
    def from_config(cls, config_dict):
        return cls(config_dict["name"], battery=config_dict.get("battery", 100))

    def use_battery(self, amount):
        if self.battery < amount:
            raise InsufficientBatteryError(self.name, amount, self.battery)
        self.battery -= amount

    @abstractmethod
    def perform_task(self, **kwargs):
        pass

class CleaningRobot(Robot):
    def __init__(self, name, battery=100, dust_capacity=500):
        super().__init__(name, battery)
        self.dust_capacity = dust_capacity
        self.dust_collected = 0

    def perform_task(self, **kwargs):
        battery_cost = 5
        self.use_battery(battery_cost)
        amount = kwargs.get("amount", 50)
        self.dust_collected = min(self.dust_capacity, self.dust_collected + amount)
        return f"Cleaned {amount} dust. Total: {self.dust_collected}"

class ProtocolRobot(Robot):
    def __init__(self, name, battery=100, languages=6000000):
        super().__init__(name, battery)
        self.languages = languages

    def perform_task(self, **kwargs):
        battery_cost = 15
        self.use_battery(battery_cost)
        target = kwargs.get("target", "human")
        return f"{self.name}: Translated communications for {target}."

def fleet_report(robots):
    for bot in robots:
        print(str(bot))

def run_task_safely(robot, **kwargs):
    try:
        result = robot.perform_task(**kwargs)
    except InsufficientBatteryError as e:
        logging.error(e)
    else:
        print(result)
    finally:
        print(f"{robot.name} battery: {robot.battery}%")