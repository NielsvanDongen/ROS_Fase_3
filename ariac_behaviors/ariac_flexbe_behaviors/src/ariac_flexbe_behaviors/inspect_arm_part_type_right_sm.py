#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_support_flexbe_states.equal_state import EqualState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Jun 03 2020
@author: wessel koolen
'''
class inspect_arm_part_type_rightSM(Behavior):
	'''
	this behavior checks both arms with the parts that theyre holding
	'''


	def __init__(self):
		super(inspect_arm_part_type_rightSM, self).__init__()
		self.name = 'inspect_arm_part_type_right'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:591 y:70, x:447 y:331, x:137 y:250
		_state_machine = OperatableStateMachine(outcomes=['gasket_part', 'no_part', 'piston_rod_part'], input_keys=['part_type_right', 'part_type_left'])
		_state_machine.userdata.piston_part = 'piston_rod_part_red'
		_state_machine.userdata.gasket_part = 'gasket_part_blue'
		_state_machine.userdata.part_type_right = ''
		_state_machine.userdata.part_type_left = ''

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:74 y:41
			OperatableStateMachine.add('CheckRobot1',
										EqualState(),
										transitions={'true': 'piston_rod_part', 'false': 'CheckRobot1Again'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'part_type_right', 'value_b': 'piston_part'})

			# x:268 y:41
			OperatableStateMachine.add('CheckRobot1Again',
										EqualState(),
										transitions={'true': 'gasket_part', 'false': 'no_part'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'part_type_right', 'value_b': 'gasket_part'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
