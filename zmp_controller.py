import numpy as np
from forward_kinematics_leg import forward_kinematics_leg
from parameters import pms
import globals 
import pandas as pd

# def zmp_controller(q):
#     """
#     Вычисление позиции ZMP на основе положения ног (опорных точек)
#     и коррекции позиции CoM.
#     """
#     # Получаем позиции ног
#     foot_positions = []
#     for leg_no in range(4):
#         q_leg = np.array([q[3*leg_no], q[3*leg_no+1], q[3*leg_no+2]])
#         pos = forward_kinematics_leg(q_leg, leg_no).end_eff_pos
#         foot_positions.append(pos)

#     # Преобразуем в массив
#     foot_positions = np.array(foot_positions)

#     # Среднее положение ног (псевдосредний CoM)
#     com_x = np.mean(foot_positions[:, 0])
#     com_y = np.mean(foot_positions[:, 1])

#     # Коэффициенты для ZMP расчета (это примерные коэффициенты, которые могут зависеть от модели робота)
#     gravity = pms.gravity  # Ускорение свободного падения
#     total_mass = pms.mass  # Общая масса робота
#     foot_height = pms.hcl  # Высота ног от земли (это пример, зависит от робота)

#     # Моменты от сил тяжести, вычисляем ZMP
#     zmp_x = com_x - (foot_height * (com_x / foot_height))  # Коррекция по оси X
#     zmp_y = com_y - (foot_height * (com_y / foot_height))  # Коррекция по оси Y

#     return zmp_x, zmp_y


time_history = []
com_history = []
zmp_history = []

def get_com_acc(model, data):

    global dt
    
    dt = model.opt.timestep 
    # 1) текущий CoM
    com = compute_com(model, data)      # [x_c, y_c, z_c]

    if globals.prev_com is None:
        globals.prev_com = com.copy()
        globals.prev_vel = np.zeros(3)
        return com, np.zeros(3)
    # vel = (com - globals.prev_com) / dt
    # acc = (vel - globals.prev_vel) / dt
    alpha = 0.2  # сглаживание (чем меньше, тем плавнее)
    vel = alpha * (com - globals.prev_com) / dt + (1 - alpha) * globals.prev_vel
    acc = alpha * (vel - globals.prev_vel) / dt + (1 - alpha) * (globals.prev_acc if hasattr(globals, 'prev_acc') else np.zeros(3))
    globals.prev_com = com.copy()
    globals.prev_vel = vel.copy()


    return com, acc

def compute_com(model, data):
    total_mass = 0.0
    weighted_pos = np.zeros(3)

    for i in range(model.nbody):
        if i == 0:
            continue  # пропускаем "world" body

        mass = model.body_mass[i]
        pos = data.xipos[i]  # позиция центра масс тела i в мировых координатах

        weighted_pos += mass * pos
        total_mass += mass

    com = weighted_pos / total_mass
    return com

def zmp_controller(model, data):
    com, acc = get_com_acc(model, data)
    g = pms.gravity

    x_zmp = com[0] - (com[2] / g) * acc[0]
    y_zmp = com[1] - (com[2] / g) * acc[1]

    # globals.log_data("CoM", com)
    # globals.log_data("a_com", acc)
    # globals.log_data("ZMP", (x_zmp, y_zmp))

    # # Сохраняем данные в CSV (например, каждую секунду или по событию)
    # globals.save_log_to_csv()

    zmp = (x_zmp, y_zmp, 0)  # Добавляем нулевую Z-координату для единообразия

    # Сохраняем данные
    time_history.append(data.time)
    com_history.append(com)
    zmp_history.append(zmp)
    return x_zmp, y_zmp

def save_data_to_csv():
    # Создаем DataFrame с временем, CoM и ZMP
    data_dict = {
        'time': time_history,
        'com_x': [com[0] for com in com_history],
        'com_y': [com[1] for com in com_history],
        'com_z': [com[2] for com in com_history],
        'zmp_x': [zmp[0] for zmp in zmp_history],
        'zmp_y': [zmp[1] for zmp in zmp_history]
    }
    
    df = pd.DataFrame(data_dict)
    df.to_csv('motion_data.csv', index=False)
    print("Данные сохранены в motion_data.csv")