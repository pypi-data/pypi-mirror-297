def calcVoltage(current, resistance):
    # Returns current * resistance
    return current * resistance
    
def calcCurrent(voltage, resistance):
    # Returns voltage / resistance
    return voltage / resistance
    
def calcResistance(voltage, current):
    # Returns voltage / current
    return voltage / current

class Drive:
    def __init__(self):
        pass