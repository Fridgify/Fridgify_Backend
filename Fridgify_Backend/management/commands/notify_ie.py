from django.core.management.base import BaseCommand

from Fridgify_Backend.utils.messaging import message_content, message_handler


class Command(BaseCommand):
    help = "Check the database and send notifications based on expiries"

    def add_arguments(self, parser):
        parser.add_argument('-d', '--duein', type=int, help="All items which are due in 0 to x days")
        parser.add_argument('-l', '--limit', type=int, help="Item limit for a notification")

    def handle(self, *args, **options):
        p_due = 3 if options["duein"] is None else options["duein"]
        p_limit = 3 if options["limit"] is None else options["limit"]

        content_group = message_content.get_grouped_content(p_due)
        self.stdout.write(f"{content_group}")

        for fridge_id, content in content_group:
            recipients = message_content.get_recipients(fridge_id)
            if not recipients:
                continue
            msg = message_content.create_expired_message(fridge_id, content, p_due, p_limit)
            self.stdout.write(f"{msg['body']}")

            message_handler.send_message(recipients, msg["title"], msg["body"], fridge_id)

        self.stdout.write(f"Command was called.")
