import numpy as np
import utility as ram
from forward_kinematics_leg import forward_kinematics_leg

def jac_end_effector_leg(q,leg_no):
    sol = forward_kinematics_leg(q,leg_no)

    #get the output
    end_eff_pos = sol.end_eff_pos
    H01 = sol.H01
    H02 = sol.H02
    H03 = sol.H03

    #end-effector position
    e0 = end_eff_pos

    #frame origin
    o01 = H01[0:3,3]
    o02 = H02[0:3,3]
    o03 = H03[0:3,3]

    #joint axis
    n1 = np.array([1,0,0])
    n2 = np.array([0,1,0])
    n3 = np.array([0,1,0])


    #rotation matrix
    R00 = np.eye(3)
    R01 = H01[0:3,0:3]
    R02 = H02[0:3,0:3]
    R03 = H03[0:3,0:3]

    #jacobians
    Jv_E = np.column_stack([
                     ram.vec2skew(R00 @ n1) @ (e0-o01), \
                     ram.vec2skew(R01 @ n2) @ (e0-o02), \
                     ram.vec2skew(R02 @ n3) @ (e0-o03),
                     ])


    return Jv_E
    # sol = forward_kinematics_leg(q, leg_no)
    # p_foot = sol.end_eff_pos
    # p_hip, p_knee, _ = sol.joint_positions

    # # Оси вращения в мировых координатах
    # z_hip = np.array([0, 0, 1])  # Бедро - ось Z
    # z_knee = sol.H01[:3,:3] @ np.array([0, 1, 0])  # Колено - ось Y
    # z_ankle = sol.H02[:3,:3] @ np.array([0, 1, 0])  # Голень - ось Y

    # # Якобиан
    # J = np.column_stack([
    #     np.cross(z_hip, p_foot - p_hip),   # Бедро
    #     np.cross(z_knee, p_foot - p_knee), # Колено
    #     np.cross(z_ankle, p_foot - p_knee) # Голень
    # ])
    
    # return J

