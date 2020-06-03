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
from ariac_flexbe_behaviors.move_to_part_belt_left_arm_sm import move_to_part_belt_left_armSM
from ariac_flexbe_states.end_assignment_state import EndAssignment
from ariac_flexbe_behaviors.inspect_arm_part_type_right_sm import inspect_arm_part_type_rightSM
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
		self.add_behavior(enable_grippersSM, 'enable_grippers')
		self.add_behavior(move_home_beltSM, 'move_home_belt')
		self.add_behavior(detect_product_beltSM, 'detect_product_belt')
		self.add_behavior(move_to_part_belt_right_armSM, 'move_to_part_belt_right_arm')
		self.add_behavior(detect_product_beltSM, 'detect_product_belt_repeat')
		self.add_behavior(move_to_part_belt_left_armSM, 'move_to_part_belt_left_arm')
		self.add_behavior(inspect_arm_part_type_rightSM, 'inspect_arm_part_type_right')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:77 y:547, x:458 y:377
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.powerOn = 100
		_state_machine.userdata.powerOff = 0
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
		_state_machine.userdata.config_name_left = 'Left_Home'
		_state_machine.userdata.move_group_right = 'Right_Arm'
		_state_machine.userdata.move_group_left = 'Left_Arm'
		_state_machine.userdata.config_name_grasp_left = 'beltPreGrasp2'
		_state_machine.userdata.part_type_left = ''
		_state_machine.userdata.part_type_right = ''

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
										transitions={'reached': 'move_to_part_belt_right_arm', 'planning_failed': 'detect_product_belt', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_grasp_right', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1156 y:45
			OperatableStateMachine.add('MoveRightSafety',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'BeltPreGraspLeft', 'planning_failed': 'failed', 'control_failed': 'BeltPreGraspLeft', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_right', 'move_group': 'move_group_right', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1158 y:124
			OperatableStateMachine.add('BeltPreGraspLeft',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'ConveyorPowerOnRepeat', 'planning_failed': 'failed', 'control_failed': 'ConveyorPowerOnRepeat', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_grasp_left', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1137 y:215
			OperatableStateMachine.add('ConveyorPowerOnRepeat',
										SetConveyorbeltPowerState(),
										transitions={'continue': 'detect_product_belt_repeat', 'fail': 'failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'power': 'powerOn'})

			# x:1105 y:301
			OperatableStateMachine.add('detect_product_belt_repeat',
										self.use_behavior(detect_product_beltSM, 'detect_product_belt_repeat'),
										transitions={'finished': 'move_to_part_belt_left_arm', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'part_type': 'part_type', 'pose': 'pose'})

			# x:39 y:40
			OperatableStateMachine.add('ExecuteMainBeltBin',
										StartAssignment(),
										transitions={'continue': 'ConveyorPowerOn'},
										autonomy={'continue': Autonomy.Off})

			# x:1106 y:393
			OperatableStateMachine.add('move_to_part_belt_left_arm',
										self.use_behavior(move_to_part_belt_left_armSM, 'move_to_part_belt_left_arm'),
										transitions={'finished': 'MoveLeftSafety', 'failed': 'failed', 'unkown_id': 'detect_product_belt_repeat'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'unkown_id': Autonomy.Inherit},
										remapping={'part_type': 'part_type', 'pose': 'pose', 'joint_values': 'joint_values', 'part_type_left': 'part_type_left'})

			# x:1159 y:478
			OperatableStateMachine.add('MoveLeftSafety',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'inspect_arm_part_type_right', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_left', 'move_group': 'move_group_left', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:192 y:563
			OperatableStateMachine.add('EndAssignment',
										EndAssignment(),
										transitions={'continue': 'finished'},
										autonomy={'continue': Autonomy.Off})

			# x:1098 y:567
			OperatableStateMachine.add('inspect_arm_part_type_right',
										self.use_behavior(inspect_arm_part_type_rightSM, 'inspect_arm_part_type_right'),
										transitions={'gasket_part': 'EndAssignment', 'failed': 'failed', 'piston_rod_part': 'EndAssignment'},
										autonomy={'gasket_part': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'piston_rod_part': Autonomy.Inherit},
										remapping={'part_type_right': 'part_type_right', 'part_type_left': 'part_type_left'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
