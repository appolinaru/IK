import numpy as np
from types import SimpleNamespace


def forward_kinematics_leg(q,leg_no):

    L = 0.2; #thigh and shank length
    
    if (leg_no==1 or leg_no==3): #Fl or RL
        w = 0.08505

    if (leg_no==0 or leg_no==2): #FR or RR
        w = -0.08505

    c1 = np.cos(q[0]); s1 = np.sin(q[0]);
    c2 = np.cos(q[1]); s2 = np.sin(q[1]);
    c3 = np.cos(q[2]); s3 = np.sin(q[2]);

    o01 = [0, 0, 0]; o12 = [0, w, 0]; o23 = [0, 0, -L];

    H01 = np.array([[1, 0, 0,     o01[0]],
                    [0, c1, -s1,  o01[1]],
                    [0, s1,  c1,  o01[2]],
                    [0,   0,  0, 1]])
    H12 = np.array([[ c2, 0, s2, o12[0]],
                    [0,  1,  0,  o12[1]],
                    [-s2, 0, c2, o12[2]],
                    [0,   0,  0, 1]])
    H23 = np.array([[ c3, 0, s3, o23[0]],
                    [0, 1,  0,   o23[1]],
                    [-s3,  0, c3, o23[2]],
                    [0,   0,  0, 1]])

    H02 = H01@H12
    H03 = H02@H23

    end_eff_pos_local = np.array([0,0,-L,1])
    end_eff_pos = H03@end_eff_pos_local
    end_eff_pos = end_eff_pos[0:3]
    #print(f"foot pos=",end_eff_pos)


    sol = SimpleNamespace(
        end_eff_pos=end_eff_pos,
        H01 = H01,
        H02 = H02,
        H03 = H03
        )
    

    return sol
# def forward_kinematics_leg(q, leg_no):
#     L = 0.2  # Длина бедра и голени
#     w = 0.08505 if (leg_no in [1,3]) else -0.08505
    
#     # Углы суставов
#     hip, thigh, knee = q
    
#     # Матрицы поворота (важно: порядок осей!)
#     R_hip = np.array([
#         [np.cos(hip), -np.sin(hip), 0],
#         [np.sin(hip), np.cos(hip),  0],
#         [0,           0,           1]
#     ])
    
#     R_thigh = np.array([
#         [np.cos(thigh),  0, np.sin(thigh)],
#         [0,             1,             0],
#         [-np.sin(thigh), 0, np.cos(thigh)]
#     ])
    
#     R_knee = np.array([
#         [np.cos(knee),  0, np.sin(knee)],
#         [0,            1,            0],
#         [-np.sin(knee), 0, np.cos(knee)]
#     ])

#     # Позиции суставов
#     p_hip = np.array([0, w, 0])
#     p_knee = p_hip + R_hip @ R_thigh @ np.array([0, 0, -L])
#     p_foot = p_knee + R_hip @ R_thigh @ R_knee @ np.array([0, 0, -L])

#     # Матрицы преобразования
#     H01 = np.eye(4); H01[:3,:3] = R_hip; H01[:3,3] = p_hip
#     H02 = np.eye(4); H02[:3,:3] = R_hip @ R_thigh; H02[:3,3] = p_knee
#     H03 = np.eye(4); H03[:3,:3] = R_hip @ R_thigh @ R_knee; H03[:3,3] = p_foot

#     return SimpleNamespace(
#         end_eff_pos=p_foot,
#         H01=H01, H02=H02, H03=H03,
#         joint_positions=[p_hip, p_knee, p_foot]
#     )