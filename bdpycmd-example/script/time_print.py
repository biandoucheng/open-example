import datetime
from bdpycmd.cmd.factory import base

class time_print:
    
    @base.BaseCommand.as_cmder
    def dt_print(self,f:str="%Y-%m-%d %H:%M:%S"):
        """
        print current time
        
        :param f: str datetime format str eg:%Y-%m-%d %H:%M:%S default:%Y-%m-%d %H:%M:%S
        :return:
        """
        dt = datetime.datetime.now().strftime(f)
        print(
            """
            %s
            """ % dt
        )