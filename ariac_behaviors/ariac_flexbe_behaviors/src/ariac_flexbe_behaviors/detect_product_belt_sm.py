#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_support_flexbe_states.replace_state import ReplaceState
from flexbe_states.wait_state import WaitState
from ariac_flexbe_states.set_conveyorbelt_power_state import SetConveyorbeltPowerState
from ariac_flexbe_states.detect_first_part_camera_ariac_state import DetectFirstPartCameraAriacState
from ariac_support_flexbe_states.add_numeric_state import AddNumericState
from flexbe_states.check_condition_state import CheckConditionState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Fri May 29 2020
@author: Wessel Koolen
'''
class detect_product_beltSM(Behavior):
	'''
	Behavior for moving to detected part
	'''


	def __init__(self):
		super(detect_product_beltSM, self).__init__()
		self.name = 'detect_product_belt'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:537 y:364, x:433 y:362, x:430 y:252
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'no_products_belt'], output_keys=['part_type', 'pose'])
		_state_machine.userdata.ref_frame = 'world'
		_state_machine.userdata.camera_topic = '/ariac/logical_camera_6'
		_state_machine.userdata.camera_frame = 'logical_camera_6_frame'
		_state_machine.userdata.powerOff = 0
		_state_machine.userdata.part_type = ''
		_state_machine.userdata.pose = []
		_state_machine.userdata.retries = 0
		_state_machine.userdata.plus = 1
		_state_machine.userdata.zero = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:77 y:33
			OperatableStateMachine.add('ZeroTics',
										ReplaceState(),
										transitions={'done': 'DetectFirstProduct'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'zero', 'result': 'retries'})

			# x:233 y:137
			OperatableStateMachine.add('WaitRetry',
										WaitState(wait_time=0.1),
										transitions={'done': 'CountCameraTics'},
										autonomy={'done': Autonomy.Off})

			# x:505 y:34
			OperatableStateMachine.add('TurnConveyorOff',
										SetConveyorbeltPowerState(),
										transitions={'continue': 'DetectFirstProductRetry', 'fail': 'failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'power': 'powerOff'})

			# x:708 y:56
			OperatableStateMachine.add('DetectFirstProductRetry',
										DetectFirstPartCameraAriacState(part_list=['piston_rod_part_red', 'gasket_part_blue'], time_out=0.5),
										transitions={'continue': 'finished', 'failed': 'failed', 'not_found': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ref_frame': 'ref_frame', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame', 'part': 'part_type', 'pose': 'pose'})

			# x:242 y:249
			OperatableStateMachine.add('CountCameraTics',
										AddNumericState(),
										transitions={'done': 'CheckCameraTics'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'retries', 'value_b': 'plus', 'result': 'retries'})

			# x:348 y:139
			OperatableStateMachine.add('CheckCameraTics',
										CheckConditionState(predicate=15),
										transitions={'true': 'no_products_belt', 'false': 'DetectFirstProduct'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'retries'})

			# x:276 y:34
			OperatableStateMachine.add('DetectFirstProduct',
										DetectFirstPartCameraAriacState(part_list=['piston_rod_part_red', 'gasket_part_blue'], time_out=0.1),
										transitions={'continue': 'TurnConveyorOff', 'failed': 'WaitRetry', 'not_found': 'WaitRetry'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ref_frame': 'ref_frame', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame', 'part': 'part_type', 'pose': 'pose'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
