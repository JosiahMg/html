import os
import logging
from logging.handlers import TimedRotatingFileHandler
import re


HTML_PATH = os.path.dirname(__file__)

# log files fold
LOGS_PATH = os.path.join(HTML_PATH, 'log')


def setup_log(log_name):
    # 创建logger对象。传入logger名字
    logger = logging.getLogger(log_name)
    log_path = os.path.join(LOGS_PATH, log_name)

    # 设置日志记录等级
    logger.setLevel(logging.DEBUG)
    # interval 滚动周期，
    # when="MIDNIGHT", interval=1 表示每天0点为更新点，每天生成一个文件
    # backupCount  表示日志保存个数
    file_handler = TimedRotatingFileHandler(
        filename=log_path, when="MIDNIGHT", interval=1, backupCount=30, encoding='utf-8'
    )

    # filename="mylog" suffix设置，会生成文件名为mylog.2020-02-25.log
    file_handler.suffix = "%Y-%m-%d.log"
    # extMatch是编译好正则表达式，用于匹配日志文件名后缀
    # 需要注意的是suffix和extMatch一定要匹配的上，如果不匹配，过期日志不会被删除。
    file_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")
    # 定义日志输出格式
    file_handler.setFormatter(
        logging.Formatter(
            "[%(asctime)s] [%(process)d] [%(levelname)s] - %(module)s.%(funcName)s (%(filename)s:%(lineno)d) - %(message)s"
        )
    )
    logger.addHandler(file_handler)
    return logger


logger = setup_log("html")

if __name__ == "__main__":
    a = 100
    logger.info(f"this is info message {a}")
    logger.warning("this is a warning message")
    try:
        int("string")
    except ValueError as e:
        logger.error(e)
