#!/usr/bin/env python3
"""Basic demo on how to control the Finger robot using a fake driver.

This script illustrates how to control a robot via the Python interface.  It
uses a fake driver, i.e. it can be executed without an actual robot.  The fake
driver will simply provide fake observations and ignore any actions that are
sent to it.
"""
import numpy as np

import robot_interfaces
import robot_fingers


def main():
    # Storage for all observations, actions, etc.
    # finger_data = robot_interfaces.finger.MultiProcessData("foo", True)
    finger_data = robot_interfaces.finger.SingleProcessData()

    # The backend sends actions from the data to the robot and writes
    # observations from the robot to the data.  Here we use a backend using the
    # "random finger driver" which just provides fake observations and does not
    # need an actual robot to be executed.
    fake_finger_backend = robot_fingers.create_fake_finger_backend(finger_data)

    # The frontend is used by the user to get observations and send actions
    finger = robot_interfaces.finger.Frontend(finger_data)

    # Initializes the robot (e.g. performs homing).
    fake_finger_backend.initialize()

    while fake_finger_backend.is_running():
        # Run a position controller that randomly changes the desired position
        # every 300 steps.
        # One time step corresponds to roughly 1 ms.

        desired_position = np.random.rand(3) * 6 - 1
        action = robot_interfaces.finger.Action(position=desired_position)
        for _ in range(300):
            # Appends a torque command ("action") to the action queue.
            # Returns the time step at which the action is going to be
            # executed.
            t = finger.append_desired_action(action)

            # Get observations of the time step t.  Will block and wait if t is
            # in the future.
            current_position = finger.get_observation(t).position

        # print current position from time to time
        print("Position: %s" % current_position)


if __name__ == "__main__":
    main()
