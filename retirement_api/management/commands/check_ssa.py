import datetime

from django.core.management.base import BaseCommand, CommandError
from retirement_api.utils import check_api

DAYSTAMP = datetime.date.today()
HELP_NOTE = """Sends a test post to SSA's Quick Calculator \
and checks the results to make sure we're getting valid results."""
END_NOTE = "Checked Quick Calculator"


class Command(BaseCommand):
    help = HELP_NOTE

    def handle(self, *args, **options):
        result = check_api.run(check_api.BASES['build'])
        self.stdout.write(check_api.build_msg(result))
