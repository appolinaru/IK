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
    
    global com_x_ref,com_y_ref,com_xdot_ref,com_ydot_ref,com_z_ref 
    com_z_ref = 0.0 
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

    global com_error_integral_y,com_error_integral_x
    com_error_integral_y = 0
    com_error_integral_x = 0
    stance_legs = []  # Будет хранить индексы ног в фазе опоры
