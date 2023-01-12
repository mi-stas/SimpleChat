import time


def time_to_message_format(seconds_time):
    local_seconds_time = time.localtime(seconds_time)
    return time.strftime("%H:%M", local_seconds_time)
