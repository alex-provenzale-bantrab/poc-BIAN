""" CustomerBehavior Service Domain - Customer Insights Publisher """
#
#  Author: Alessandro Petroni <apetroni@gmail.com>

import json
from solace.messaging.resources.topic import Topic
from solace.messaging.publisher.direct_message_publisher import PublishFailureListener, FailedPublishEvent
from solace.messaging.publisher.persistent_message_publisher import PersistentMessagePublisher, MessagePublishReceiptListener


class PublisherErrorHandling(PublishFailureListener):
    def on_failed_publish(self, e: "FailedPublishEvent"): 
        print("on_failed_publish")


class MessagePublishReceiptListenerImpl(MessagePublishReceiptListener):
    def on_publish_receipt(self, publish_receipt= 'PublishReceipt'):
        pass
        #print("on publish, sends the publish receipt")


class MessagePublisher():
    def __init__(self, messaging_service):
        self.publisher: PersistentMessagePublisher = messaging_service.create_persistent_message_publisher_builder().build()
        self.publisher.start()
        self.outboud_msg_builder = messaging_service.message_builder()
        
    def publish_string_message_non_blocking(self, destination: Topic, message):
      publish_receipt_listener = MessagePublishReceiptListenerImpl()
      self.publisher.set_message_publish_receipt_listener(publish_receipt_listener)
      
      message_body = json.dumps(message)
      outboud_msg = self.outboud_msg_builder.build(f'{message_body}')
      
      self.publisher.publish( message=outboud_msg, destination=destination)
      print(f'Published message with {destination}')
