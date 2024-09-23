import platform
from sys import stdout
from loguru import logger

if platform.system()=="Linux":
    pass
else:
    from colorama import init
    init()

# Do you like the elegance of Chinese characters?
def PrintRed(*kw,**kargs):
    print("\033[0;31m",*kw,"\033[0m",**kargs)
def PrintGreen(*kw,**kargs):
    print("\033[0;32m",*kw,"\033[0m",**kargs)
def PrintYellow(*kw,**kargs):
    print("\033[0;33m",*kw,"\033[0m",**kargs)
def PrintBlue(*kw,**kargs):
    print("\033[0;34m",*kw,"\033[0m",**kargs)
def PrintPurple(*kw,**kargs):
    print("\033[0;35m",*kw,"\033[0m",**kargs)
def PrintIndigo(*kw,**kargs):
    print("\033[0;36m",*kw,"\033[0m",**kargs)

def PrintBrightRed(*kw,**kargs):
    print("\033[1;31m",*kw,"\033[0m",**kargs)
def PrintBrightGreen(*kw,**kargs):
    print("\033[1;32m",*kw,"\033[0m",**kargs)
def PrintBrightYellow(*kw,**kargs):
    print("\033[1;33m",*kw,"\033[0m",**kargs)
def PrintBrightBlue(*kw,**kargs):
    print("\033[1;34m",*kw,"\033[0m",**kargs)
def PrintBrightPurple(*kw,**kargs):
    print("\033[1;35m",*kw,"\033[0m",**kargs)
def PrintBrightIndigo(*kw,**kargs):
    print("\033[1;36m",*kw,"\033[0m",**kargs)

# Do you like the elegance of Chinese characters?
def sprint_red(*kw):
    return "\033[0;31m"+' '.join(kw)+"\033[0m"
def sprint_green(*kw):
    return "\033[0;32m"+' '.join(kw)+"\033[0m"
def sprint_yellow(*kw):
    return "\033[0;33m"+' '.join(kw)+"\033[0m"
def sprint_blue(*kw):
    return "\033[0;34m"+' '.join(kw)+"\033[0m"
def sprint_purple(*kw):
    return "\033[0;35m"+' '.join(kw)+"\033[0m"
def sprint_indigo(*kw):
    return "\033[0;36m"+' '.join(kw)+"\033[0m"
def sprint_bright_red(*kw):
    return "\033[1;31m"+' '.join(kw)+"\033[0m"
def sprint_bright_green(*kw):
    return "\033[1;32m"+' '.join(kw)+"\033[0m"
def sprint_bright_yellow(*kw):
    return "\033[1;33m"+' '.join(kw)+"\033[0m"
def sprint_bright_blue(*kw):
    return "\033[1;34m"+' '.join(kw)+"\033[0m"
def sprint_bright_purple(*kw):
    return "\033[1;35m"+' '.join(kw)+"\033[0m"
def SprintIndigo(*kw):
    return "\033[1;36m"+' '.join(kw)+"\033[0m"

def log红(*kw,**kargs):
    logger.opt(depth=1).info(sprint_red(*kw))
def log绿(*kw,**kargs):
    logger.opt(depth=1).info(sprint_green(*kw))
def log黄(*kw,**kargs):
    logger.opt(depth=1).info(sprint_yellow(*kw))
def log蓝(*kw,**kargs):
    logger.opt(depth=1).info(sprint_blue(*kw))
def log紫(*kw,**kargs):
    logger.opt(depth=1).info(sprint_purple(*kw))
def log靛(*kw,**kargs):
    logger.opt(depth=1).info(sprint_indigo(*kw))

def log_red(*kw,**kargs):
    logger.opt(depth=1).info(sprint_bright_red(*kw))
def log_green(*kw,**kargs):
    logger.opt(depth=1).info(sprint_bright_green(*kw))
def log_yellow(*kw,**kargs):
    logger.opt(depth=1).info(sprint_bright_yellow(*kw))
def log_blue(*kw,**kargs):
    logger.opt(depth=1).info(sprint_bright_blue(*kw))
def log_purple(*kw,**kargs):
    logger.opt(depth=1).info(sprint_bright_purple(*kw))
def log亮靛(*kw,**kargs):
    logger.opt(depth=1).info(SprintIndigo(*kw))