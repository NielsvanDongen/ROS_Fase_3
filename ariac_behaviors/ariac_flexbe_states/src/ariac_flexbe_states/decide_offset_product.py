#!/usr/bin/env python
import rospy

from flexbe_core import EventState, Logger

'''
Author: Wessel Koolen & Niels van Dongen 2140086
'''


class DecideOffsetProduct(EventState):
	'''
	This state decides when input gives certain part which offset will be given in return

	># part_type	string 		part name
	#> part_offset	float		part part_offset

	<= succes 			Given time has passed.
	<= unknown_id 				Example for a failure outcome.

	'''

	def __init__(self, target_time):
		# Declare outcomes, input_keys, and output_keys by calling the super constructor with the corresponding arguments.
		super(DecideOffsetProduct, self).__init__(input_keys = ['part_type'], output_keys = ['part_offset'], outcomes = ['succes', 'unknown_id'])

	def execute(self, userdata):
		# This method is called periodically while the state is active.
		# Main purpose is to check state conditions and trigger a corresponding outcome.
		# If no outcome is returned, the state will stay active.

			if self._part == 'gear_part_red':
				userdata.part_offset = 0.02
				return 'succes'
			elif self._part == 'piston_rod_part_red':
				userdata.part_offset = 0.015
				return 'succes'
			elif self._part == 'gear_part_blue':
				userdata.part_offset = 0.02
				return 'succes'
			elif self._part == 'pulley_part_red':
				userdata.part_offset = 0.08
				return 'succes'
			elif self._part == 'gasket_part_blue':
				userdata.part_offset = 0.03
				return 'succes'
			elif self._part == 'gasket_part_red':
				userdata.part_offset = 0.03
				return 'succes'
			elif self._part == 'disk_part':
				userdata.part_offset = 0.05
				return 'succes'
			else:
				return 'unknown_id'


	def on_enter(self, userdata):
		# This method is called when the state becomes active, i.e. a transition from another state to this one is taken.
		# It is primarily used to start actions which are associated with this state.

		# The following code is just for illustrating how the behavior logger works.
		# Text logged by the behavior logger is sent to the operator and displayed in the GUI.

		self._part = userdata.part_type


	def on_exit(self, userdata):
		# This method is called when an outcome is returned and another state gets active.
		# It can be used to stop possibly running processes started by on_enter.

		pass # Nothing to do in this example.


	def on_start(self):
		# This method is called when the behavior is started.
		# If possible, it is generally better to initialize used resources in the constructor
		# because if anything failed, the behavior would not even be started.

		# In this example, we use this event to set the correct start time.
		pass


	def on_stop(self):
		# This method is called whenever the behavior stops execution, also if it is cancelled.
		# Use this event to clean up things like claimed resources.

		pass # Nothing to do in this example.
