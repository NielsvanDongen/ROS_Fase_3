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
from ariac_logistics_flexbe_states.get_order_state import GetOrderState
from ariac_logistics_flexbe_states.get_products_from_shipment_state import GetProductsFromShipmentState
from ariac_logistics_flexbe_states.get_part_from_products_state import GetPartFromProductsState
from ariac_flexbe_behaviors.move_home_belt_sm import move_home_beltSM
from ariac_flexbe_behaviors.order_picking_sm import Order_pickingSM
from ariac_support_flexbe_states.add_numeric_state import AddNumericState
from ariac_support_flexbe_states.equal_state import EqualState
from ariac_flexbe_states.message_state import MessageState
from ariac_flexbe_states.choice_of_location import choiceoflocation
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu May 27 2020
@author: Niels van Dongen
'''
class Main_prog_order_picking_v2SM(Behavior):
	'''
	Main program for order picking
	'''


	def __init__(self):
		super(Main_prog_order_picking_v2SM, self).__init__()
		self.name = 'Main_prog_order_picking_v2'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(move_home_beltSM, 'move_home_belt')
		self.add_behavior(Order_pickingSM, 'Order_picking')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:27 y:469, x:242 y:360
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.powerOn = 100
		_state_machine.userdata.config_name = ''
		_state_machine.userdata.move_group_g = 'Gantry'
		_state_machine.userdata.move_group_prefix = '/ariac/gantry'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.robot_name = 'gantry'
		_state_machine.userdata.joint_values = []
		_state_machine.userdata.joint_names = []
		_state_machine.userdata.ref_frame = 'world'
		_state_machine.userdata.camera_topic = ''
		_state_machine.userdata.camera_frame = ''
		_state_machine.userdata.tool_link = ''
		_state_machine.userdata.pose = ''
		_state_machine.userdata.rotation = 0
		_state_machine.userdata.move_group = ''
		_state_machine.userdata.arm_id = ''
		_state_machine.userdata.part_index = 0
		_state_machine.userdata.part_type = ''
		_state_machine.userdata.one = 1
		_state_machine.userdata.product_itt = 0
		_state_machine.userdata.shipments_index = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:64 y:31
			OperatableStateMachine.add('Start_assignment',
										StartAssignment(),
										transitions={'continue': 'move_home_belt'},
										autonomy={'continue': Autonomy.Off})

			# x:431 y:28
			OperatableStateMachine.add('get_orders',
										GetOrderState(),
										transitions={'continue': 'Get shipments'},
										autonomy={'continue': Autonomy.Off},
										remapping={'order_id': 'order_id', 'shipments': 'shipments', 'number_of_shipments': 'number_of_shipments'})

			# x:615 y:25
			OperatableStateMachine.add('Get shipments',
										GetProductsFromShipmentState(),
										transitions={'continue': 'get part', 'invalid_index': 'failed'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'shipments': 'shipments', 'index': 'shipments_index', 'shipment_type': 'shipment_type', 'agv_id': 'agv_id', 'products': 'products', 'number_of_products': 'number_of_products'})

			# x:833 y:35
			OperatableStateMachine.add('get part',
										GetPartFromProductsState(),
										transitions={'continue': 'message part main prg', 'invalid_index': 'failed'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'products': 'products', 'index': 'part_index', 'type': 'part_type', 'pose': 'pose'})

			# x:261 y:28
			OperatableStateMachine.add('move_home_belt',
										self.use_behavior(move_home_beltSM, 'move_home_belt'),
										transitions={'finished': 'get_orders', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:1278 y:406
			OperatableStateMachine.add('Order_picking',
										self.use_behavior(Order_pickingSM, 'Order_picking'),
										transitions={'finished': 'add_itterator order', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'part_type': 'part_type'})

			# x:905 y:467
			OperatableStateMachine.add('add_itterator order',
										AddNumericState(),
										transitions={'done': 'part index message'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'one', 'value_b': 'part_index', 'result': 'part_index'})

			# x:536 y:510
			OperatableStateMachine.add('Check_product_amount',
										EqualState(),
										transitions={'true': 'move_home_belt', 'false': 'Get shipments'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'number_of_products', 'value_b': 'part_index'})

			# x:1053 y:12
			OperatableStateMachine.add('message part main prg',
										MessageState(),
										transitions={'continue': 'choice point'},
										autonomy={'continue': Autonomy.Off},
										remapping={'message': 'part_type'})

			# x:750 y:504
			OperatableStateMachine.add('part index message',
										MessageState(),
										transitions={'continue': 'Check_product_amount'},
										autonomy={'continue': Autonomy.Off},
										remapping={'message': 'part_index'})

			# x:1277 y:24
			OperatableStateMachine.add('choice point',
										choiceoflocation(time_out=0.5),
										transitions={'bingr0': 'Order_picking', 'bingr1': 'Order_picking', 'bingr2': 'Order_picking', 'bingr3': 'Order_picking', 'bingr4': 'Order_picking', 'bingr5': 'Order_picking', 'failed': 'failed'},
										autonomy={'bingr0': Autonomy.Off, 'bingr1': Autonomy.Off, 'bingr2': Autonomy.Off, 'bingr3': Autonomy.Off, 'bingr4': Autonomy.Off, 'bingr5': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'part_type': 'part_type'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
