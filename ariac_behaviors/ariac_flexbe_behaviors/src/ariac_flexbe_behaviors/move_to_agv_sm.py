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
from ariac_flexbe_behaviors.place_on_agv_sm import Place_on_agvSM
from ariac_flexbe_behaviors.place_on_agv_2_sm import Place_on_agv_2SM
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
		self.add_behavior(Place_on_agvSM, 'Place_on_agv')
		self.add_behavior(Place_on_agv_2SM, 'Place_on_agv_2')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:983 y:389, x:130 y:406
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
		_state_machine.userdata.config_name_gantry_p = 'Gantry_Home_Pick'

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

			# x:596 y:51
			OperatableStateMachine.add('check agv id',
										EqualState(),
										transitions={'true': 'Place_on_agv_2', 'false': 'Place_on_agv'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'agv_id', 'value_b': 'agv2'})

			# x:420 y:12
			OperatableStateMachine.add('MoveGantryhome band',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'check agv id', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_gantry_p', 'move_group': 'move_group_g', 'move_group_prefix': 'move_group_prefix_g', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:570 y:185
			OperatableStateMachine.add('Place_on_agv',
										self.use_behavior(Place_on_agvSM, 'Place_on_agv'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'agv_id': 'agv_id', 'pose_on_agv_l': 'pose_on_agv_l', 'pose_on_agv_r': 'pose_on_agv_r'})

			# x:1002 y:157
			OperatableStateMachine.add('Place_on_agv_2',
										self.use_behavior(Place_on_agv_2SM, 'Place_on_agv_2'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'agv_id': 'agv_id', 'pose_on_agv_l': 'pose_on_agv_l', 'pose_on_agv_r': 'pose_on_agv_r'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
