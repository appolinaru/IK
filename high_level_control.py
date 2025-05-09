import globals
import numpy as np
from parameters import pms
from set_command_step import set_command_step
#from zmp_controller import zmp_controller

def high_level_control():
    if(globals.prev_step < globals.step):
        globals.prev_step = globals.step

        vx = globals.xdot_ref
        vx_ = 2 #0.1 desired
        globals.xdot_ref = set_command_step(vx_, vx, pms.vx_min, pms.vx_max,pms.dvx)

        # vy = globals.ydot_ref
        # vy_ = 0.4 #desired
        # globals.ydot_ref = set_command_step(vy_, vy, pms.vy_min, pms.vy_max,pms.dvy)

# def high_level_control():
#     # Расчет ZMP и устойчивости
#     zmp_x, zmp_y = zmp_controller.calculate_zmp()
#     zmp_controller.calculate_support_polygon()
#     is_stable = zmp_controller.is_stable(zmp_x, zmp_y)
    
#     # Сохраняем данные для визуализации/отладки
#     globals.zmp_x = zmp_x
#     globals.zmp_y = zmp_y
#     globals.is_stable = is_stable
    
#     # Коррекция скорости на основе ZMP
#     if not is_stable:
#         # Уменьшаем скорость при потере устойчивости
#         globals.xdot_ref *= 0.8
#         globals.ydot_ref *= 0.8
    
#     if(globals.prev_step < globals.step):
#         globals.prev_step = globals.step
        
#         # Плавное изменение скорости с учетом устойчивости
#         desired_vx = 2 if is_stable else 0.1  # Пример адаптации
#         globals.xdot_ref = set_command_step(desired_vx, globals.xdot_ref, pms.vx_min, pms.vx_max, pms.dvx)