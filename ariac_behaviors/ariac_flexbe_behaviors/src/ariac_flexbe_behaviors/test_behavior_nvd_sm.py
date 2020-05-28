#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.find_correct_bin import FindCorrectBin
from flexbe_states.wait_state import WaitState
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_flexbe_behaviors.move_home_belt_sm import move_home_beltSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu May 27 2020
@author: Niels van Dongen
'''
class Test_behavior_nvdSM(Behavior):
	'''
	Test behavior om te testen
	'''


	def __init__(self):
		super(Test_behavior_nvdSM, self).__init__()
		self.name = 'Test_behavior_nvd'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(move_home_beltSM, 'move_home_belt')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:631 y:281, x:242 y:360
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.powerOn = 100
		_state_machine.userdata.config_name = ''
		_state_machine.userdata.move_group = 'Gantry'
		_state_machine.userdata.move_group_prefix = '/ariac/gantry'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.robot_name = 'gantry'
		_state_machine.userdata.part_type = 'pulley_part_red'
		_state_machine.userdata.joint_values = []
		_state_machine.userdata.joint_names = []

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:230 y:22
			OperatableStateMachine.add('move_home_belt',
										self.use_behavior(move_home_beltSM, 'move_home_belt'),
										transitions={'finished': 'Find_product_location', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:810 y:40
			OperatableStateMachine.add('Waitretry',
										WaitState(wait_time=2),
										transitions={'done': 'move_gantry_bin_gr1'},
										autonomy={'done': Autonomy.Off})

			# x:701 y:151
			OperatableStateMachine.add('move_gantry_bin_gr1',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'finished', 'planning_failed': 'Waitretry', 'control_failed': 'Waitretry', 'param_error': 'Waitretry'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'bin', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:559 y:28
			OperatableStateMachine.add('Find_product_location',
										FindCorrectBin(time_out=0.5),
										transitions={'continue': 'move_gantry_bin_gr1', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'part_type': 'part_type', 'bin': 'bin', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame', 'ref_frame': 'ref_frame'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
