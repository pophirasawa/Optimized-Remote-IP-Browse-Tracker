import psutil
import time
import threading

class GetExtraInfoUtil:
    class UpdateNetSpeed(threading.Thread):
        upload_speed_MBps = 0
        download_speed_MBps = 0

        def __init__(self):
            threading.Thread.__init__(self)
            self.daemon = True
            self._init = True

        def run(self):
            while True:
                measure_start = psutil.net_io_counters()
                time.sleep(1)
                measure_end = psutil.net_io_counters()

                self.upload_speed_MBps = round(
                    (measure_end.bytes_sent - measure_start.bytes_sent) / 1048576, 2
                )
                self.download_speed_MBps = round(
                    (measure_end.bytes_recv - measure_start.bytes_recv) / 1048576, 2
                )

    def get_net_speed(net_speed_measure):
        return {
            "netSpeed": {
                "uploadSpeed": net_speed_measure.upload_speed_MBps,
                "downloadSpeed": net_speed_measure.download_speed_MBps,
            }
        }

    def get_cpu_usage():
        return {"cpuUsage": psutil.cpu_percent(1)}

net_speed_measure = GetExtraInfoUtil.UpdateNetSpeed()
net_speed_measure.start()