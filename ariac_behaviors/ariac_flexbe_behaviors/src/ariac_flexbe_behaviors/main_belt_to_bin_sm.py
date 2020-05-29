#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.start_assignment_state import StartAssignment
from ariac_flexbe_states.set_conveyorbelt_power_state import SetConveyorbeltPowerState
from ariac_flexbe_behaviors.move_home_belt_sm import move_home_beltSM
from ariac_flexbe_behaviors.detect_product_belt_sm import detect_product_beltSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Fri May 29 2020
@author: Wessel Koolen
'''
class main_belt_to_binSM(Behavior):
	'''
	Main behavior for controlling supply line
	'''


	def __init__(self):
		super(main_belt_to_binSM, self).__init__()
		self.name = 'main_belt_to_bin'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(move_home_beltSM, 'move_home_belt')
		self.add_behavior(detect_product_beltSM, 'detect_product_belt')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:740 y:372, x:130 y:365
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.powerOn = 100
		_state_machine.userdata.powerOff = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:39 y:40
			OperatableStateMachine.add('ExecuteMainBeltBin',
										StartAssignment(),
										transitions={'continue': 'ConveyorPowerOn'},
										autonomy={'continue': Autonomy.Off})

			# x:195 y:41
			OperatableStateMachine.add('ConveyorPowerOn',
										SetConveyorbeltPowerState(),
										transitions={'continue': 'move_home_belt', 'fail': 'failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'power': 'powerOn'})

			# x:384 y:41
			OperatableStateMachine.add('move_home_belt',
										self.use_behavior(move_home_beltSM, 'move_home_belt'),
										transitions={'finished': 'detect_product_belt', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:576 y:42
			OperatableStateMachine.add('detect_product_belt',
										self.use_behavior(detect_product_beltSM, 'detect_product_belt'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'part_type': 'part_type', 'pose': 'pose'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
