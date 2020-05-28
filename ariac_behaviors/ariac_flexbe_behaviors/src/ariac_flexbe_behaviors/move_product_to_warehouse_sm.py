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
from ariac_flexbe_states.detect_first_part_camera_ariac_state import DetectFirstPartCameraAriacState
from flexbe_states.wait_state import WaitState
from ariac_flexbe_states.detect_part_camera_ariac_state import DetectPartCameraAriacState
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
		self.add_behavior(move_home_beltSM, 'move_home_belt')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1220 y:329, x:267 y:397
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.powerOn = 100
		_state_machine.userdata.config_name_Home = 'Gantry_Home'
		_state_machine.userdata.move_group = 'Gantry'
		_state_machine.userdata.move_group_prefix = '/ariac/gantry'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.robot_name = 'gantry'
		_state_machine.userdata.joint_values = []
		_state_machine.userdata.joint_names = []
		_state_machine.userdata.powerOff = 0
		_state_machine.userdata.ref_frame = 'torso_main'
		_state_machine.userdata.camera_topic = '/ariac/logical_camera_6'
		_state_machine.userdata.camera_frame = 'logical_camera_6_frame'
		_state_machine.userdata.part_type = ''
		_state_machine.userdata.pose = []

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:30 y:40
			OperatableStateMachine.add('StartAssignment',
										StartAssignment(),
										transitions={'continue': 'move_home_belt'},
										autonomy={'continue': Autonomy.Off})

			# x:360 y:37
			OperatableStateMachine.add('TurnOnConveyor',
										SetConveyorbeltPowerState(),
										transitions={'continue': 'CameraDetectPartPose', 'fail': 'failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'power': 'powerOn'})

			# x:178 y:38
			OperatableStateMachine.add('move_home_belt',
										self.use_behavior(move_home_beltSM, 'move_home_belt'),
										transitions={'finished': 'TurnOnConveyor', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:554 y:37
			OperatableStateMachine.add('CameraDetectPartPose',
										DetectFirstPartCameraAriacState(part_list=['piston_rod_part_red', 'piston_rod_part_red_1', 'piston_rod_part_red_2', 'gasket_part_blue_0', 'gasket_part_blue_1', 'gasket_part_blue_2'], time_out=0.5),
										transitions={'continue': 'TurnOffConveyor', 'failed': 'WaitRetry', 'not_found': 'WaitRetry'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ref_frame': 'ref_frame', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame', 'part': 'part_type', 'pose': 'pose'})

			# x:769 y:38
			OperatableStateMachine.add('TurnOffConveyor',
										SetConveyorbeltPowerState(),
										transitions={'continue': 'CameraRefreshPose', 'fail': 'failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'power': 'powerOff'})

			# x:625 y:143
			OperatableStateMachine.add('WaitRetry',
										WaitState(wait_time=0.5),
										transitions={'done': 'CameraDetectPartPose'},
										autonomy={'done': Autonomy.Off})

			# x:946 y:38
			OperatableStateMachine.add('CameraRefreshPose',
										DetectPartCameraAriacState(time_out=0.5),
										transitions={'continue': 'finished', 'failed': 'failed', 'not_found': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ref_frame': 'ref_frame', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame', 'part': 'part_type', 'pose': 'pose'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
