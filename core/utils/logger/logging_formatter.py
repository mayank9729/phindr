import logging

class SafeFormatter(logging.Formatter):
    def format(self, record):
        if not hasattr(record, 'ip'):
            record.ip = 'unknown'  
        return super().format(record)
