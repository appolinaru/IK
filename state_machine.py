import globals
from parameters import pms

def state_machine():

    time = globals.time
    #print(globals.time)
    #print(globals.fsm)
    fsm_stand = pms.fsm_stand
    fsm_stance = pms.fsm_stance
    fsm_swing = pms.fsm_swing

    t_stand = pms.t_stand
    t_step = pms.t_step



    for leg_num in range(4):
        if(time >= globals.t_fsm[leg_num]+ t_stand and globals.fsm[leg_num]==fsm_stand):
            if(leg_num == 0 or leg_num == 3):
                globals.fsm[leg_num] = fsm_swing
                globals.t_fsm[leg_num] = time

                globals.t_i[leg_num] = 0
                globals.t_f[leg_num] = t_step
                globals.lz_i[leg_num] = pms.lz0 
                globals.lz_f[leg_num] = pms.lz0 + pms.hcl

            if(leg_num == 1 or leg_num == 2):
                globals.fsm[leg_num] = fsm_stance
                globals.t_fsm[leg_num] = time

                globals.t_i[leg_num] = 0
                globals.t_f[leg_num] = t_step
                globals.lz_i[leg_num] = pms.lz0
                globals.lz_f[leg_num] = pms.lz0

        if(time >= globals.t_fsm[leg_num]+ t_step and globals.fsm[leg_num]==fsm_stance):
            globals.fsm[leg_num] = fsm_swing
            globals.t_fsm[leg_num] = time
            globals.t_i[leg_num] = 0
            globals.t_f[leg_num] = t_step
            globals.lz_i[leg_num] = pms.lz0
            globals.lz_f[leg_num] = pms.lz0+pms.hcl

            globals.lx_i[leg_num] = -0.5*globals.xdot_ref * t_step
            globals.lx_f[leg_num] = 0.5*globals.xdot_ref * t_step
            globals.ly_i[leg_num] = -0.5*globals.ydot_ref * t_step
            globals.ly_f[leg_num] = 0.5*globals.ydot_ref * t_step

        if(time >= globals.t_fsm[leg_num]+ t_step and globals.fsm[leg_num]==fsm_swing):
            if (leg_num == 0 or leg_num == 1):
                globals.step+=1
            globals.fsm[leg_num] = fsm_stance
            globals.t_fsm[leg_num] = time
            globals.t_i[leg_num] = 0
            globals.t_f[leg_num] = t_step
            globals.lz_i[leg_num] = pms.lz0
            globals.lz_f[leg_num] = pms.lz0

            globals.lx_i[leg_num] = 0.5*globals.xdot_ref * t_step
            globals.lx_f[leg_num] = -0.5*globals.xdot_ref * t_step
            globals.ly_i[leg_num] = 0.5*globals.ydot_ref * t_step
            globals.ly_f[leg_num] = -0.5*globals.ydot_ref * t_step
# def state_machine():
#     time = globals.time
#     gait = pms.gaits[pms.current_gait]
#     phase_duration = gait["phase_duration"]
    
#     # Определяем текущую фазу (0 → 1 → 2 → 3 → 0...)
#     total_phases = len(gait["phase_order"])
#     current_phase_index = int((time // phase_duration) % total_phases)
#     active_leg = gait["phase_order"][current_phase_index][0]  # Текущая нога в swing

#     for leg_num in range(4):
#         # Для активной ноги (swing)
#         if leg_num == active_leg:
#             if globals.fsm[leg_num] != pms.fsm_swing:  # Если ещё не в swing
#                 globals.fsm[leg_num] = pms.fsm_swing
#                 globals.t_fsm[leg_num] = time
#                 globals.t_i[leg_num] = 0
#                 globals.t_f[leg_num] = phase_duration
#                 globals.lz_i[leg_num] = pms.lz0 
#                 globals.lz_f[leg_num] = pms.lz0 + pms.hcl
                
#                 # Установка начальных/конечных позиций для движения
#                 globals.lx_i[leg_num] = -0.5 * globals.xdot_ref * phase_duration
#                 globals.lx_f[leg_num] = 0.5 * globals.xdot_ref * phase_duration
#                 globals.ly_i[leg_num] = -0.5 * globals.ydot_ref * phase_duration
#                 globals.ly_f[leg_num] = 0.5 * globals.ydot_ref * phase_duration
        
#         # Для неактивных ног (stance)
#         else:
#             if globals.fsm[leg_num] == pms.fsm_swing:
#                 # Проверяем, завершила ли нога swing-фазу
#                 if time >= globals.t_fsm[leg_num] + phase_duration:
#                     globals.fsm[leg_num] = pms.fsm_stance
#                     globals.t_fsm[leg_num] = time
#                     globals.t_i[leg_num] = 0
#                     globals.t_f[leg_num] = phase_duration
#                     globals.lz_i[leg_num] = pms.lz0
#                     globals.lz_f[leg_num] = pms.lz0
                    
#                     # Добавить в блок установки stance
#                     globals.lx_i[leg_num] = 0.5 * globals.xdot_ref * phase_duration
#                     globals.lx_f[leg_num] = -0.5 * globals.xdot_ref * phase_duration
#                     globals.ly_i[leg_num] = 0.5 * globals.ydot_ref * phase_duration
#                     globals.ly_f[leg_num] = -0.5 * globals.ydot_ref * phase_duration

#                     # # Установка позиций для stance (чтобы нога не "прыгала")
#                     # globals.lx_i[leg_num] = globals.lx_ref[leg_num]
#                     # globals.lx_f[leg_num] = globals.lx_ref[leg_num]
#                     # globals.ly_i[leg_num] = globals.ly_ref[leg_num]
#                     # globals.ly_f[leg_num] = globals.ly_ref[leg_num]