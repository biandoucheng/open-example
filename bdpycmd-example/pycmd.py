from bdpycmd.pycmd import *

CmdBaseConf.init(
    root_dir=".",
    cmd_dir='cmder'
)

if __name__ == "__main__":
    CmdBaseConf.run()