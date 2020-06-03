#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_behaviors.inspect_arm_part_type_right_sm import inspect_arm_part_type_rightSM
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_flexbe_states.compute_drop_ariac_state import ComputeDropAriacState
from ariac_flexbe_states.moveit_to_joints_dyn_ariac_state import MoveitToJointsDynAriacState
from ariac_flexbe_states.gripper_control_state import GripperControl
from ariac_flexbe_behaviors.inspect_arm_part_type_left_sm import inspect_arm_part_type_leftSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Jun 03 2020
@author: wessel koolen
'''
class move_part_to_binSM(Behavior):
	'''
	behavior for moving a part to its destined bin inside the warehouse
	'''


	def __init__(self):
		super(move_part_to_binSM, self).__init__()
		self.name = 'move_part_to_bin'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(inspect_arm_part_type_rightSM, 'inspect_arm_part_type_right')
		self.add_behavior(inspect_arm_part_type_leftSM, 'inspect_arm_part_type_left')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:31 y:622, x:691 y:334
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['part_type_right', 'part_type_left'])
		_state_machine.userdata.config_name_right_bin1 = 'rightArmBin1'
		_state_machine.userdata.move_group_gantry = 'Gantry'
		_state_machine.userdata.move_group_prefix = '/ariac/gantry'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.robot_name = ''
		_state_machine.userdata.joint_values = []
		_state_machine.userdata.joint_names = ''
		_state_machine.userdata.part_type_right = ''
		_state_machine.userdata.part_type_left = ''
		_state_machine.userdata.config_name_right_bin2 = 'rightArmBin2'
		_state_machine.userdata.move_group_right_arm = 'Right_Arm'
		_state_machine.userdata.move_group_left_arm = 'Left_Arm'
		_state_machine.userdata.tool_link_right = 'right_ee_link'
		_state_machine.userdata.offset_x = 0
		_state_machine.userdata.offset_y = 0
		_state_machine.userdata.offset_z = 0
		_state_machine.userdata.rotation = 0
		_state_machine.userdata.pose = []
		_state_machine.userdata.tool_link_left = 'left_ee_link'
		_state_machine.userdata.arm1 = 'Right_Arm'
		_state_machine.userdata.arm2 = 'Left_Arm'
		_state_machine.userdata.config_name_right_home = 'Right_Home'
		_state_machine.userdata.config_name_left_home = 'Left_Home'
		_state_machine.userdata.config_name_left_bin1 = 'leftArmBin1'
		_state_machine.userdata.config_name_left_bin2 = 'leftArmBin2'
		_state_machine.userdata.pose1 = 'bin1'
		_state_machine.userdata.pose2 = 'bin2'

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:86 y:86
			OperatableStateMachine.add('inspect_arm_part_type_right',
										self.use_behavior(inspect_arm_part_type_rightSM, 'inspect_arm_part_type_right'),
										transitions={'gasket_part': 'MoveToGasketBin', 'failed': 'failed', 'piston_rod_part': 'MoveToPistonBin'},
										autonomy={'gasket_part': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'piston_rod_part': Autonomy.Inherit},
										remapping={'part_type_right': 'part_type_right', 'part_type_left': 'part_type_left'})

			# x:347 y:38
			OperatableStateMachine.add('MoveToPistonBin',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'ComputeDropPartPiston', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_right_bin1', 'move_group': 'move_group_gantry', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:348 y:161
			OperatableStateMachine.add('MoveToGasketBin',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'ComputeDropPartGasket', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_right_bin2', 'move_group': 'move_group_gantry', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:528 y:37
			OperatableStateMachine.add('ComputeDropPartPiston',
										ComputeDropAriacState(joint_names=['right_shoulder_pan_joint', 'right_shoulder_lift_joint', 'right_elbow_joint', 'right_wrist_1_joint', 'right_wrist_2_joint', 'right_wrist_3_joint']),
										transitions={'continue': 'MoveToPlacePiston', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group_right_arm', 'move_group_prefix': 'move_group_prefix', 'tool_link': 'tool_link_right', 'pose': 'pose1', 'offset_x': 'offset_x', 'offset_y': 'offset_y', 'offset_z': 'offset_z', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:531 y:162
			OperatableStateMachine.add('ComputeDropPartGasket',
										ComputeDropAriacState(joint_names=['right_shoulder_pan_joint', 'right_shoulder_lift_joint', 'right_elbow_joint', 'right_wrist_1_joint', 'right_wrist_2_joint', 'right_wrist_3_joint']),
										transitions={'continue': 'MoveToPlaceGasket', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group_right_arm', 'move_group_prefix': 'move_group_prefix', 'tool_link': 'tool_link_right', 'pose': 'pose2', 'offset_x': 'offset_x', 'offset_y': 'offset_y', 'offset_z': 'offset_z', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:719 y:37
			OperatableStateMachine.add('MoveToPlacePiston',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'DisableGripperPiston', 'planning_failed': 'ComputeDropPartPiston', 'control_failed': 'MoveToPlaceGasket'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'move_group_right_arm', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:725 y:162
			OperatableStateMachine.add('MoveToPlaceGasket',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'DisableGripperGasket', 'planning_failed': 'ComputeDropPartGasket', 'control_failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'move_group_right_arm', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:919 y:35
			OperatableStateMachine.add('DisableGripperPiston',
										GripperControl(enable=False),
										transitions={'continue': 'MoveRightHome', 'failed': 'MoveToPlaceGasket', 'invalid_id': 'MoveToPlacePiston'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'invalid_id': Autonomy.Off},
										remapping={'arm_id': 'arm1'})

			# x:922 y:165
			OperatableStateMachine.add('DisableGripperGasket',
										GripperControl(enable=False),
										transitions={'continue': 'MoveRightHome_2', 'failed': 'failed', 'invalid_id': 'MoveToPlaceGasket'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'invalid_id': Autonomy.Off},
										remapping={'arm_id': 'arm1'})

			# x:1094 y:36
			OperatableStateMachine.add('MoveRightHome',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'inspect_arm_part_type_left', 'planning_failed': 'MoveToPlaceGasket', 'control_failed': 'failed', 'param_error': 'MoveToPlaceGasket'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_right_home', 'move_group': 'move_group_right_arm', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1094 y:164
			OperatableStateMachine.add('MoveRightHome_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'inspect_arm_part_type_left', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_right_home', 'move_group': 'move_group_right_arm', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1111 y:530
			OperatableStateMachine.add('inspect_arm_part_type_left',
										self.use_behavior(inspect_arm_part_type_leftSM, 'inspect_arm_part_type_left'),
										transitions={'gasket_part': 'MoveToGasketBinLeft', 'failed': 'failed', 'piston_rod_part': 'MoveToPistonBinLeft'},
										autonomy={'gasket_part': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'piston_rod_part': Autonomy.Inherit},
										remapping={'part_type_right': 'part_type_right', 'part_type_left': 'part_type_left'})

			# x:927 y:448
			OperatableStateMachine.add('MoveToPistonBinLeft',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'ComputeDropPartPistonLeft', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_left_bin1', 'move_group': 'move_group_gantry', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:928 y:599
			OperatableStateMachine.add('MoveToGasketBinLeft',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'ComputeDropPartGasketLeft', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_left_bin2', 'move_group': 'move_group_gantry', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:702 y:454
			OperatableStateMachine.add('ComputeDropPartPistonLeft',
										ComputeDropAriacState(joint_names=['left_shoulder_pan_joint', 'left_shoulder_lift_joint', 'left_elbow_joint', 'left_wrist_1_joint', 'left_wrist_2_joint', 'left_wrist_3_joint']),
										transitions={'continue': 'MoveToPlacePistonLeft', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group_left_arm', 'move_group_prefix': 'move_group_prefix', 'tool_link': 'tool_link_left', 'pose': 'pose1', 'offset_x': 'offset_x', 'offset_y': 'offset_y', 'offset_z': 'offset_z', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:699 y:595
			OperatableStateMachine.add('ComputeDropPartGasketLeft',
										ComputeDropAriacState(joint_names=['left_shoulder_pan_joint', 'left_shoulder_lift_joint', 'left_elbow_joint', 'left_wrist_1_joint', 'left_wrist_2_joint', 'left_wrist_3_joint']),
										transitions={'continue': 'MoveToPlaceGasketLeft', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group_left_arm', 'move_group_prefix': 'move_group_prefix', 'tool_link': 'tool_link_left', 'pose': 'pose2', 'offset_x': 'offset_x', 'offset_y': 'offset_y', 'offset_z': 'offset_z', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:515 y:451
			OperatableStateMachine.add('MoveToPlacePistonLeft',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'DisableGripperPistonLeft', 'planning_failed': 'ComputeDropPartPistonLeft', 'control_failed': 'DisableGripperPistonLeft'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'move_group_left_arm', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:508 y:594
			OperatableStateMachine.add('MoveToPlaceGasketLeft',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'DisableGripperGasketLeft', 'planning_failed': 'ComputeDropPartGasketLeft', 'control_failed': 'DisableGripperGasketLeft'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'move_group_left_arm', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:326 y:447
			OperatableStateMachine.add('DisableGripperPistonLeft',
										GripperControl(enable=False),
										transitions={'continue': 'MoveLeftHome', 'failed': 'failed', 'invalid_id': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'invalid_id': Autonomy.Off},
										remapping={'arm_id': 'arm2'})

			# x:329 y:603
			OperatableStateMachine.add('DisableGripperGasketLeft',
										GripperControl(enable=False),
										transitions={'continue': 'MoveLeftHome_2', 'failed': 'failed', 'invalid_id': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'invalid_id': Autonomy.Off},
										remapping={'arm_id': 'arm2'})

			# x:168 y:602
			OperatableStateMachine.add('MoveLeftHome_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'finished', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_left_home', 'move_group': 'move_group_left_arm', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:168 y:445
			OperatableStateMachine.add('MoveLeftHome',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'finished', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_left_home', 'move_group': 'move_group_left_arm', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
