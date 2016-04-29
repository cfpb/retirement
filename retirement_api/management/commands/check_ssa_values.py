from django.core.management.base import BaseCommand, CommandError
from retirement_api.utils import ssa_check

LOGFILE = ''
HELP_NOTE = "Checks a ragne of results from SSA's Quick Calculator \
to detect whether benefit formulas have changed."
END_NOTE = "Checked SSA values; see results at {0}"


class Command(BaseCommand):
    help = HELP_NOTE

    def add_arguments(self, parser):
        parser.add_argument('--recalibrate',
                            action='store_true',
                            help='Create a new calibration file')

    def handle(self, *args, **options):
        if options['recalibrate']:
            endmsg = ssa_check.run_tests(recalibrate=True)
            self.stdout.write(endmsg)
        else:
            endmsg = ssa_check.run_tests()
            self.stdout.write(endmsg)
