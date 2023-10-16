#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Libraries
import time    #https://docs.python.org/fr/3/library/time.html
from Robot import Robot
from datetime import datetime as dt
import numpy as np

# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# from matplotlib.animation import FuncAnimation
# from mpl_toolkits.mplot3d.art3d import Poly3DCollection  # appropriate import to draw 3d polygons

import cProfile


RAD = 0.0174532925

# function main 
def main():
    
    robot = Robot(11.25, 16.25)

    robot.reset_leg_positions()


    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')

    # def plot_line(p1, p2):
    #     ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]])

    # def update(num):
    #     robot.tick()

    #     ax.clear()

    #     # adding leg tips
    #     x = [robot.current_leg_positions[i][0] for i in range(len(robot.current_leg_positions))]
    #     y = [robot.current_leg_positions[i][1] for i in range(len(robot.current_leg_positions))]
    #     z = [robot.current_leg_positions[i][2] for i in range(len(robot.current_leg_positions))]

    #     # center of leg tips

    #     xsum = 0
    #     ysum = 0

    #     for i in range(6):
    #         xsum += x[i]
    #         ysum += y[i]

    #     # print(f"X IS\n{x}\n XSUM IS: {xsum}")
    #     # print(f"Y IS\n{y}\n YSUM IS: {ysum}")

    #     x.append(xsum)
    #     y.append(ysum)
    #     z.append(robot.WORKING_HEIGHT)

    #     # adding triangles
        
    #     verts = [list(zip([x[0], x[2], x[4]], [y[0], y[2], y[4]], [z[0], z[2], z[4]]))]
    #     srf = Poly3DCollection(verts, alpha=.25, facecolor='#800000')
    #     plt.gca().add_collection3d(srf)

    #     verts = [list(zip([x[1], x[3], x[5]], [y[1], y[3], y[5]], [z[1], z[3], z[5]]))]
    #     srf = Poly3DCollection(verts, alpha=.25, facecolor='#008000')
    #     plt.gca().add_collection3d(srf)

        # adding Body
        for i in range(6):
            x.append(robot.legs[i].hipPos[0])
        for i in range(6):
            y.append(robot.legs[i].hipPos[1])
        for i in range(6):
            z.append(robot.legs[i].hipPos[2])
    #     # adding Body
    #     for i in range(3):
    #         x.append(-robot.hip_x)
    #     for i in range(3):
    #         x.append(robot.hip_x)
    #     for i in range(2):
    #         y.append(robot.hip_y)
    #         y.append(0)
    #         y.append(-robot.hip_y)
    #     for i in range(6):
    #         z.append(0)

    #     # center of body on floor
    #     x.append(0)
    #     y.append(0)
    #     z.append(robot.WORKING_HEIGHT)

        # RECTANGULAR BOT

        # plot_line([-robot.hip_x, -robot.hip_y, 0], [robot.hip_x, -robot.hip_y, 0])
        # plot_line([robot.hip_x, -robot.hip_y, 0], [robot.hip_x, robot.hip_y, 0])
        # plot_line([robot.hip_x, robot.hip_y, 0], [-robot.hip_x, robot.hip_y, 0])
        # plot_line([-robot.hip_x, robot.hip_y, 0], [-robot.hip_x, -robot.hip_y, 0])

        plot_line(robot.legs[0].hipPos, robot.legs[1].hipPos)
        plot_line(robot.legs[1].hipPos, robot.legs[2].hipPos)
        plot_line(robot.legs[3].hipPos, robot.legs[4].hipPos)
        plot_line(robot.legs[4].hipPos, robot.legs[5].hipPos)

        plot_line(robot.legs[3].hipPos, robot.legs[0].hipPos)
        plot_line(robot.legs[2].hipPos, robot.legs[5].hipPos)
    #     plot_line([-robot.hip_x, -robot.hip_y, 0], [robot.hip_x, -robot.hip_y, 0])
    #     plot_line([robot.hip_x, -robot.hip_y, 0], [robot.hip_x, robot.hip_y, 0])
    #     plot_line([robot.hip_x, robot.hip_y, 0], [-robot.hip_x, robot.hip_y, 0])
    #     plot_line([-robot.hip_x, robot.hip_y, 0], [-robot.hip_x, -robot.hip_y, 0])

    #     #adding legs
    #     for i in range(6):
    #         pt1 = robot.legs[i].hipPos
    #         temp = robot.legs[i].COXA_LENGTH * np.array([np.sin(robot.servos[i][0] * RAD), -np.cos(robot.servos[i][0] * RAD), 0]) @ robot.legs[i].ROT_Z_MATRIX
    #         temp = temp.tolist()[0]
    #         pt2 = pt1 + temp
    #         plot_line(pt1, pt2)

    #         theta = -np.radians(robot.servos[i][0] - 90) + robot.legs[i].rest_angle
    #         c, s = np.cos(theta), np.sin(theta)
    #         R = np.matrix([[c, -s, 0], [s, c,0], [0,0,1]])

    #         temp = robot.legs[i].FEMUR_LENGTH * np.array([np.cos(np.pi/2 - robot.servos[i][1] * RAD), 0, -np.sin(np.pi/2 - robot.servos[i][1] * RAD)]) @ R
    #         temp = temp.tolist()[0]
    #         pt3 = pt2 + temp
    #         plot_line(pt2, pt3)

    #         temp = robot.legs[i].TIBIA_LENGTH * np.array([-np.cos((robot.servos[i][2]) * RAD + robot.servos[i][1] * RAD - np.pi/2), 0, -np.sin((robot.servos[i][2]) * RAD + robot.servos[i][1] * RAD - np.pi/2)]) @ R
    #         temp = temp.tolist()[0]
    #         pt4 = pt3 + temp
    #         plot_line(pt3, pt4)

    #     ax.scatter(x, y, z)
    #     ax.set_xlim(-30, 30)
    #     ax.set_ylim(-30, 30)
    #     ax.set_zlim(-30, 30)

    # ani = FuncAnimation(fig, update, frames=range(5), interval=5)

    # plt.show()


    """# h = -20
    # w = 20
    # l = 20

    # # i=0

    # for i in range(150):
    #     robot.move_leg_to_position(0, [-w+i/10, l, h])

    #     robot.move_leg_to_position(1, [-w+i/10, 0, h])

    #     robot.move_leg_to_position(2, [-w+i/10, -l, h])

    #     robot.move_leg_to_position(3, [w+i/10, l, h])

    #     robot.move_leg_to_position(4, [w+i/10, 0, h])

    #     robot.move_leg_to_position(5, [w+i/10, -l, h])
    #     time.sleep(0.02)

    # time.sleep(5)"""

    # for i in range(1000):
    #     robot.tick()

    while True:
        robot.tick()
        

    robot.loosen()

    # robot.move_leg_from_point_to_point(np.array[10, 10, -5], np.array(10, -10, -5), 3)

if __name__ == '__main__':

    # cProfile.run('main()')
    main()