import json
import multiprocessing
import signal

from abdi_config import AbdiConfig
from config import get_config
from holon.HolonicAgent import HolonicAgent
import logit
from stopwatch import Stopwatch
from worker import Worker


logger = logit.get_logger()


class WorkingTest(HolonicAgent):
    def __init__(self, cfg):
        super().__init__(cfg)

        self.sw = Stopwatch()


    def on_connected(self):
        self.subscribe("work_start", topic_handler=self.start_working)
        self.subscribe("job_done", topic_handler=self.handle_job_done)

        Worker(self.config).start()


    def start_job(self, topic:str, payload):
        job = json.loads(payload.decode())

        job = json.dumps({
            "id": "1",
            "load": 30000
        })
        self.publish(topic="job", payload=job)
        logger.info(f"Start job at: {Stopwatch.format_time(self.sw.start())}")


    def handle_job_done(self, topic:str, payload):
        logger.info(f"Elapsed: {Stopwatch.format_elapsed_time(self.sw.stop()[0])}")



if __name__ == '__main__':
    logger.info(f'***** Experiment start *****')

    def signal_handler(signal, frame):
        logger.warning("System was interrupted.")
    signal.signal(signal.SIGINT, signal_handler)

    multiprocessing.set_start_method('spawn')

    cfg = AbdiConfig(get_config())

    WorkingTest(cfg).start(head=False)
