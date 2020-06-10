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
from ariac_flexbe_states.moveit_to_joints_dyn_ariac_state import MoveitToJointsDynAriacState
from flexbe_states.wait_state import WaitState
from ariac_flexbe_states.gripper_active_check import GripperActiveCheck
from ariac_support_flexbe_states.replace_state import ReplaceState
from ariac_support_flexbe_states.equal_state import EqualState
from ariac_flexbe_behaviors.move_home_robot_r_s_sm import move_home_robot_r_SSM
from ariac_flexbe_behaviors.move_home_robot_l_s_sm import move_home_robot_l_SSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu May 27 2020
@author: Niels van Dongen
'''
class shelvepick_behavior_V2SM(Behavior):
	'''
	behavior om parts de shelve te pakken
	'''


	def __init__(self):
		super(shelvepick_behavior_V2SM, self).__init__()
		self.name = 'shelve pick_behavior_V2'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(move_home_pickSM, 'move_home_pick')
		self.add_behavior(move_home_robot_r_SSM, 'move_home_robot_r_S')
		self.add_behavior(move_home_robot_l_SSM, 'move_home_robot_l_S')

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
		_state_machine.userdata.Grasp5 = 'bingr5SafeGrasp'
		_state_machine.userdata.arm_id_l = 'Left_Arm'
		_state_machine.userdata.move_groupL = 'Left_Arm'
		_state_machine.userdata.tool_link_l = 'left_ee_link'
		_state_machine.userdata.pose_on_agv = []
		_state_machine.userdata.pose_on_agv_l = []
		_state_machine.userdata.pose_on_agv_r = []
		_state_machine.userdata.bin5r = 'bin5R'
		_state_machine.userdata.bin5l = 'bin5L'
		_state_machine.userdata.bin4r = 'bin4R'
		_state_machine.userdata.bin4l = 'bin4L'
		_state_machine.userdata.bin5 = 'bingr5PreGrasp'
		_state_machine.userdata.move_group_g = 'Gantry'

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:204 y:22
			OperatableStateMachine.add('move_home_pick',
										self.use_behavior(move_home_pickSM, 'move_home_pick'),
										transitions={'finished': 'Find_product_location', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:1426 y:173
			OperatableStateMachine.add('move_gantry_bin_gr1',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'find part', 'planning_failed': 'Waitretry', 'control_failed': 'Waitretry', 'param_error': 'Waitretry'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'bin4r', 'move_group': 'move_group_g', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:471 y:43
			OperatableStateMachine.add('Find_product_location',
										FindCorrectBin(time_out=0.5),
										transitions={'continue': 'move_gantry_bin_gr1_2', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'part_type': 'part_type', 'bin': 'bin', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame', 'ref_frame': 'ref_frame'})

			# x:1573 y:588
			OperatableStateMachine.add('compute_pick _r',
										ComputeGraspAriacState(joint_names=['right_shoulder_pan_joint', 'right_shoulder_lift_joint', 'right_elbow_joint', 'right_wrist_1_joint', 'right_wrist_2_joint', 'right_wrist_3_joint']),
										transitions={'continue': 'Move to pick', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_groupR', 'move_group_prefix': 'move_group_prefix', 'tool_link': 'tool_link_r', 'pose': 'pose', 'offset': 'part_offset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1317 y:280
			OperatableStateMachine.add('find part',
										DetectPartCameraAriacState(time_out=0.5),
										transitions={'continue': 'Offset bepalen', 'failed': 'failed', 'not_found': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ref_frame': 'ref_frame', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame', 'part': 'part_type', 'pose': 'pose'})

			# x:1631 y:341
			OperatableStateMachine.add('Offset bepalen',
										DecideOffsetProduct(target_time=0.5),
										transitions={'succes': 'gripper check_3', 'unknown_id': 'failed'},
										autonomy={'succes': Autonomy.Off, 'unknown_id': Autonomy.Off},
										remapping={'part_type': 'part_type', 'part_offset': 'part_offset'})

			# x:1223 y:684
			OperatableStateMachine.add('Gripper_enable_r',
										GripperControl(enable=True),
										transitions={'continue': 'pose safe r', 'failed': 'Move to pick', 'invalid_id': 'Gripper_enable_r'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'invalid_id': Autonomy.Off},
										remapping={'arm_id': 'arm_id_r'})

			# x:1363 y:603
			OperatableStateMachine.add('Move to pick',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'Gripper_enable_r', 'planning_failed': 'failed', 'control_failed': 'Gripper_enable_r'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'move_groupR', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:633 y:98
			OperatableStateMachine.add('move_gantry_bin_gr1_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'Equal bin 5', 'planning_failed': 'Waitretry_2', 'control_failed': 'Waitretry_2', 'param_error': 'Waitretry_2'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'Grasp5', 'move_group': 'move_group_g', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:690 y:7
			OperatableStateMachine.add('Waitretry_2',
										WaitState(wait_time=2),
										transitions={'done': 'move_gantry_bin_gr1_2'},
										autonomy={'done': Autonomy.Off})

			# x:1287 y:110
			OperatableStateMachine.add('Waitretry',
										WaitState(wait_time=2),
										transitions={'done': 'move_gantry_bin_gr1'},
										autonomy={'done': Autonomy.Off})

			# x:992 y:121
			OperatableStateMachine.add('gripper check',
										GripperActiveCheck(),
										transitions={'Left': 'move_gantry_bin_gr1_3_2', 'Right': 'move_gantry_bin_gr1_3', 'failed': 'failed', 'Full': 'failed'},
										autonomy={'Left': Autonomy.Off, 'Right': Autonomy.Off, 'failed': Autonomy.Off, 'Full': Autonomy.Off},
										remapping={'arm_id': 'arm_id', 'tool_link': 'tool_link', 'move_group': 'move_group'})

			# x:1280 y:433
			OperatableStateMachine.add('compute_pick _l',
										ComputeGraspAriacState(joint_names=['left_shoulder_pan_joint', 'left_shoulder_lift_joint', 'left_elbow_joint', 'left_wrist_1_joint', 'left_wrist_2_joint', 'left_wrist_3_joint']),
										transitions={'continue': 'Move to pick_l', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_groupL', 'move_group_prefix': 'move_group_prefix', 'tool_link': 'tool_link_l', 'pose': 'pose', 'offset': 'part_offset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:947 y:447
			OperatableStateMachine.add('Gripper_enable_l',
										GripperControl(enable=True),
										transitions={'continue': 'pose safe l', 'failed': 'Move to pick_l', 'invalid_id': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'invalid_id': Autonomy.Off},
										remapping={'arm_id': 'arm_id_l'})

			# x:1089 y:372
			OperatableStateMachine.add('Move to pick_l',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'Gripper_enable_l', 'planning_failed': 'failed', 'control_failed': 'Gripper_enable_l'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'move_groupL', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1059 y:618
			OperatableStateMachine.add('pose safe r',
										ReplaceState(),
										transitions={'done': 'move_home_robot_r_S'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'pose_on_agv', 'result': 'pose_on_agv_r'})

			# x:785 y:400
			OperatableStateMachine.add('pose safe l',
										ReplaceState(),
										transitions={'done': 'move_home_robot_l_S'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'pose_on_agv', 'result': 'pose_on_agv_l'})

			# x:1176 y:35
			OperatableStateMachine.add('Equal bin 5',
										EqualState(),
										transitions={'true': 'gripper check', 'false': 'gripper check_2'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'bin', 'value_b': 'bin5'})

			# x:1526 y:51
			OperatableStateMachine.add('gripper check_2',
										GripperActiveCheck(),
										transitions={'Left': 'move_gantry_bin_gr1_4', 'Right': 'move_gantry_bin_gr1', 'failed': 'failed', 'Full': 'failed'},
										autonomy={'Left': Autonomy.Off, 'Right': Autonomy.Off, 'failed': Autonomy.Off, 'Full': Autonomy.Off},
										remapping={'arm_id': 'arm_id', 'tool_link': 'tool_link', 'move_group': 'move_group'})

			# x:864 y:238
			OperatableStateMachine.add('move_gantry_bin_gr1_3',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'find part', 'planning_failed': 'Waitretry_3', 'control_failed': 'Waitretry_3', 'param_error': 'Waitretry_3'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'bin5r', 'move_group': 'move_group_g', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:830 y:134
			OperatableStateMachine.add('Waitretry_3',
										WaitState(wait_time=2),
										transitions={'done': 'move_gantry_bin_gr1_3'},
										autonomy={'done': Autonomy.Off})

			# x:1083 y:230
			OperatableStateMachine.add('move_gantry_bin_gr1_3_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'find part', 'planning_failed': 'Waitretry_3_2', 'control_failed': 'Waitretry_3_2', 'param_error': 'Waitretry_3_2'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'bin5l', 'move_group': 'move_group_g', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1168 y:110
			OperatableStateMachine.add('Waitretry_3_2',
										WaitState(wait_time=2),
										transitions={'done': 'move_gantry_bin_gr1_3_2'},
										autonomy={'done': Autonomy.Off})

			# x:1632 y:163
			OperatableStateMachine.add('move_gantry_bin_gr1_4',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'find part', 'planning_failed': 'Waitretry_4', 'control_failed': 'Waitretry_4', 'param_error': 'Waitretry_4'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'bin4l', 'move_group': 'move_group_g', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1736 y:8
			OperatableStateMachine.add('Waitretry_4',
										WaitState(wait_time=2),
										transitions={'done': 'move_gantry_bin_gr1_4'},
										autonomy={'done': Autonomy.Off})

			# x:1462 y:416
			OperatableStateMachine.add('gripper check_3',
										GripperActiveCheck(),
										transitions={'Left': 'compute_pick _l', 'Right': 'compute_pick _r', 'failed': 'failed', 'Full': 'failed'},
										autonomy={'Left': Autonomy.Off, 'Right': Autonomy.Off, 'failed': Autonomy.Off, 'Full': Autonomy.Off},
										remapping={'arm_id': 'arm_id', 'tool_link': 'tool_link', 'move_group': 'move_group'})

			# x:860 y:680
			OperatableStateMachine.add('move_home_robot_r_S',
										self.use_behavior(move_home_robot_r_SSM, 'move_home_robot_r_S'),
										transitions={'finished': 'move_gantry_bin_gr1_2_2', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:612 y:468
			OperatableStateMachine.add('move_home_robot_l_S',
										self.use_behavior(move_home_robot_l_SSM, 'move_home_robot_l_S'),
										transitions={'finished': 'move_gantry_bin_gr1_2_2', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:538 y:627
			OperatableStateMachine.add('move_gantry_bin_gr1_2_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'finished', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'Grasp5', 'move_group': 'move_group_g', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
