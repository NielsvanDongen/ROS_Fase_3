#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_support_flexbe_states.equal_state import EqualState
from ariac_flexbe_states.gripper_active_check import GripperActiveCheck
from ariac_flexbe_states.gripper_control_state import GripperControl
from ariac_flexbe_states.get_object_pose import GetObjectPoseState
from ariac_flexbe_states.moveit_to_joints_dyn_ariac_state import MoveitToJointsDynAriacState
from ariac_flexbe_states.compute_drop_nvd import ComputeDropPartOffsetGraspAriacState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed May 27 2020
@author: Niels van Dongen
'''
class move_to_agvSM(Behavior):
	'''
	Moves complete gantry to the chosen agv.
	'''


	def __init__(self):
		super(move_to_agvSM, self).__init__()
		self.name = 'move_to_agv'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1345 y:747, x:130 y:406
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['agv_id', 'pose_on_agv_l', 'pose_on_agv_r'])
		_state_machine.userdata.config_name_left = 'Left_Home_B'
		_state_machine.userdata.config_name_right = 'Right_Home_B'
		_state_machine.userdata.config_name_gantry = 'Gantry_Home'
		_state_machine.userdata.move_group_g = 'Gantry'
		_state_machine.userdata.move_group_prefix_g = '/ariac/gantry'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.robot_name = 'gantry'
		_state_machine.userdata.joint_values = []
		_state_machine.userdata.joint_names = []
		_state_machine.userdata.move_group_l = 'Left_Arm'
		_state_machine.userdata.move_group_r = 'Right_Arm'
		_state_machine.userdata.agv_id = ''
		_state_machine.userdata.config_name_agv1_r = 'Gantry_AGV1_R'
		_state_machine.userdata.config_name_agv1_l = 'Gantry_AGV1_L'
		_state_machine.userdata.config_name_agv2_l = 'Gantry_AGV2_L'
		_state_machine.userdata.config_name_agv2_r = 'Gantry_AGV2_R'
		_state_machine.userdata.agv2 = 'agv2'
		_state_machine.userdata.arm_id_r = 'Right_Arm'
		_state_machine.userdata.arm_id_l = 'Left_Arm'
		_state_machine.userdata.agv_pose = []
		_state_machine.userdata.offset = 0.09
		_state_machine.userdata.tool_link_r = 'right_ee_link'
		_state_machine.userdata.tool_link_l = 'left_ee_link'
		_state_machine.userdata.rotation = 0
		_state_machine.userdata.pose_on_agv_r = []
		_state_machine.userdata.pose_on_agv_l = []

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:30 y:40
			OperatableStateMachine.add('MoveLeftArm',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'MoveRightArm', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_left', 'move_group': 'move_group_l', 'move_group_prefix': 'move_group_prefix_g', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:208 y:38
			OperatableStateMachine.add('MoveRightArm',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'MoveGantryhome band', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_right', 'move_group': 'move_group_r', 'move_group_prefix': 'move_group_prefix_g', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:517 y:167
			OperatableStateMachine.add('MoveGantryagv1',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'Getet agv pose', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_agv1_r', 'move_group': 'move_group_g', 'move_group_prefix': 'move_group_prefix_g', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:596 y:51
			OperatableStateMachine.add('check agv id',
										EqualState(),
										transitions={'true': 'MoveGantryagv2', 'false': 'MoveGantryagv1'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'agv_id', 'value_b': 'agv2'})

			# x:1116 y:42
			OperatableStateMachine.add('MoveGantryagv2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'finished', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_agv2_r', 'move_group': 'move_group_g', 'move_group_prefix': 'move_group_prefix_g', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:420 y:12
			OperatableStateMachine.add('MoveGantryhome band',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'check agv id', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_gantry', 'move_group': 'move_group_g', 'move_group_prefix': 'move_group_prefix_g', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:346 y:632
			OperatableStateMachine.add('gripper active check',
										GripperActiveCheck(),
										transitions={'Left': 'finished', 'Right': 'MoveGantryagv1-2', 'failed': 'failed', 'Full': 'MoveGantryagv1-2'},
										autonomy={'Left': Autonomy.Off, 'Right': Autonomy.Off, 'failed': Autonomy.Off, 'Full': Autonomy.Off},
										remapping={'arm_id': 'arm_id', 'tool_link': 'tool_link', 'move_group': 'move_group'})

			# x:370 y:724
			OperatableStateMachine.add('MoveGantryagv1-2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'Getet agv pose_2', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_agv1_l', 'move_group': 'move_group_g', 'move_group_prefix': 'move_group_prefix_g', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:481 y:497
			OperatableStateMachine.add('gripper disabble',
										GripperControl(enable=False),
										transitions={'continue': 'MoveRightArm_2', 'failed': 'failed', 'invalid_id': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'invalid_id': Autonomy.Off},
										remapping={'arm_id': 'arm_id_r'})

			# x:528 y:247
			OperatableStateMachine.add('Getet agv pose',
										GetObjectPoseState(object_frame='kit_tray_1', ref_frame='world'),
										transitions={'continue': 'test', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'agv_pose'})

			# x:495 y:404
			OperatableStateMachine.add('move to drop',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'gripper disabble', 'planning_failed': 'failed', 'control_failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix_g', 'move_group': 'move_group_r', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:484 y:331
			OperatableStateMachine.add('test',
										ComputeDropPartOffsetGraspAriacState(joint_names=['right_shoulder_pan_joint', 'right_shoulder_lift_joint', 'right_elbow_joint', 'right_wrist_1_joint', 'right_wrist_2_joint', 'right_wrist_3_joint']),
										transitions={'continue': 'move to drop', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group_r', 'move_group_prefix': 'move_group_prefix_g', 'tool_link': 'tool_link_r', 'part_pose': 'pose_on_agv_r', 'pose': 'agv_pose', 'offset': 'offset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:775 y:445
			OperatableStateMachine.add('gripper disabble_2',
										GripperControl(enable=False),
										transitions={'continue': 'MoveLeftArm_2', 'failed': 'failed', 'invalid_id': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'invalid_id': Autonomy.Off},
										remapping={'arm_id': 'arm_id_l'})

			# x:771 y:189
			OperatableStateMachine.add('Getet agv pose_2',
										GetObjectPoseState(object_frame='kit_tray_1', ref_frame='world'),
										transitions={'continue': 'test_2', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'agv_pose'})

			# x:755 y:358
			OperatableStateMachine.add('move to drop_2',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'gripper disabble_2', 'planning_failed': 'failed', 'control_failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix_g', 'move_group': 'move_group_l', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:746 y:282
			OperatableStateMachine.add('test_2',
										ComputeDropPartOffsetGraspAriacState(joint_names=['left_shoulder_pan_joint', 'left_shoulder_lift_joint', 'left_elbow_joint', 'left_wrist_1_joint', 'left_wrist_2_joint', 'left_wrist_3_joint']),
										transitions={'continue': 'move to drop_2', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group_l', 'move_group_prefix': 'move_group_prefix_g', 'tool_link': 'tool_link_l', 'part_pose': 'pose_on_agv_l', 'pose': 'agv_pose', 'offset': 'offset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:444 y:566
			OperatableStateMachine.add('MoveRightArm_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'gripper active check', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_right', 'move_group': 'move_group_r', 'move_group_prefix': 'move_group_prefix_g', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:770 y:549
			OperatableStateMachine.add('MoveLeftArm_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'finished', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_left', 'move_group': 'move_group_l', 'move_group_prefix': 'move_group_prefix_g', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
