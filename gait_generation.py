import mujoco as mj # type: ignore
import mujoco.viewer as viewer # type: ignore
import numpy as np # type: ignore
import globals
import os
from state_machine import state_machine
from forward_kinematics_leg import forward_kinematics_leg
from cartesian_traj import cartesian_traj
from joint_trah import joint_traj
from joint_control import joint_control 

flag_trajectory_generation = 0

model_path = r"C:\Users\Polina\Documents\ITMO\Graduation_Thesis\mujoco-3.3.0-windows-x86_64\model\unitree_a1\scene.xml"
model = mj.MjModel.from_xml_path(model_path)
data = mj.MjData(model)

globals.init()
hip = 0
pitch = 0.9
knee = -1.8

sol = forward_kinematics_leg(np.array([hip,pitch,knee]),0)
end_eff_pos = sol.end_eff_pos
lz0=end_eff_pos[2]
#print(lz0)

pos = np.array([0,0,0.3])
quat = np.array([1,0,0,0])
qleg = np.array([hip,pitch,knee])

#setting initial position
data.qpos = np.concatenate((pos,quat,qleg,qleg,qleg,qleg))

with viewer.launch_passive(model, data) as vis:
    while vis.is_running():

        model.opt.timestep = 0.001
        state_machine()
        cartesian_traj()
        joint_traj()
        globals.time = data.time

        if(flag_trajectory_generation==1): #kinematic mode
            data.time +=model.opt.timestep
            data.qpos = np.concatenate((pos,quat,globals.q_ref))
            mj.mj_forward(model,data)
        else: #dynamic mode
            globals.q_act = data.qpos[7:].copy()
            globals.u_act = data.qvel[6:].copy()
            joint_control()
            data.ctrl = globals.trq.copy()
            mj.mj_step(model, data)

        # Camera setup
        # vis.cam.lookat[:] = data.qpos[:3] 
        # vis.cam.distance = 2.0
        # vis.cam.elevation = -10
        # vis.cam.azimuth = 90
         
        
        vis.sync()
