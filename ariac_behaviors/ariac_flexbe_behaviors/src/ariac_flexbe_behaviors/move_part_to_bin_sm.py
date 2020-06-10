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
from ariac_flexbe_states.get_object_pose import GetObjectPoseState
from ariac_support_flexbe_states.add_numeric_state import AddNumericState
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
		# x:80 y:338, x:691 y:334
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
		_state_machine.userdata.bin1_offset = 0
		_state_machine.userdata.rotation = 0
		_state_machine.userdata.poseBin1 = []
		_state_machine.userdata.tool_link_left = 'left_ee_link'
		_state_machine.userdata.arm1 = 'Right_Arm'
		_state_machine.userdata.arm2 = 'Left_Arm'
		_state_machine.userdata.config_name_right_home = 'Right_Home'
		_state_machine.userdata.config_name_left_home = 'Left_Home'
		_state_machine.userdata.config_name_left_bin1 = 'leftArmBin1'
		_state_machine.userdata.config_name_left_bin2 = 'leftArmBin2'
		_state_machine.userdata.poseBin2 = []
		_state_machine.userdata.iterator = 0.17
		_state_machine.userdata.offset = 0
		_state_machine.userdata.bin2_offset = 0
		_state_machine.userdata.config_name_right_left = 'gantryPosPlaceRightLeft'
		_state_machine.userdata.config_name_left_right = 'gantryPosPlaceLeftRight'

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:86 y:86
			OperatableStateMachine.add('inspect_arm_part_type_right',
										self.use_behavior(inspect_arm_part_type_rightSM, 'inspect_arm_part_type_right'),
										transitions={'gasket_part': 'MoveToGasketBin', 'no_part': 'inspect_arm_part_type_left', 'piston_rod_part': 'MoveToPistonBin'},
										autonomy={'gasket_part': Autonomy.Inherit, 'no_part': Autonomy.Inherit, 'piston_rod_part': Autonomy.Inherit},
										remapping={'part_type_right': 'part_type_right', 'part_type_left': 'part_type_left'})

			# x:347 y:38
			OperatableStateMachine.add('MoveToPistonBin',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'GetPoseBin1', 'planning_failed': 'failed', 'control_failed': 'GetPoseBin1', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_right_left', 'move_group': 'move_group_gantry', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:348 y:161
			OperatableStateMachine.add('MoveToGasketBin',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'GetPoseBin2', 'planning_failed': 'failed', 'control_failed': 'GetPoseBin2', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_left_right', 'move_group': 'move_group_gantry', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:675 y:36
			OperatableStateMachine.add('ComputeDropPartPiston',
										ComputeDropAriacState(joint_names=['right_shoulder_pan_joint', 'right_shoulder_lift_joint', 'right_elbow_joint', 'right_wrist_1_joint', 'right_wrist_2_joint', 'right_wrist_3_joint']),
										transitions={'continue': 'MoveToPlacePiston', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group_right_arm', 'move_group_prefix': 'move_group_prefix', 'tool_link': 'tool_link_right', 'pose': 'poseBin1', 'offset': 'bin1_offset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:675 y:161
			OperatableStateMachine.add('ComputeDropPartGasket',
										ComputeDropAriacState(joint_names=['right_shoulder_pan_joint', 'right_shoulder_lift_joint', 'right_elbow_joint', 'right_wrist_1_joint', 'right_wrist_2_joint', 'right_wrist_3_joint']),
										transitions={'continue': 'MoveToPlaceGasket', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group_right_arm', 'move_group_prefix': 'move_group_prefix', 'tool_link': 'tool_link_right', 'pose': 'poseBin2', 'offset': 'bin2_offset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:860 y:37
			OperatableStateMachine.add('MoveToPlacePiston',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'DisableGripperPiston', 'planning_failed': 'ComputeDropPartPiston', 'control_failed': 'DisableGripperPiston'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'move_group_right_arm', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:869 y:158
			OperatableStateMachine.add('MoveToPlaceGasket',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'DisableGripperGasket', 'planning_failed': 'ComputeDropPartGasket', 'control_failed': 'DisableGripperGasket'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'move_group_right_arm', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1080 y:38
			OperatableStateMachine.add('DisableGripperPiston',
										GripperControl(enable=False),
										transitions={'continue': 'MoveRightHome', 'failed': 'failed', 'invalid_id': 'MoveToPlacePiston'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'invalid_id': Autonomy.Off},
										remapping={'arm_id': 'arm1'})

			# x:1086 y:154
			OperatableStateMachine.add('DisableGripperGasket',
										GripperControl(enable=False),
										transitions={'continue': 'MoveRightHome_2', 'failed': 'failed', 'invalid_id': 'MoveToPlaceGasket'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'invalid_id': Autonomy.Off},
										remapping={'arm_id': 'arm1'})

			# x:1243 y:36
			OperatableStateMachine.add('MoveRightHome',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'AddOffsetBin1', 'planning_failed': 'failed', 'control_failed': 'AddOffsetBin1', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_right_home', 'move_group': 'move_group_right_arm', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1251 y:150
			OperatableStateMachine.add('MoveRightHome_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'AddOffsetBin2', 'planning_failed': 'failed', 'control_failed': 'AddOffsetBin2', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_right_home', 'move_group': 'move_group_right_arm', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1405 y:510
			OperatableStateMachine.add('inspect_arm_part_type_left',
										self.use_behavior(inspect_arm_part_type_leftSM, 'inspect_arm_part_type_left'),
										transitions={'gasket_part': 'MoveToGasketBinLeft', 'no_part': 'finished', 'piston_rod_part': 'MoveToPistonBinLeft'},
										autonomy={'gasket_part': Autonomy.Inherit, 'no_part': Autonomy.Inherit, 'piston_rod_part': Autonomy.Inherit},
										remapping={'part_type_right': 'part_type_right', 'part_type_left': 'part_type_left'})

			# x:1188 y:444
			OperatableStateMachine.add('MoveToPistonBinLeft',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'GetPoseBin1Left', 'planning_failed': 'failed', 'control_failed': 'GetPoseBin1Left', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_left_right', 'move_group': 'move_group_gantry', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1197 y:594
			OperatableStateMachine.add('MoveToGasketBinLeft',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'GetPoseBin2_2', 'planning_failed': 'failed', 'control_failed': 'GetPoseBin2_2', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_right_left', 'move_group': 'move_group_gantry', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:792 y:449
			OperatableStateMachine.add('ComputeDropPartPistonLeft',
										ComputeDropAriacState(joint_names=['left_shoulder_pan_joint', 'left_shoulder_lift_joint', 'left_elbow_joint', 'left_wrist_1_joint', 'left_wrist_2_joint', 'left_wrist_3_joint']),
										transitions={'continue': 'MoveToPlacePistonLeft', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group_left_arm', 'move_group_prefix': 'move_group_prefix', 'tool_link': 'tool_link_left', 'pose': 'poseBin1', 'offset': 'bin1_offset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:810 y:591
			OperatableStateMachine.add('ComputeDropPartGasketLeft',
										ComputeDropAriacState(joint_names=['left_shoulder_pan_joint', 'left_shoulder_lift_joint', 'left_elbow_joint', 'left_wrist_1_joint', 'left_wrist_2_joint', 'left_wrist_3_joint']),
										transitions={'continue': 'MoveToPlaceGasketLeft', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group_left_arm', 'move_group_prefix': 'move_group_prefix', 'tool_link': 'tool_link_left', 'pose': 'poseBin2', 'offset': 'bin2_offset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:585 y:448
			OperatableStateMachine.add('MoveToPlacePistonLeft',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'DisableGripperPistonLeft', 'planning_failed': 'ComputeDropPartPistonLeft', 'control_failed': 'DisableGripperPistonLeft'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'move_group_left_arm', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:581 y:590
			OperatableStateMachine.add('MoveToPlaceGasketLeft',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'DisableGripperGasketLeft', 'planning_failed': 'ComputeDropPartGasketLeft', 'control_failed': 'DisableGripperGasketLeft'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'move_group_left_arm', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:393 y:446
			OperatableStateMachine.add('DisableGripperPistonLeft',
										GripperControl(enable=False),
										transitions={'continue': 'MoveLeftHome', 'failed': 'failed', 'invalid_id': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'invalid_id': Autonomy.Off},
										remapping={'arm_id': 'arm2'})

			# x:390 y:589
			OperatableStateMachine.add('DisableGripperGasketLeft',
										GripperControl(enable=False),
										transitions={'continue': 'MoveLeftHome_2', 'failed': 'failed', 'invalid_id': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'invalid_id': Autonomy.Off},
										remapping={'arm_id': 'arm2'})

			# x:225 y:590
			OperatableStateMachine.add('MoveLeftHome_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'AddOffsetBin2_2', 'planning_failed': 'failed', 'control_failed': 'AddOffsetBin2_2', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_left_home', 'move_group': 'move_group_left_arm', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:219 y:444
			OperatableStateMachine.add('MoveLeftHome',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'AddOffsetBin1_2', 'planning_failed': 'failed', 'control_failed': 'AddOffsetBin1_2', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_left_home', 'move_group': 'move_group_left_arm', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:512 y:36
			OperatableStateMachine.add('GetPoseBin1',
										GetObjectPoseState(object_frame='bin1_frame', ref_frame='world'),
										transitions={'continue': 'ComputeDropPartPiston', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'poseBin1'})

			# x:1407 y:36
			OperatableStateMachine.add('AddOffsetBin1',
										AddNumericState(),
										transitions={'done': 'inspect_arm_part_type_left'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'bin1_offset', 'value_b': 'iterator', 'result': 'bin1_offset'})

			# x:516 y:160
			OperatableStateMachine.add('GetPoseBin2',
										GetObjectPoseState(object_frame='bin2_frame', ref_frame='world'),
										transitions={'continue': 'ComputeDropPartGasket', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'poseBin2'})

			# x:1412 y:148
			OperatableStateMachine.add('AddOffsetBin2',
										AddNumericState(),
										transitions={'done': 'inspect_arm_part_type_left'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'bin2_offset', 'value_b': 'iterator', 'result': 'bin2_offset'})

			# x:1010 y:446
			OperatableStateMachine.add('GetPoseBin1Left',
										GetObjectPoseState(object_frame='bin1_frame', ref_frame='world'),
										transitions={'continue': 'ComputeDropPartPistonLeft', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'poseBin1'})

			# x:1011 y:591
			OperatableStateMachine.add('GetPoseBin2_2',
										GetObjectPoseState(object_frame='bin2_frame', ref_frame='world'),
										transitions={'continue': 'ComputeDropPartGasketLeft', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'poseBin2'})

			# x:34 y:439
			OperatableStateMachine.add('AddOffsetBin1_2',
										AddNumericState(),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'bin1_offset', 'value_b': 'iterator', 'result': 'bin1_offset'})

			# x:39 y:583
			OperatableStateMachine.add('AddOffsetBin2_2',
										AddNumericState(),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'bin2_offset', 'value_b': 'iterator', 'result': 'bin2_offset'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
