#!/usr/bin/env python3
"""Demo script for the TriFingerPro robot

Moves the TriFingerPro robot with a hard-coded choreography for show-casing and
testing.
"""
import argparse
import time
import numpy as np

import robot_interfaces
import robot_fingers


def run_choreography(frontend):
    """Move the legs in some hard-coded choreography."""

    def perform_step(position):
        # one step should take 1 second, so repeat action 1000 times
        for i in range(1000):
            t = frontend.append_desired_action(
                robot_interfaces.trifinger.Action(position=position))
            frontend.wait_until_timeindex(t)

    pose_initial = [0, 0.9, -1.7]
    pose_intermediate = [0.75, 1.2, -2.3]
    pose_up = [1.3, 1.5, -2.6]
    pose_other_side_up = [-0.8, 1.5, -1.7]

    last_time_print = 0

    while True:
        # initial pose
        perform_step(pose_initial * 3)
        perform_step(pose_intermediate * 3)
        perform_step(pose_up * 3)
        perform_step(pose_initial * 3)
        perform_step(pose_other_side_up * 3)

        # print current date/time every hour, so we can roughly see how long it
        # ran in case it crashes during a long-run-test.
        now = time.time()
        if (now - last_time_print > 3600):
            print(time.strftime("%F %T"))
            last_time_print = now


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--multi-process", action="store_true",
                        help="""If set run only frontend with multi-process
                        robot data.  Otherwise run everything within a single
                        process.""")
    parser.add_argument("--log", type=str)
    args = parser.parse_args()

    if args.multi_process:
        # In multi-process case assume that the backend is running in a
        # separate process and only set up the frontend here.
        robot_data = robot_interfaces.trifinger.MultiProcessData("trifinger",
                                                                 False)
        frontend = robot_interfaces.trifinger.Frontend(robot_data)
    else:
        # In single-process case run both frontend and backend in this process
        # (using the `Robot` helper class).
        robot = robot_fingers.Robot(robot_interfaces.trifinger,
                                    robot_fingers.create_trifinger_backend,
                                    "trifingerpro.yml")
        if args.log:
            logger = robot_interfaces.trifinger.Logger(robot.robot_data, 100)
            logger.start(args.log)

        robot.initialize()
        frontend = robot.frontend

    # move around
    run_choreography(frontend)


if __name__ == "__main__":
    main()

