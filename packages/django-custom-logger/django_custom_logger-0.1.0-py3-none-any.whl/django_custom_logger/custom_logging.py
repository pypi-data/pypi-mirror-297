import os
import threading
import time
import traceback
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime, timedelta
from logging import LogRecord, getLoggerClass, setLoggerClass, Filter

thread_local = threading.local()

class RequestIdFilter(Filter):
    def filter(self, record):
        record.request_id = getattr(thread_local, 'request_id', 'no_request_id')
        return True

class RequestIdLogger(getLoggerClass()):
    def makeRecord(self, name, level, fn, lno, msg, args, exc_info,
                   func=None, extra=None, sinfo=None):
        rv = super().makeRecord(name, level, fn, lno, msg, args, exc_info, func, extra, sinfo)
        rv.request_id = getattr(thread_local, 'request_id', 'no_request_id')
        rv.exec_info = getattr(thread_local, 'exec_info', None)
        return rv

    def exception(self, msg, *args, **kwargs):
        thread_local.exec_info = traceback.format_exc()
        super().exception(msg, *args, **kwargs)
        thread_local.exec_info = None

setLoggerClass(RequestIdLogger)

class SizeTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, filename, max_bytes, keep_days, encoding=None):
        super().__init__(filename, when='midnight', interval=1, encoding=encoding)
        self.maxBytes = max_bytes
        self.suffix = "%Y-%m-%d"
        self.keep_days = keep_days

    def shouldRollover(self, record):
        if self.stream is None:
            self.stream = self._open()
        if self.maxBytes > 0:
            msg = "%s\n" % self.format(record)
            self.stream.seek(0, 2)
            if self.stream.tell() + len(msg) >= self.maxBytes:
                return 1
        t = int(time.time())
        if t >= self.rolloverAt:
            return 1
        return 0

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        currentTime = int(time.time())
        dstNow = time.localtime(currentTime)[-1]
        t = self.rolloverAt - self.interval
        if self.utc:
            timeTuple = time.gmtime(t)
        else:
            timeTuple = time.localtime(t)
            dstThen = timeTuple[-1]
            if dstNow != dstThen:
                if dstNow:
                    addend = 3600
                else:
                    addend = -3600
                timeTuple = time.localtime(t + addend)
        dfn = self.rotation_filename(self.baseFilename + "." +
                                    time.strftime(self.suffix, timeTuple))

        if os.path.exists(dfn):
            count = 1
            dfn_base = dfn
            while os.path.exists(dfn):
                dfn = f"{dfn_base}.{count}"
                count += 1

        if os.path.exists(self.baseFilename):
            try:
                os.rename(self.baseFilename, dfn)
            except OSError:
                os.remove(self.baseFilename)

        if not self.delay:
            self.stream = self._open()
        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            if dstNow != dstAtRollover:
                if not dstNow:
                    addend = -3600
                else:
                    addend = 3600
                newRolloverAt += addend
        self.rolloverAt = newRolloverAt

        self.deleteOldLogs()

    def deleteOldLogs(self):
        dirName, baseName = os.path.split(self.baseFilename)
        fileNames = os.listdir(dirName)
        prefix = baseName + "."
        plen = len(prefix)
        current_time = datetime.now()
        for fileName in fileNames:
            if fileName.startswith(prefix):
                filePath = os.path.join(dirName, fileName)
                fileTime = datetime.fromtimestamp(os.path.getmtime(filePath))
                if (current_time - fileTime) > timedelta(days=self.keep_days):
                    try:
                        os.remove(filePath)
                        print(f"Deleted old log file: {filePath}")
                    except Exception as e:
                        print(f"Error deleting {filePath}: {e}")

def create_timed_rotating_log_handler(filename, max_bytes=5 * 1024 * 1024, keep_days=10, encoding='utf-8'):
    log_dir = os.path.dirname(filename)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    handler = SizeTimedRotatingFileHandler(filename, max_bytes=max_bytes, keep_days=keep_days, encoding=encoding)
    handler.deleteOldLogs()
    return handler

def set_request_id(request_id):
    thread_local.request_id = request_id

def clear_request_id():
    if hasattr(thread_local, 'request_id'):
        del thread_local.request_id

def get_request_id():
    return getattr(thread_local, 'request_id', 'no_request_id')