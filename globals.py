import numpy as np # type: ignore
from parameters import pms
import pandas as pd

def init():
    global time
    global fsm,t_fsm

    time = 0
    fsm = np.array([pms.fsm_stand,pms.fsm_stand,pms.fsm_stand,pms.fsm_stand])
    t_fsm = np.zeros(4)

    #global lz0
    #global hcl

    #cartesian trajectory
    global t_i, t_f
    global lx_ref, ly_ref, lz_ref, lxdot_ref, lydot_ref, lzdot_ref
    global lx_i, lx_f, ly_i, ly_f, lz_i, lz_f

    t_i = np.zeros(4)
    t_f = np.array([pms.t_stand,pms.t_stand,pms.t_stand,pms.t_stand])
    lx_ref, ly_ref, lz_ref, lxdot_ref, lydot_ref, lzdot_ref = (np.zeros(4) for _ in range(6))
    lx_i, lx_f, ly_i, ly_f = (np.zeros(4) for _ in range(4))
    lz_i = np.array([pms.lz0,pms.lz0,pms.lz0,pms.lz0])
    lz_f = np.array([pms.lz0,pms.lz0,pms.lz0,pms.lz0])

    #joint traj
    global q_ref, u_ref

    q_ref,u_ref = (np.zeros(12) for _ in range(2))
    
    #joint control

    global q_act, u_act, trq
    
    q_act, u_act, trq = (np.zeros(12) for _ in range(3))

    global xdot_ref, ydot_ref

    xdot_ref = 0
    ydot_ref = 0

    global prev_step, step

    step = 0
    prev_step = 0

    # global zmp_x, zmp_y, is_stable
    # zmp_x = 0
    # zmp_y = 0
    # is_stable = True
    global com_x_ref,com_y_ref,com_xdot_ref,com_ydot_ref 
    com_x_ref = 0.0
    com_y_ref = 0.0
    com_xdot_ref = 0.0
    com_ydot_ref = 0.0

    global prev_com,prev_vel,prev_zmp_error_x,prev_zmp_error_y,zmp_x_ref,zmp_y_ref, stance_legs
    prev_com = None
    prev_vel = None
    prev_acc = None
    prev_com_error_x = 0
    prev_com_error_y = 0
    zmp_x_ref = 0.0  # Желаемый ZMP (можно обновлять в зависимости от фазы шага)
    zmp_y_ref = 0.0
    prev_zmp_error_x = 0.0
    prev_zmp_error_y = 0.0

    stance_legs = []  # Будет хранить индексы ног в фазе опоры

# # Создаём глобальный DataFrame для записи данных
# log_df = pd.DataFrame(columns=["timestamp", "com_x", "com_y", "com_z", "acc_x", "acc_y", "acc_z", "zmp_x", "zmp_y"])

# def log_data(tag, vec):
#     # Логируем время и данные
#     timestamp = globals.time  # допустим, время уже используется в глобальной переменной
#     data = {"timestamp": timestamp}
    
#     # Записываем данные для CoM, ускорения и ZMP
#     if tag == "CoM":
#         data.update({"com_x": vec[0], "com_y": vec[1], "com_z": vec[2]})
#     elif tag == "a_com":
#         data.update({"acc_x": vec[0], "acc_y": vec[1], "acc_z": vec[2]})
#     elif tag == "ZMP":
#         data.update({"zmp_x": vec[0], "zmp_y": vec[1]})
    
#     # Добавляем строку в DataFrame
#     global log_df
#     log_df = log_df.append(data, ignore_index=True)

#     print(f"{tag}: {vec}")

# def save_log_to_csv():
#     # Сохраняем DataFrame в CSV файл
#     log_df.to_csv("log_zmp_com.csv", index=False)