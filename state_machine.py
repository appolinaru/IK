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

        if(time >= globals.t_fsm[leg_num]+ t_step and globals.fsm[leg_num]==fsm_swing):
            globals.fsm[leg_num] = fsm_stance
            globals.t_fsm[leg_num] = time
            globals.t_i[leg_num] = 0
            globals.t_f[leg_num] = t_step
            globals.lz_i[leg_num] = pms.lz0
            globals.lz_f[leg_num] = pms.lz0

            globals.lx_i[leg_num] = 0.5*globals.xdot_ref * t_step
            globals.lx_f[leg_num] = -0.5*globals.xdot_ref * t_step
