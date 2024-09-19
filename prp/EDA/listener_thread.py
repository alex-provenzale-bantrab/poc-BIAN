import threading
import time
import json
import argparse
from solace.messaging.resources.topic_subscription import TopicSubscription
from solace.messaging.receiver.persistent_message_receiver import PersistentMessageReceiver
from solace.messaging.resources.queue import Queue
from solace.messaging.errors.pubsubplus_client_error import PubSubPlusClientError
from solace.messaging.config.missing_resources_creation_configuration import MissingResourcesCreationStrategy
from solace.messaging.receiver.message_receiver import (InboundMessage, MessageHandler)
from .messaging_util import connect_to_broker
from .publisher import MessagePublisher
from solace.messaging.resources.topic import Topic

from prp.services import PartyStateService, AlertService, RatingService, StatusService

from flask import current_app

party_state_service = PartyStateService()
alert_service = AlertService()
rating_service = RatingService()
status_service = StatusService()


def handle_initiate_CR_operation (payload):
    print("Handling Initiate operation CR Level")
    return party_state_service.initiate_profile_state_monitoring(payload)
    
def handle_update_CR_operation (CR_id: str, payload):
    print("Handling Update operation CR Level")
    return party_state_service.update_party_state(payload, CR_id)
    
def handle_execute_CR_operation (CR_id: str, payload):
    print("Handling Execute operation CR Level")
    
def handle_request_CR_operation (CR_id: str, payload):
    print("Handling Request operation CR Level")

def handle_retrieve_CR_operation (CR_id: str):
    print("Handling Retrieve operation CR Level")
    return party_state_service.retrieve_party_state(CR_id)

def handle_update_BQ_operation (CR_id: str, BQ, BQ_id: str, payload):
    print("Handling Update operation BQ level")
    if BQ == 'Alert':
        return alert_service.update_alert(payload, CR_id, BQ_id)
    elif BQ == 'Rating':
        return rating_service.update_rating(payload, CR_id, BQ_id)
    elif BQ == 'Status':
        return status_service.update_status(payload, CR_id, BQ_id)

def handle_capture_BQ_operation (CR_id: str, BQ, BQ_id: str, payload):
    print("Handling Capture operation BQ level")    
    # if BQ == 'Alert':
    #     return alert_service.
    # elif BQ == 'Rating':
    #     return rating_service.
    # elif BQ == 'Status':
    #     return status_service.

def handle_retrieve_BQ_operation (CR_id: str, BQ, BQ_id: str):
    print("Handling Retrieve operation BQ level")
    if BQ == 'Alert':
        return alert_service.retrieve_alert(CR_id, BQ_id)
    elif BQ == 'Rating':
        return rating_service.retrieve_rating(CR_id, BQ_id)
    elif BQ == 'Status':
        return status_service.retrieve_status(CR_id, BQ_id)


# Callback for received messages
class MessageHandlerImpl(MessageHandler):
    def __init__(self, persistent_receiver: PersistentMessageReceiver, app=None):
        self.receiver: PersistentMessageReceiver = persistent_receiver
        self.message_publisher = None
        self.app = app
        
    def set_message_publisher(self, message_publisher):
        self.message_publisher = message_publisher

    """ Handles messages received from the broker. """
    def on_message(self, message: InboundMessage):
        with self.app.app_context():
            topic = message.get_destination_name()
            assert topic.startswith('BIAN/12.0.0/PartyRoutingProfile')
            payload = message.get_payload_as_string() if message.get_payload_as_string() != None else message.get_payload_as_bytes()
            if isinstance(payload, bytearray):
                print(f"Received a message of type: {type(payload)}. Decoding to string")
                payload = payload.decode()
            print("\n" + f"Message received. Topic: {topic}")
            print(f"Message Payload: {payload}")

            # Parse the JSON data
            json_data = json.loads(payload)

            # BIAN/12.0.0/PartyRoutingProfile/PRPId/Status/StatusId/Action
            
            try:
                parts = topic.split("/")
                
                action_term = parts[-1]
                sd_version = parts[1]
                control_record = parts[2]
                control_record_id = parts[3] if parts[3] != action_term else None
                
                behaviour_qualifier = None 
                behaviour_qualifier_id = None
                
                if len(parts) > 4 and parts[4] != action_term:
                    behaviour_qualifier = parts[4]
                    behaviour_qualifier_id = parts[5] if parts[5] != action_term else None
                
                if behaviour_qualifier:
                    if action_term == "Update":
                        behaviour_qualifier_res, status_code = handle_update_BQ_operation(control_record_id, behaviour_qualifier, behaviour_qualifier_id, json_data[behaviour_qualifier])
                    elif action_term == "Capture":
                        behaviour_qualifier_res, status_code = handle_capture_BQ_operation(control_record_id, behaviour_qualifier, behaviour_qualifier_id, json_data[behaviour_qualifier])
                    elif action_term == "Retrieve":
                        behaviour_qualifier_res, status_code = handle_retrieve_BQ_operation(control_record_id, behaviour_qualifier, behaviour_qualifier_id)
                    else:
                        # Handle unknown or unsupported BQ operation
                        print(f"Unsupported BQ operation: {action_term}")
                    if behaviour_qualifier_res and status_code and status_code in [200, 201]:
                        self.message_publisher.publish_string_message_non_blocking(Topic.of(topic + '/Response'), {
                                'status_code': status_code,
                                'data': behaviour_qualifier_res
                            })
                    else:
                        self.message_publisher.publish_string_message_non_blocking(Topic.of(topic + '/Response'), behaviour_qualifier_res)
                else:
                    if action_term == "Initiate":
                        control_record_res, status_code = handle_initiate_CR_operation(json_data)
                    elif action_term == "Update":
                        control_record_res, status_code = handle_update_CR_operation(control_record_id, json_data)
                    elif action_term == "Execute":
                        handle_execute_CR_operation(control_record_id, json_data)
                    elif action_term == "Request":
                        handle_request_CR_operation(control_record_id, json_data)
                    elif action_term == "Retrieve":
                        control_record_res, status_code = handle_retrieve_CR_operation(control_record_id)
                    else:
                        # Handle unknown or unsupported CR operation
                        print(f"Unsupported CR operation: {action_term}")
                    if control_record_res and status_code and status_code in [200, 201]:
                        self.message_publisher.publish_string_message_non_blocking(Topic.of(topic + '/Response'), {
                                'status_code': status_code,
                                'data': control_record_res
                            })
                    else:
                        self.message_publisher.publish_string_message_non_blocking(Topic.of(topic + '/Response'), control_record_res)
            except Exception as ex:
                print ("Exception while processing incoming message" , ex)
            finally:
                self.receiver.ack(message)


def start_listener(queue_name="bian-coreless4-poc", app=None):
    # Attempts to connect to BIAN cloud broker
    messaging_service = connect_to_broker()
    
    topics = ["BIAN/12.0.0/PartyRoutingProfile/>"]
    topics_sub = [TopicSubscription.of(t) for t in topics]

    durable_exclusive_queue = Queue.durable_exclusive_queue(queue_name)

    # Build a receiver and bind it to the durable exclusive queue
    persistent_receiver: PersistentMessageReceiver = messaging_service.create_persistent_message_receiver_builder() \
        .with_subscriptions(topics_sub) \
        .with_missing_resources_creation_strategy(MissingResourcesCreationStrategy.CREATE_ON_START) \
        .build(durable_exclusive_queue)
    persistent_receiver.start()
    
    msg_publisher = MessagePublisher(messaging_service=messaging_service)

    try:
        # Callback for received messages
        msg_handler = MessageHandlerImpl(persistent_receiver, app=app)
        msg_handler.set_message_publisher(msg_publisher)
        persistent_receiver.receive_async(msg_handler)
        print(f'Persistent receiver started, bound to Queue [{durable_exclusive_queue.get_name()}]')
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print('\nDisconnecting Messaging Service')
    except PubSubPlusClientError as exception:
        print(f'\nMake sure queue { queue_name } exists on broker!')
    finally:
        if persistent_receiver and persistent_receiver.is_running():
            print('\nTerminating receiver')
            persistent_receiver.terminate()
        print('\nDisconnecting Messaging Service')
        messaging_service.disconnect()
