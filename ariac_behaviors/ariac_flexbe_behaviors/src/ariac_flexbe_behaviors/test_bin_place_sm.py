#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_behaviors.enable_grippers_sm import enable_grippersSM
from ariac_flexbe_states.set_conveyorbelt_power_state import SetConveyorbeltPowerState
from ariac_flexbe_behaviors.move_home_belt_sm import move_home_beltSM
from ariac_flexbe_behaviors.detect_product_belt_sm import detect_product_beltSM
from ariac_flexbe_behaviors.move_to_part_belt_right_arm_sm import move_to_part_belt_right_armSM
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_flexbe_states.start_assignment_state import StartAssignment
from ariac_flexbe_behaviors.move_part_to_bin_sm import move_part_to_binSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu Jun 04 2020
@author: wessel koolen
'''
class test_bin_placeSM(Behavior):
	'''
	testprogramma wessel
	'''


	def __init__(self):
		super(test_bin_placeSM, self).__init__()
		self.name = 'test_bin_place'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(enable_grippersSM, 'enable_grippers')
		self.add_behavior(move_home_beltSM, 'move_home_belt')
		self.add_behavior(detect_product_beltSM, 'detect_product_belt')
		self.add_behavior(move_to_part_belt_right_armSM, 'move_to_part_belt_right_arm')
		self.add_behavior(move_part_to_binSM, 'move_part_to_bin')
		self.add_behavior(move_home_beltSM, 'move_home_belt_2')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:644 y:287
		_state_machine = OperatableStateMachine(outcomes=['failed'])
		_state_machine.userdata.powerOn = 100
		_state_machine.userdata.part_type = ''
		_state_machine.userdata.pose = []
		_state_machine.userdata.config_name_grasp_right = 'beltPreGrasp'
		_state_machine.userdata.move_group = 'Gantry'
		_state_machine.userdata.move_group_prefix = '/ariac/gantry'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.robot_name = ''
		_state_machine.userdata.joint_names = ''
		_state_machine.userdata.joint_values = []
		_state_machine.userdata.config_name_right = 'Right_Home'
		_state_machine.userdata.move_group_right = 'Right_Arm'
		_state_machine.userdata.part_type_right = ''
		_state_machine.userdata.part_type_left = ''
		_state_machine.userdata.config_name_place = 'gantryPosPlace'

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:41 y:129
			OperatableStateMachine.add('enable_grippers',
										self.use_behavior(enable_grippersSM, 'enable_grippers'),
										transitions={'finished': 'ExecuteMainBeltBin', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

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
										transitions={'finished': 'BeltPreGraspRight', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'part_type': 'part_type', 'pose': 'pose'})

			# x:926 y:44
			OperatableStateMachine.add('move_to_part_belt_right_arm',
										self.use_behavior(move_to_part_belt_right_armSM, 'move_to_part_belt_right_arm'),
										transitions={'finished': 'MoveRightSafety', 'failed': 'failed', 'unkown_id': 'BeltPreGraspRight'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'unkown_id': Autonomy.Inherit},
										remapping={'part_type': 'part_type', 'pose': 'pose', 'joint_values': 'joint_values', 'part_type_right': 'part_type_right'})

			# x:762 y:43
			OperatableStateMachine.add('BeltPreGraspRight',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'move_to_part_belt_right_arm', 'planning_failed': 'detect_product_belt', 'control_failed': 'move_to_part_belt_right_arm', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_grasp_right', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1156 y:45
			OperatableStateMachine.add('MoveRightSafety',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'moveplacepos', 'planning_failed': 'failed', 'control_failed': 'moveplacepos', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_right', 'move_group': 'move_group_right', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:39 y:40
			OperatableStateMachine.add('ExecuteMainBeltBin',
										StartAssignment(),
										transitions={'continue': 'ConveyorPowerOn'},
										autonomy={'continue': Autonomy.Off})

			# x:1156 y:193
			OperatableStateMachine.add('moveplacepos',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'move_part_to_bin', 'planning_failed': 'failed', 'control_failed': 'move_part_to_bin', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_place', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1131 y:348
			OperatableStateMachine.add('move_part_to_bin',
										self.use_behavior(move_part_to_binSM, 'move_part_to_bin'),
										transitions={'finished': 'move_home_belt_2', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'part_type_right': 'part_type_right', 'part_type_left': 'part_type_left'})

			# x:528 y:489
			OperatableStateMachine.add('move_home_belt_2',
										self.use_behavior(move_home_beltSM, 'move_home_belt_2'),
										transitions={'finished': 'ConveyorPowerOn', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
