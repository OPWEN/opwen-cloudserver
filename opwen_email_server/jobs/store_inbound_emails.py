from opwen_email_server.api import email_receive
from opwen_email_server.backend import server_datastore
from opwen_email_server.services.queue_consumer import QueueConsumer
from opwen_email_server.utils.email_parser import format_inline_images
from opwen_email_server.utils.email_parser import format_attachments
from opwen_email_server.utils.email_parser import parse_mime_email


class Job(QueueConsumer):
    def __init__(self):
        super().__init__(email_receive.QUEUE.dequeue)

    def _process_message(self, message: dict):
        resource_id = message['resource_id']
        mime_email = email_receive.STORAGE.fetch_text(resource_id)
        self.log_info('Fetched inbound MIME email %s', resource_id)

        email = parse_mime_email(mime_email)
        email = format_attachments(email)
        email = format_inline_images(email)
        server_datastore.store_email(resource_id, email)
        self.log_info('Stored inbound email %s', resource_id)

        email_receive.STORAGE.delete(resource_id)
        self.log_info('Deleted inbound MIME email %s', resource_id)


if __name__ == '__main__':
    from opwen_email_server.services.queue_consumer import cli
    cli(Job)
