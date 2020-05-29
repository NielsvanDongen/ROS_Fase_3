#!/usr/bin/env python
import rospy
import rostopic

from flexbe_core import EventState, Logger
from nist_gear.msg import VacuumGripperState
from nist_gear.srv import VacuumGripperControl, VacuumGripperControlRequest, VacuumGripperControlResponse
from std_msgs.msg import String

# Authors: Wessel Koolen & Niels van Dongen

class GripperControl(EventState):
	'''
	This state is used for enabling and disabling the gripper used on both robotarms

	-- enable 	bool 		Enables the vacuum gripper True of False

	#> arm_id	string		Arm identifier.

	<= continue 			Given time has passed.
	<= failed 				Example for a failure outcome.
	<= invalid_id			arm_id invalid

	'''

	def __init__(self, enable):
		# Declare outcomes, input_keys, and output_keys by calling the super constructor with the corresponding arguments.
		super(GripperControl, self).__init__(input_keys = ['arm_id'], outcomes = ['continue', 'failed', 'invalid_id'])

		# Store state parameter for later use.

		self._enable = enable
		# The constructor is called when building the state machine, not when actually starting the behavior.
		# Thus, we cannot save the starting time now and will do so later.


	def execute(self, userdata):
		if userdata.arm_id == 'Left_Arm':
			gripper_service = '/ariac/Left_Arm/gripper/control'

		elif userdata.arm_id == 'Right_Arm':
			gripper_service = '/ariac/Right_Arm/gripper/control'

		else:
			return 'invalid_id'

		rospy.loginfo("Waiting for service")
		rospy.wait_for_service(gripper_service)
		try:
			gripper_control = rospy.ServiceProxy(gripper_service, VacuumGripperControl)
			request = VacuumGripperControlRequest()
			request.enable = self._enable

			service_response = gripper_control(request)

			if service_response.success == True:
				if self._enable == True:
					if userdata.arm_id == 'Left_Arm':
						status = rospy.wait_for_message('/ariac/Left_Arm/gripper/state', VacuumGripperState)
						if status.attached == True:
							return 'continue'
					elif userdata.arm_id == 'Right_Arm':
						status = rospy.wait_for_message('/ariac/Right_Arm/gripper/state', VacuumGripperState)
						if status.attached == True:
							return 'continue'
					else:
						return 'failed'
				else:
					return 'continue'
			else:
				return 'failed'

		except rospy.ServiceException, e:
			rospy.loginfo("Service call failed: %s"%e)
			return 'failed'

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
