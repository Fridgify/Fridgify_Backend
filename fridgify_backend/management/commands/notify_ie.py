import logging
from logging import handlers

from django.core.management.base import BaseCommand

from fridgify_backend.utils.messaging import message_content, message_handler


class Command(BaseCommand):
    help = "Check the database and send notifications based on expiries"

    def add_arguments(self, parser):
        parser.add_argument('-d', '--duein', type=int, help="All items which are due in 0 to x days")
        parser.add_argument('-l', '--limit', type=int, help="Item limit for a notification")

    def handle(self, *args, **options):
        p_due = 3 if options["duein"] is None else options["duein"]
        p_limit = 3 if options["limit"] is None else options["limit"]

        handler = logging.handlers.RotatingFileHandler(
            "./logs/fridgify_notifications.log",
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
            mode='a'
        )
        logging.basicConfig(
            format='%(asctime)s %(name)s:%(levelname)s - %(message)s',
            level=logging.DEBUG,
            handlers=[handler]
        )

        content_group = message_content.get_grouped_content(p_due)
        self.stdout.write(f"{content_group}")

        for fridge_id, content in content_group:
            self.stdout.write(f"Send notification to members of {fridge_id}")
            recipients = message_content.get_recipients(fridge_id)
            if not recipients:
                continue
            msg = message_content.create_expired_message(fridge_id, content, p_due, p_limit)
            message_handler.send(recipients, msg["title"], msg["body"], fridge_id=fridge_id)
            self.stdout.write(f"Send notification to service providers...")

        self.stdout.write(f"Send messages successfully.")
