from abc import ABC, abstractmethod
import logging
import functools

logging.basicConfig(level=logging.INFO)

def log_action(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        logging.info(f"Calling {func.__name__}")
        result = func(self, *args, **kwargs)
        logging.info(f"{func.__name__} finished")
        return result
    return wrapper

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
    
    #add the classmethod for config to bot
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

    @log_action
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

    @log_action
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

def demonstrate_mutable_class_attribute_trap():
    class BuggyRobot:
        logs = []  
        
        def __init__(self, name):
            self.name = name
            
        def add_log(self, entry):
            self.logs.append(entry)

    buggy1 = BuggyRobot("Bot1")
    buggy2 = BuggyRobot("Bot2")
    buggy1.add_log("Started up.")
    
    print(f"Buggy sharing: {buggy2.logs}") 

    class FixedRobot:
        def __init__(self, name):
            self.name = name
            self.logs = []  
            
        def add_log(self, entry):
            self.logs.append(entry)

    fixed1 = FixedRobot("Fix1")
    fixed2 = FixedRobot("Fix2")
    fixed1.add_log("Started up.")
    
    print(f"Fixed isolation: {fixed2.logs}")

if __name__ == "__main__":
    roomba = CleaningRobot("Roomba", battery=10)
    c3 = ProtocolRobot.from_config({"name": "C3", "battery": 100})
    
    fleet = [roomba, c3]
    fleet_report(fleet)
    
    run_task_safely(c3, target="rebel forces")
    run_task_safely(roomba, amount=100)
    run_task_safely(roomba, amount=20)