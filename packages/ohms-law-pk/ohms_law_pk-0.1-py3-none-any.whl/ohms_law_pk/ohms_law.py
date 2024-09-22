# program calculates ohms law with user inputs

class Drive:
    def __init__(self):
        pass

def calcvoltage(current, resistance):
    """
    Returns Current * Resistace
    """

    return current * resistance
    
def calcCurrent(voltage, resistance):
    """
    Retrns voltage / Resistace
    """

    return voltage / resistance
    
def calcresitance(voltage, current):
    """
    Returns Voltage / Current
    """

    return voltage / current
    