from bdpycmd.cmd.factory import base
from script import time_print

class Command(base.BaseCommand,time_print.time_print):
    def __init__(self):
        super().__init__(name=__class__.__module__,alias='Print',description='Print')
        super(base.BaseCommand,self).__init__()
        