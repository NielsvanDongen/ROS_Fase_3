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
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon May 25 2020
@author: Wessel Koolen
'''
class move_product_to_warehouseSM(Behavior):
	'''
	Behavior for supplying the warehouse
	'''


	def __init__(self):
		super(move_product_to_warehouseSM, self).__init__()
		self.name = 'move_product_to_warehouse'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:631 y:281, x:242 y:360
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.powerOn = 100

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:30 y:40
			OperatableStateMachine.add('StartAssignment',
										StartAssignment(),
										transitions={'continue': 'TurnOnConveyor'},
										autonomy={'continue': Autonomy.Off})

			# x:169 y:40
			OperatableStateMachine.add('TurnOnConveyor',
										SetConveyorbeltPowerState(),
										transitions={'continue': 'finished', 'fail': 'failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'power': 'powerOn'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
