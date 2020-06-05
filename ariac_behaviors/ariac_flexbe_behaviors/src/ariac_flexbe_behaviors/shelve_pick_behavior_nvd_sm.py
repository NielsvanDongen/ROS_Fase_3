#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_behaviors.move_home_pick_sm import move_home_pickSM
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_flexbe_states.find_correct_bin import FindCorrectBin
from ariac_flexbe_states.compute_grasp_ariac_state import ComputeGraspAriacState
from ariac_flexbe_states.detect_part_camera_ariac_state import DetectPartCameraAriacState
from ariac_flexbe_states.decide_offset_product import DecideOffsetProduct
from ariac_flexbe_states.gripper_control_state import GripperControl
from ariac_flexbe_behaviors.move_home_robot_r_sm import move_home_robot_rSM
from ariac_flexbe_states.moveit_to_joints_dyn_ariac_state import MoveitToJointsDynAriacState
from flexbe_states.wait_state import WaitState
from ariac_flexbe_states.gripper_active_check import GripperActiveCheck
from ariac_support_flexbe_states.replace_state import ReplaceState
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
		self.add_behavior(move_home_pickSM, 'move_home_pick')
		self.add_behavior(move_home_robot_rSM, 'move_home_robot_r')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:27 y:469, x:793 y:325
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['pose_on_agv', 'part_type'], output_keys=['pose_on_agv_l', 'pose_on_agv_r'])
		_state_machine.userdata.powerOn = 100
		_state_machine.userdata.config_name = ''
		_state_machine.userdata.move_group = 'Gantry'
		_state_machine.userdata.move_group_prefix = '/ariac/gantry'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.robot_name = 'gantry'
		_state_machine.userdata.part_type = ''
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
		_state_machine.userdata.arm_id_l = 'Left_Arm'
		_state_machine.userdata.move_groupL = 'Left_Arm'
		_state_machine.userdata.tool_link_l = 'left_ee_link'
		_state_machine.userdata.pose_on_agv = []
		_state_machine.userdata.pose_on_agv_l = []
		_state_machine.userdata.pose_on_agv_r = []

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:204 y:22
			OperatableStateMachine.add('move_home_pick',
										self.use_behavior(move_home_pickSM, 'move_home_pick'),
										transitions={'finished': 'Find_product_location', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:660 y:108
			OperatableStateMachine.add('move_gantry_bin_gr1',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'move_gantry_bin_gr1_2', 'planning_failed': 'Waitretry', 'control_failed': 'Waitretry', 'param_error': 'Waitretry'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'bin', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:471 y:43
			OperatableStateMachine.add('Find_product_location',
										FindCorrectBin(time_out=0.5),
										transitions={'continue': 'move_gantry_bin_gr1', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'part_type': 'part_type', 'bin': 'bin', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame', 'ref_frame': 'ref_frame'})

			# x:1089 y:258
			OperatableStateMachine.add('compute_pick _r',
										ComputeGraspAriacState(joint_names=['right_shoulder_pan_joint', 'right_shoulder_lift_joint', 'right_elbow_joint', 'right_wrist_1_joint', 'right_wrist_2_joint', 'right_wrist_3_joint']),
										transitions={'continue': 'Move to pick', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_groupR', 'move_group_prefix': 'move_group_prefix', 'tool_link': 'tool_link_r', 'pose': 'pose', 'offset': 'part_offset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1096 y:74
			OperatableStateMachine.add('find part',
										DetectPartCameraAriacState(time_out=0.5),
										transitions={'continue': 'Offset bepalen', 'failed': 'failed', 'not_found': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ref_frame': 'ref_frame', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame', 'part': 'part_type', 'pose': 'pose'})

			# x:1300 y:88
			OperatableStateMachine.add('Offset bepalen',
										DecideOffsetProduct(target_time=0.5),
										transitions={'succes': 'gripper check', 'unknown_id': 'failed'},
										autonomy={'succes': Autonomy.Off, 'unknown_id': Autonomy.Off},
										remapping={'part_type': 'part_type', 'part_offset': 'part_offset'})

			# x:1024 y:463
			OperatableStateMachine.add('Gripper_enable',
										GripperControl(enable=True),
										transitions={'continue': 'pose safe r', 'failed': 'Move to pick', 'invalid_id': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'invalid_id': Autonomy.Off},
										remapping={'arm_id': 'arm_id_r'})

			# x:648 y:701
			OperatableStateMachine.add('move_home_robot_r',
										self.use_behavior(move_home_robot_rSM, 'move_home_robot_r'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:1064 y:360
			OperatableStateMachine.add('Move to pick',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'Gripper_enable', 'planning_failed': 'failed', 'control_failed': 'Gripper_enable'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'move_groupR', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:870 y:107
			OperatableStateMachine.add('move_gantry_bin_gr1_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'find part', 'planning_failed': 'Waitretry_2', 'control_failed': 'Waitretry_2', 'param_error': 'Waitretry_2'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'Grasp5', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:882 y:10
			OperatableStateMachine.add('Waitretry_2',
										WaitState(wait_time=2),
										transitions={'done': 'move_gantry_bin_gr1_2'},
										autonomy={'done': Autonomy.Off})

			# x:686 y:12
			OperatableStateMachine.add('Waitretry',
										WaitState(wait_time=2),
										transitions={'done': 'move_gantry_bin_gr1'},
										autonomy={'done': Autonomy.Off})

			# x:1306 y:173
			OperatableStateMachine.add('gripper check',
										GripperActiveCheck(),
										transitions={'Left': 'compute_pick _l', 'Right': 'compute_pick _r', 'failed': 'failed', 'Full': 'move_home_pick'},
										autonomy={'Left': Autonomy.Off, 'Right': Autonomy.Off, 'failed': Autonomy.Off, 'Full': Autonomy.Off},
										remapping={'arm_id': 'arm_id', 'tool_link': 'tool_link', 'move_group': 'move_group'})

			# x:1527 y:231
			OperatableStateMachine.add('compute_pick _l',
										ComputeGraspAriacState(joint_names=['left_shoulder_pan_joint', 'left_shoulder_lift_joint', 'left_elbow_joint', 'left_wrist_1_joint', 'left_wrist_2_joint', 'left_wrist_3_joint']),
										transitions={'continue': 'Move to pick_l', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_groupL', 'move_group_prefix': 'move_group_prefix', 'tool_link': 'tool_link_l', 'pose': 'pose', 'offset': 'part_offset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1573 y:425
			OperatableStateMachine.add('Gripper_enable_2',
										GripperControl(enable=True),
										transitions={'continue': 'pose safe l', 'failed': 'Move to pick_l', 'invalid_id': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'invalid_id': Autonomy.Off},
										remapping={'arm_id': 'arm_id_l'})

			# x:1530 y:319
			OperatableStateMachine.add('Move to pick_l',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'Gripper_enable_2', 'planning_failed': 'failed', 'control_failed': 'Gripper_enable_2'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'move_groupL', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:865 y:537
			OperatableStateMachine.add('pose safe r',
										ReplaceState(),
										transitions={'done': 'move_home_robot_r'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'pose_on_agv', 'result': 'pose_on_agv_r'})

			# x:1502 y:553
			OperatableStateMachine.add('pose safe l',
										ReplaceState(),
										transitions={'done': 'move_home_robot_r'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'pose_on_agv', 'result': 'pose_on_agv_l'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
