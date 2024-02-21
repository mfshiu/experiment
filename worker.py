import json

from holon.HolonicAgent import HolonicAgent
import logit


logger = logit.get_logger()


class Worker(HolonicAgent):
    def __init__(self, cfg):
        super().__init__(cfg)

        logger.debug(f"Init Experiment done.")


    def on_connected(self):
        self.subscribe("job", topic_handler=self.do_job)


    def do_job(self, topic:str, payload):
        job = json.loads(payload.decode())
        logger.info(f"job: {job}")

        echo_interval = 1000
        load = int(job['load'])
        for i in range(1, load+1):
            if not i%echo_interval:
                print(f".{i//echo_interval}", end="")
        print(f"\nJob {job['id']} has been completed.")

        self.publish(topic="job_done", payload=job['id'])

