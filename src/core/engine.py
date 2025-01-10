import math

class Engine:
    def __init__(self, max_rpm=7000, friction=0.1, baseline_ratio=0.5):
        """
        Simulates an engine for dynamic sound modulation.
        :param max_rpm: Maximum RPM the engine can reach.
        :param friction: Deceleration rate due to "friction."
        :param baseline_ratio: Pedal position (0-1) that corresponds to zero acceleration.
        """
        self.max_rpm = max_rpm
        self.friction = friction
        self.baseline_ratio = baseline_ratio
        self.current_rpm = 0
        self.revs_forward = True  # If False, allows reverse "revving."

    def update_rpm(self, pedal_input):
        """
        Update the RPM based on pedal input.
        :param pedal_input: Float from 0 to 1, representing pedal position.
        """
        # Map pedal input to target RPM
        baseline_rpm = self.max_rpm * self.baseline_ratio
        if pedal_input >= self.baseline_ratio:
            target_rpm = baseline_rpm + (pedal_input - self.baseline_ratio) * (self.max_rpm - baseline_rpm)
        else:
            target_rpm = baseline_rpm * (pedal_input / self.baseline_ratio)

        # Reverse mode handling
        if not self.revs_forward and pedal_input < self.baseline_ratio:
            target_rpm = -target_rpm

        # Smooth transition to target RPM
        self.current_rpm += (target_rpm - self.current_rpm) * (1 - self.friction)

    def get_play_speed(self):
        """
        Get the current play speed as a fraction of normal speed.
        Positive values mean forward; negative values mean reverse.
        """
        return self.current_rpm / self.max_rpm
