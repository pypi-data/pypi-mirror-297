"""
Python utilities used in CSC 201 at UT.
This file includes classes and methods related to logic gates.
"""

class LogicGate:
    """Defines a logic gate."""
    def __init__(self, label):
        self._label = label
        self._output = None

    """Performs the logic and returns the output."""
    def get_output(self):
        return self.perform_gate_logic()

class BinaryGate(LogicGate):
    """Defines a binary gate."""
    def __init__(self, label):
        super().__init__(label)
        self._pin_a = None
        self._pin_b = None

    """Returns the pin A input."""
    def get_pin_a(self):
        if (self._pin_a == None):
            raise RuntimeError("Error: NO PIN INPUT A")
        else:
            return self._pin_a.get_from().get_output()

    """Returns the pin B input."""
    def get_pin_b(self):
        if (self._pin_b == None):
            raise RuntimeError("Error: NO PIN INPUT B")
        else:
            return self._pin_b.get_from().get_output()

    """Sets an input pin."""
    def set_input_pin(self, source):
        if (self._pin_a == None):
            self._pin_a = source
        elif (self._pin_b == None):
            self._pin_b = source
        else:
            raise RuntimeError("Error: NO EMPTY PINS")

class UnaryGate(LogicGate):
    """Defines a unary gate."""
    def __init__(self, label):
        super().__init__(label)
        self._pin = None

    """Returns the pin input."""
    def get_pin(self):
        if (self._pin == None):
            raise RuntimeError("Error: NO PIN INPUT")
        else:
            return self._pin.get_from().get_output()

    """Sets the input pin."""
    def set_input_pin(self, source):
        if (self._pin == None):
            self._pin = source
        else:
            raise RuntimeError("Error: NO EMPTY PINS")

class AndGate(BinaryGate):
    """Defines an and gate."""
    def __init__(self, label):
        super().__init__(label)

    """Performs the logic and returns the output."""
    def perform_gate_logic(self):
        a = self.get_pin_a()
        b = self.get_pin_b()
        if (a == 1 and b == 1):
            return 1
        else:
            return 0

class OrGate(BinaryGate):
    """Defines an or gate."""
    def __init__(self, label):
        super().__init__(label)

    """Performs the logic and returns the output."""
    def perform_gate_logic(self):
        a = self.get_pin_a()
        b = self.get_pin_b()
        if (a == 1 or b == 1):
            return 1
        else:
            return 0

class NotGate(UnaryGate):
    """Defines a not gate."""
    def __init__(self, label):
        super().__init__(label)

    """Performs the logic and returns the output."""
    def perform_gate_logic(self):
        if (self.get_pin() == 0):
            return 1
        else:
            return 0

class Connector:
    """Defines a connector."""
    def __init__(self, from_gate, to_gate):
        self._from_gate = from_gate
        self._to_gate = to_gate

        to_gate.set_input_pin(self)

    """Returns the input gate."""
    def get_from(self):
        return self._from_gate

    """Returns the output gate."""
    def get_to(self):
        return self._to_gate

class Source:
    """Defines a source."""
    def __init__(self, label, output=None):
        self._label = label
        self._output = output

    """Returns the source's output."""
    def get_output(self):
        if (self._output == None):
            self._output = int(input(f"Enter pin input {self._label}: "))
        return self._output

