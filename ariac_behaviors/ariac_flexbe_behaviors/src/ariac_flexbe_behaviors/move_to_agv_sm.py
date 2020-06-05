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
		# x:757 y:738, x:130 y:406
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['agv_id'])
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
										transitions={'reached': 'gripper disabble', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_agv1_r', 'move_group': 'move_group_g', 'move_group_prefix': 'move_group_prefix_g', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:596 y:51
			OperatableStateMachine.add('check agv id',
										EqualState(),
										transitions={'true': 'MoveGantryagv2', 'false': 'MoveGantryagv1'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'agv_id', 'value_b': 'agv2'})

			# x:1261 y:44
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

			# x:569 y:355
			OperatableStateMachine.add('gripper active check',
										GripperActiveCheck(),
										transitions={'Left': 'finished', 'Right': 'MoveGantryagv1-2', 'failed': 'failed', 'Full': 'MoveGantryagv1-2'},
										autonomy={'Left': Autonomy.Off, 'Right': Autonomy.Off, 'failed': Autonomy.Off, 'Full': Autonomy.Off},
										remapping={'arm_id': 'arm_id', 'tool_link': 'tool_link', 'move_group': 'move_group'})

			# x:561 y:481
			OperatableStateMachine.add('MoveGantryagv1-2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'finished', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_agv1_l', 'move_group': 'move_group_g', 'move_group_prefix': 'move_group_prefix_g', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:496 y:239
			OperatableStateMachine.add('gripper disabble',
										GripperControl(enable=False),
										transitions={'continue': 'gripper active check', 'failed': 'failed', 'invalid_id': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'invalid_id': Autonomy.Off},
										remapping={'arm_id': 'arm_id_r'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
