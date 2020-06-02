#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.decide_offset_product import DecideOffsetProduct
from ariac_flexbe_states.gripper_control_state import GripperControl
from ariac_flexbe_states.compute_grasp_ariac_state import ComputeGraspAriacState
from ariac_flexbe_states.moveit_to_joints_dyn_ariac_state import MoveitToJointsDynAriacState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue Jun 02 2020
@author: Wessel Koolen
'''
class move_to_part_belt_right_armSM(Behavior):
	'''
	This behavior uses part information to move to an allocated spot, here the robot picks up that part
	'''


	def __init__(self):
		super(move_to_part_belt_right_armSM, self).__init__()
		self.name = 'move_to_part_belt_right_arm'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1203 y:331, x:356 y:305, x:344 y:207
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'unkown_id'], input_keys=['part_type', 'pose', 'joint_values'], output_keys=['part_type_r'])
		_state_machine.userdata.part_type = ''
		_state_machine.userdata.pose = []
		_state_machine.userdata.move_group = 'Right_Arm'
		_state_machine.userdata.move_group_prefix = '/ariac/gantry'
		_state_machine.userdata.tool_link = 'right_ee_link'
		_state_machine.userdata.part_offset = 0
		_state_machine.userdata.rotation = 0
		_state_machine.userdata.joint_values = []
		_state_machine.userdata.joint_names = []
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.arm_id = 'Right_Arm'
		_state_machine.userdata.part_type_r = ''
		_state_machine.userdata.robot_name = ''

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:250 y:36
			OperatableStateMachine.add('DecideOffset',
										DecideOffsetProduct(target_time=0.5),
										transitions={'succes': 'ComputePick', 'unknown_id': 'unkown_id'},
										autonomy={'succes': Autonomy.Off, 'unknown_id': Autonomy.Off},
										remapping={'part_type': 'part_type', 'part_offset': 'part_offset'})

			# x:816 y:35
			OperatableStateMachine.add('EnableGripper',
										GripperControl(enable=True),
										transitions={'continue': 'finished', 'failed': 'failed', 'invalid_id': 'unkown_id'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'invalid_id': Autonomy.Off},
										remapping={'arm_id': 'arm_id'})

			# x:414 y:36
			OperatableStateMachine.add('ComputePick',
										ComputeGraspAriacState(joint_names=['right_elbow_joint', 'right_shoulder_lift_joint', 'right_shoulder_pan_joint', 'right_wrist_1_joint', 'right_wrist_2_joint', 'right_wrist_2_joint']),
										transitions={'continue': 'MoveToPartBelt', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'tool_link': 'tool_link', 'pose': 'pose', 'offset': 'part_offset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:593 y:33
			OperatableStateMachine.add('MoveToPartBelt',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'EnableGripper', 'planning_failed': 'failed', 'control_failed': 'EnableGripper'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'move_group', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
