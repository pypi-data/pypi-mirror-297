#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from logging import Formatter, LogRecord

class JsonFormatter(Formatter):
    def format(self, record: LogRecord) -> str:
        log_record = {
            'level': record.levelname,
            'module': record.module,
            'funcName': record.funcName,
            'filename': record.filename,
            'lineno': record.lineno,
            'message': record.getMessage(),
            'time': self.formatTime(record, self.datefmt)
        }

        if record.exc_info:
            log_record['exception'] = self.formatException(record.exc_info)

        return json.dumps(log_record)
