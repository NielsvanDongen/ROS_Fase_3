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
from ariac_flexbe_states.detect_part_camera_ariac_state import DetectPartCameraAriacState
from ariac_flexbe_states.compute_grasp_ariac_state import ComputeGraspAriacState
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
		_state_machine.userdata.config_name_Home = 'Gantry_Home'
		_state_machine.userdata.move_group = 'Gantry'
		_state_machine.userdata.move_group_prefix = '/ariac/gantry'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.robot_name = 'gantry'
		_state_machine.userdata.joint_values = []
		_state_machine.userdata.joint_names_left = ['left_elbow_joint', 'left_shoulder_lift_joint', 'left_shoulder_pan_joint', 'left_wrist_1_joint', 'left_wrist_2_joint', 'left_wrist_3_joint']
		_state_machine.userdata.powerOff = 0
		_state_machine.userdata.ref_frame = 'torso_main'
		_state_machine.userdata.camera_topic = '/ariac/logical_camera_6'
		_state_machine.userdata.camera_frame = 'logical_camera_6_frame'
		_state_machine.userdata.part_type = ''
		_state_machine.userdata.pose = []
		_state_machine.userdata.camera_topic_7 = '/ariac/logical_camera_7'
		_state_machine.userdata.camera_frame_7 = 'logical_camera_7_frame'
		_state_machine.userdata.offset = 0
		_state_machine.userdata.rotation = 0
		_state_machine.userdata.tool_link = ''

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
										transitions={'continue': 'CameraDetectPartPoseCamera6', 'fail': 'failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'power': 'powerOn'})

			# x:178 y:38
			OperatableStateMachine.add('move_home_belt',
										self.use_behavior(move_home_beltSM, 'move_home_belt'),
										transitions={'finished': 'TurnOnConveyor', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:554 y:37
			OperatableStateMachine.add('CameraDetectPartPoseCamera6',
										DetectFirstPartCameraAriacState(part_list=['piston_rod_part_red', 'piston_rod_part_red_1', 'piston_rod_part_red_2', 'gasket_part_blue_0', 'gasket_part_blue_1', 'gasket_part_blue_2'], time_out=0.5),
										transitions={'continue': 'TurnOffConveyor', 'failed': 'CameraDetectPartPoseCamera7', 'not_found': 'CameraDetectPartPoseCamera7'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ref_frame': 'ref_frame', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame', 'part': 'part_type', 'pose': 'pose'})

			# x:769 y:38
			OperatableStateMachine.add('TurnOffConveyor',
										SetConveyorbeltPowerState(),
										transitions={'continue': 'CameraRefreshPose', 'fail': 'failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'power': 'powerOff'})

			# x:946 y:38
			OperatableStateMachine.add('CameraRefreshPose',
										DetectPartCameraAriacState(time_out=0.5),
										transitions={'continue': 'ComputeGrasp', 'failed': 'failed', 'not_found': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ref_frame': 'ref_frame', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame', 'part': 'part_type', 'pose': 'pose'})

			# x:554 y:129
			OperatableStateMachine.add('CameraDetectPartPoseCamera7',
										DetectFirstPartCameraAriacState(part_list=['piston_rod_part_red', 'piston_rod_part_red_1', 'piston_rod_part_red_2', 'gasket_part_blue_0', 'gasket_part_blue_1', 'gasket_part_blue_2'], time_out=0.5),
										transitions={'continue': 'TurnOffConveyor', 'failed': 'CameraDetectPartPoseCamera6', 'not_found': 'CameraDetectPartPoseCamera6'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ref_frame': 'ref_frame', 'camera_topic': 'camera_topic_7', 'camera_frame': 'camera_frame_7', 'part': 'part_type', 'pose': 'pose'})

			# x:1137 y:37
			OperatableStateMachine.add('ComputeGrasp',
										ComputeGraspAriacState(joint_names=['left_elbow_joint', 'left_shoulder_lift_joint', 'left_shoulder_pan_joint', 'left_wrist_1_joint', 'left_wrist_2_joint', 'left_wrist_3_joint']),
										transitions={'continue': 'finished', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'tool_link': 'tool_link', 'pose': 'pose', 'offset': 'offset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
