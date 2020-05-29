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
from ariac_flexbe_states.compute_grasp_ariac_state import ComputeGraspAriacState
from flexbe_states.wait_state import WaitState
from ariac_flexbe_states.moveit_to_joints_dyn_ariac_state import MoveitToJointsDynAriacState
from ariac_flexbe_states.detect_first_part_camera_ariac_state import DetectFirstPartCameraAriacState
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
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
		# x:1227 y:622, x:267 y:397
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.powerOn = 100
		_state_machine.userdata.move_group_g = 'Gantry'
		_state_machine.userdata.move_group_prefix = '/ariac/gantry'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.robot_name = ''
		_state_machine.userdata.joint_values = []
		_state_machine.userdata.joint_names = []
		_state_machine.userdata.powerOff = 0
		_state_machine.userdata.ref_frame = 'world'
		_state_machine.userdata.camera_topic = '/ariac/logical_camera_6'
		_state_machine.userdata.camera_frame = 'logical_camera_6_frame'
		_state_machine.userdata.pose = []
		_state_machine.userdata.camera_topic_7 = '/ariac/logical_camera_7'
		_state_machine.userdata.camera_frame_7 = 'logical_camera_7_frame'
		_state_machine.userdata.part_offset = 0
		_state_machine.userdata.rotation = 0
		_state_machine.userdata.tool_link = 'right_ee_link'
		_state_machine.userdata.config_name_pregrasp = 'beltPreGrasp'
		_state_machine.userdata.part_type = ''
		_state_machine.userdata.move_group = 'Right_Arm'
		_state_machine.userdata.joint_names_r = ['right_shoulder_pan_joint', 'right_shoulder_lift_joint', 'right_elbow_joint', 'right_wrist_1_joint', 'right_wrist_2_joint', 'right_wrist_3_joint']
		_state_machine.userdata.robot_name_g = ''

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:30 y:40
			OperatableStateMachine.add('StartAssignment',
										StartAssignment(),
										transitions={'continue': 'TurnOnConveyor'},
										autonomy={'continue': Autonomy.Off})

			# x:172 y:41
			OperatableStateMachine.add('TurnOnConveyor',
										SetConveyorbeltPowerState(),
										transitions={'continue': 'move_home_belt', 'fail': 'failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'power': 'powerOn'})

			# x:361 y:39
			OperatableStateMachine.add('move_home_belt',
										self.use_behavior(move_home_beltSM, 'move_home_belt'),
										transitions={'finished': 'DetectFirstPartBelt', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:769 y:38
			OperatableStateMachine.add('TurnOffConveyor',
										SetConveyorbeltPowerState(),
										transitions={'continue': 'DetectFirstPartBelt_2', 'fail': 'failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'power': 'powerOff'})

			# x:1135 y:204
			OperatableStateMachine.add('ComputeGrasp',
										ComputeGraspAriacState(joint_names=['right_shoulder_pan_joint', 'right_shoulder_lift_joint', 'right_elbow_joint', 'right_wrist_1_joint', 'right_wrist_2_joint', 'right_wrist_3_joint']),
										transitions={'continue': 'PickProduct', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'tool_link': 'tool_link', 'pose': 'pose', 'offset': 'part_offset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:470 y:134
			OperatableStateMachine.add('WaitRetry',
										WaitState(wait_time=0.5),
										transitions={'done': 'DetectFirstPartBelt'},
										autonomy={'done': Autonomy.Off})

			# x:1120 y:284
			OperatableStateMachine.add('PickProduct',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'MoveUp', 'planning_failed': 'failed', 'control_failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'move_group', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:561 y:38
			OperatableStateMachine.add('DetectFirstPartBelt',
										DetectFirstPartCameraAriacState(part_list=['piston_rod_part_red', 'gasket_part_blue_0', 'gasket_part_blue_1', 'gasket_part_blue_2'], time_out=0.5),
										transitions={'continue': 'TurnOffConveyor', 'failed': 'WaitRetry', 'not_found': 'WaitRetry'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ref_frame': 'ref_frame', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame', 'part': 'part_type', 'pose': 'pose'})

			# x:958 y:36
			OperatableStateMachine.add('DetectFirstPartBelt_2',
										DetectFirstPartCameraAriacState(part_list=['piston_rod_part_red', 'gasket_part_blue_0', 'gasket_part_blue_1', 'gasket_part_blue_2'], time_out=0.5),
										transitions={'continue': 'MovePreGraspBelt', 'failed': 'failed', 'not_found': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ref_frame': 'ref_frame', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame', 'part': 'part_type', 'pose': 'pose'})

			# x:1164 y:36
			OperatableStateMachine.add('MovePreGraspBelt',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'ComputeGrasp', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_pregrasp', 'move_group': 'move_group_g', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name_g', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1147 y:439
			OperatableStateMachine.add('MoveUp',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'finished', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_pregrasp', 'move_group': 'move_group_g', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name_g', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
