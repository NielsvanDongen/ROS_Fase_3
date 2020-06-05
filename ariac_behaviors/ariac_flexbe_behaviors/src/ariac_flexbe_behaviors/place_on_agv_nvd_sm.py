#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_behaviors.move_home_belt_sm import move_home_beltSM
from flexbe_states.wait_state import WaitState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu May 27 2020
@author: Niels van Dongen
'''
class place_on_agv_nvdSM(Behavior):
	'''
	behavior voor plaatsten parts on agv
	'''


	def __init__(self):
		super(place_on_agv_nvdSM, self).__init__()
		self.name = 'place_on_agv_nvd'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(move_home_beltSM, 'move_home_belt')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:27 y:469, x:242 y:360
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.powerOn = 100
		_state_machine.userdata.config_name = ''
		_state_machine.userdata.move_group = 'Gantry'
		_state_machine.userdata.move_group_prefix = '/ariac/gantry'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.robot_name = 'gantry'
		_state_machine.userdata.part_type = 'gear_part_red'
		_state_machine.userdata.joint_values = []
		_state_machine.userdata.joint_names = []
		_state_machine.userdata.ref_frame = 'world'
		_state_machine.userdata.camera_topic = ''
		_state_machine.userdata.camera_frame = ''
		_state_machine.userdata.tool_link_r = 'right_ee_link'
		_state_machine.userdata.pose = ''
		_state_machine.userdata.rotation = 0
		_state_machine.userdata.move_groupR = 'Right_Arm'
		_state_machine.userdata.arm_id_r = 'Right_Arm'

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:230 y:22
			OperatableStateMachine.add('move_home_belt',
										self.use_behavior(move_home_beltSM, 'move_home_belt'),
										transitions={'finished': 'finished', 'failed': 'Waitretry'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:810 y:40
			OperatableStateMachine.add('Waitretry',
										WaitState(wait_time=2),
										transitions={'done': 'move_home_belt'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
