#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.wait_state import WaitState
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_flexbe_states.find_correct_bin import FindCorrectBin
from ariac_flexbe_states.compute_grasp_ariac_state import ComputeGraspAriacState
from ariac_flexbe_states.detect_part_camera_ariac_state import DetectPartCameraAriacState
from ariac_flexbe_states.decide_offset_product import DecideOffsetProduct
from ariac_flexbe_states.gripper_control_state import GripperControl
from ariac_flexbe_behaviors.move_home_robot_r_sm import move_home_robot_rSM
from ariac_flexbe_states.moveit_to_joints_dyn_ariac_state import MoveitToJointsDynAriacState
from ariac_flexbe_behaviors.move_home_pick_sm import move_home_pickSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu May 27 2020
@author: Niels van Dongen
'''
class shelvepick_behavior_nvdSM(Behavior):
	'''
	behavior om blauwe gear te pakken
	'''


	def __init__(self):
		super(shelvepick_behavior_nvdSM, self).__init__()
		self.name = 'shelve pick_behavior_nvd'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(move_home_robot_rSM, 'move_home_robot_r')
		self.add_behavior(move_home_pickSM, 'move_home_pick')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:27 y:469, x:242 y:360
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.powerOn = 100
		_state_machine.userdata.config_name = ''
		_state_machine.userdata.move_group = 'Gantry'
		_state_machine.userdata.move_group_prefix = '/ariac/gantry'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.robot_name = 'gantry'
		_state_machine.userdata.part_type = 'gear_part_blue'
		_state_machine.userdata.joint_values = []
		_state_machine.userdata.joint_names = []
		_state_machine.userdata.ref_frame = 'world'
		_state_machine.userdata.camera_topic = ''
		_state_machine.userdata.camera_frame = ''
		_state_machine.userdata.tool_link_r = 'right_ee_link'
		_state_machine.userdata.pose = ''
		_state_machine.userdata.rotation = 0
		_state_machine.userdata.move_groupR = 'Right_Arm'
		_state_machine.userdata.arm_id_r = 'Right_Arm'
		_state_machine.userdata.Grasp5 = 'bingr5Grasp'

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:204 y:22
			OperatableStateMachine.add('move_home_pick',
										self.use_behavior(move_home_pickSM, 'move_home_pick'),
										transitions={'finished': 'Find_product_location', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:694 y:113
			OperatableStateMachine.add('move_gantry_bin_gr1',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'move_gantry_bin_gr1_2', 'planning_failed': 'Waitretry', 'control_failed': 'Waitretry', 'param_error': 'Waitretry'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'bin', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:559 y:28
			OperatableStateMachine.add('Find_product_location',
										FindCorrectBin(time_out=0.5),
										transitions={'continue': 'move_gantry_bin_gr1', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'part_type': 'part_type', 'bin': 'bin', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame', 'ref_frame': 'ref_frame'})

			# x:694 y:497
			OperatableStateMachine.add('compute_pick _r',
										ComputeGraspAriacState(joint_names=['right_shoulder_pan_joint', 'right_shoulder_lift_joint', 'right_elbow_joint', 'right_wrist_1_joint', 'right_wrist_2_joint', 'right_wrist_3_joint']),
										transitions={'continue': 'Move to pick', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_groupR', 'move_group_prefix': 'move_group_prefix', 'tool_link': 'tool_link_r', 'pose': 'pose', 'offset': 'part_offset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:714 y:310
			OperatableStateMachine.add('find part',
										DetectPartCameraAriacState(time_out=0.5),
										transitions={'continue': 'Offset bepalen', 'failed': 'failed', 'not_found': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ref_frame': 'ref_frame', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame', 'part': 'part_type', 'pose': 'pose'})

			# x:710 y:394
			OperatableStateMachine.add('Offset bepalen',
										DecideOffsetProduct(target_time=0.5),
										transitions={'succes': 'compute_pick _r', 'unknown_id': 'failed'},
										autonomy={'succes': Autonomy.Off, 'unknown_id': Autonomy.Off},
										remapping={'part_type': 'part_type', 'part_offset': 'part_offset'})

			# x:433 y:563
			OperatableStateMachine.add('Gripper_enable',
										GripperControl(enable=True),
										transitions={'continue': 'move_home_robot_r', 'failed': 'Move to pick', 'invalid_id': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'invalid_id': Autonomy.Off},
										remapping={'arm_id': 'arm_id_r'})

			# x:234 y:591
			OperatableStateMachine.add('move_home_robot_r',
										self.use_behavior(move_home_robot_rSM, 'move_home_robot_r'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:619 y:590
			OperatableStateMachine.add('Move to pick',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'Gripper_enable', 'planning_failed': 'failed', 'control_failed': 'Gripper_enable'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'move_groupR', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:702 y:174
			OperatableStateMachine.add('move_gantry_bin_gr1_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'find part', 'planning_failed': 'Waitretry_2', 'control_failed': 'Waitretry_2', 'param_error': 'Waitretry_2'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'Grasp5', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:872 y:178
			OperatableStateMachine.add('Waitretry_2',
										WaitState(wait_time=2),
										transitions={'done': 'move_gantry_bin_gr1_2'},
										autonomy={'done': Autonomy.Off})

			# x:810 y:40
			OperatableStateMachine.add('Waitretry',
										WaitState(wait_time=2),
										transitions={'done': 'move_gantry_bin_gr1'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
