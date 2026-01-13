import logging

class EllipsisFormatter(logging.Formatter):
    def format(self, record):
        message = super().format(record)
        # 在日志的开头添加一个换行符
        return '\n' + str(message)

def get_logger(name="ISSUE"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 设置自定义日志格式
    formatter = EllipsisFormatter('%(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    # 添加处理器
    if not logger.hasHandlers():
        logger.addHandler(console_handler)

    return logger

