#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.detect_first_part_camera_ariac_state import DetectFirstPartCameraAriacState
from flexbe_states.wait_state import WaitState
from ariac_flexbe_states.set_conveyorbelt_power_state import SetConveyorbeltPowerState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Fri May 29 2020
@author: Wessel Koolen
'''
class detect_productSM(Behavior):
	'''
	Behavior for moving to detected part
	'''


	def __init__(self):
		super(detect_productSM, self).__init__()
		self.name = 'detect_product'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:537 y:364, x:130 y:365
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.ref_frame = 'world'
		_state_machine.userdata.camera_topic = '/ariac/logical_camera_6'
		_state_machine.userdata.camera_frame = 'logical_camera_6_frame'
		_state_machine.userdata.powerOff = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:30 y:40
			OperatableStateMachine.add('DetectFirstProduct',
										DetectFirstPartCameraAriacState(part_list=['piston_rod_part_red', 'gasket_part_blue'], time_out=0.5),
										transitions={'continue': 'TurnConveyorOff', 'failed': 'failed', 'not_found': 'WaitRetry'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ref_frame': 'ref_frame', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame', 'part': 'part_type', 'pose': 'pose'})

			# x:119 y:111
			OperatableStateMachine.add('WaitRetry',
										WaitState(wait_time=0.5),
										transitions={'done': 'DetectFirstProduct'},
										autonomy={'done': Autonomy.Off})

			# x:238 y:42
			OperatableStateMachine.add('TurnConveyorOff',
										SetConveyorbeltPowerState(),
										transitions={'continue': 'DetectFirstProductRetry', 'fail': 'failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'power': 'powerOff'})

			# x:419 y:41
			OperatableStateMachine.add('DetectFirstProductRetry',
										DetectFirstPartCameraAriacState(part_list=['piston_rod_part_red', 'gasket_part_blue'], time_out=0.5),
										transitions={'continue': 'finished', 'failed': 'failed', 'not_found': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ref_frame': 'ref_frame', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame', 'part': 'part_type', 'pose': 'pose'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
