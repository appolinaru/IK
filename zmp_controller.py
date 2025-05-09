import numpy as np
from forward_kinematics_leg import forward_kinematics_leg
from parameters import pms
import globals

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


prev_com = np.zeros(3)
prev_vel = np.zeros(3)

def get_com_acc(model, data):
    global prev_com, prev_vel, dt
    
    dt = model.opt.timestep 
    # 1) текущий CoM
    com = compute_com(model, data)      # [x_c, y_c, z_c]

    # 2) текущая скорость CoM
    vel = (com - prev_com) / dt         # [vx, vy, vz]

    # 3) ускорение CoM
    acc = (vel - prev_vel) / dt         # [ax, ay, az]

    # 4) обновляем буферы
    prev_com, prev_vel = com.copy(), vel.copy()

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
    (x_c, y_c, z_c), (xdd, ydd, zdd) = get_com_acc(model, data)
    g = pms.gravity

    x_zmp = x_c - (z_c / g) * xdd
    y_zmp = y_c - (z_c / g) * ydd
    return x_zmp, y_zmp

