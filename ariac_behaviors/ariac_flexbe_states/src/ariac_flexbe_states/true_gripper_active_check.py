#!/usr/bin/env python
import rospy
import rostopic

from flexbe_core import EventState, Logger
from nist_gear.msg import VacuumGripperState
from nist_gear.srv import VacuumGripperControl, VacuumGripperControlRequest, VacuumGripperControlResponse
from std_msgs.msg import String

# Authors: Niels van Dongen

class TrueGripperActiveCheck(EventState):
	'''
	This state is used for enabling and disabling the gripper used on both robotarms



	<= continue 			The left gripper already has a product attached.
	<= failed 			The left gripper is empty.
	<= arm_id	string		The arm id that is empty.
	<= tool_link	string		The tool link that will be used.
	<= move_group	string		The move group thats need to move.
	#> joint_names	string[]	names of the joints

	'''

	def __init__(self):
		# Declare outcomes, input_keys, and output_keys by calling the super constructor with the corresponding arguments.
		super(TrueGripperActiveCheck, self).__init__(outcomes = ['Left', 'Right', 'failed', 'Full'], output_keys = ['arm_id','tool_link','move_group'])

		# Store state parameter for later use.

	
		# The constructor is called when building the state machine, not when actually starting the behavior.
		# Thus, we cannot save the starting time now and will do so later.


	def execute(self, userdata):
		#gripper_service_l = '/ariac/gantry/left_arm/gripper/control'
		#gripper_service_r = '/ariac/gantry/right_arm/gripper/control'

		#rospy.loginfo("Waiting for service")
		#rospy.wait_for_service(gripper_service_l)
		#rospy.wait_for_service(gripper_service_r)
		#service_response = gripper_control(request)

		#if service_response.success == True:
		status_l = rospy.wait_for_message('/ariac/gantry/left_arm/gripper/state', VacuumGripperState)
		status_r = rospy.wait_for_message('/ariac/gantry/right_arm/gripper/state', VacuumGripperState)
		if status_r.attached == True:
			userdata.arm_id = "Right_Arm"
			userdata.tool_link = "right_ee_link"
			userdata.move_group = "Right_Arm"
			return 'Right'

		elif status_l.attached == True:
			userdata.arm_id = "Left_Arm"
			userdata.tool_link = "left_ee_link"
			userdata.move_group = "Left_Arm"
			return 'Left'
		else: 
			return 'Full'
		
	


		# This method is called periodically while the state is active.
		# Main purpose is to check state conditions and trigger a corresponding outcome.
		# If no outcome is returned, the state will stay active.
		pass # Nothing to do in this example.


	def on_exit(self, userdata):
		# This method is called when an outcome is returned and another state gets active.
		# It can be used to stop possibly running processes started by on_enter.

		pass # Nothing to do in this example.


	def on_start(self):
		# This method is called when the behavior is started.
		# If possible, it is generally better to initialize used resources in the constructor
		# because if anything failed, the behavior would not even be started.

		# In this example, we use this event to set the correct start time.
		pass #nothing in this example


	def on_stop(self):
		# This method is called whenever the behavior stops execution, also if it is cancelled.
		# Use this event to clean up things like claimed resources.

		pass # Nothing to do in this example.
