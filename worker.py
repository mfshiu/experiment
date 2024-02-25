import json
import threading

from holon.HolonicAgent import HolonicAgent
from holon.logistics.loading_coordinator import LoadingCoordinator
import logit


logger = logit.get_logger()
        

class Worker(HolonicAgent):
    def __init__(self, cfg, worker_id):
        super().__init__(cfg)
        
        self.number = worker_id
        self.current_progress = 0

        logger.debug(f"Init Experiment done.")


    def on_connected(self):
        self.loading_coordinator = LoadingCoordinator(
            agent=self,
            loading_evaluator=self.evaluate_loading)
        self.loading_coordinator.subscribe(topic="job", topic_handler=self.do_job)        
        self.subscribe("worker_termination", topic_handler=self.terminate_me)
        
        
    def evaluate_loading(self, topic, payload):
        return min(100, self.current_progress)


    def do_job(self, topic:str, payload):
        job = json.loads(payload.decode())
        logger.info(f"job: {job}")

        echo_interval = 1000000
        load = int(job['load'])
        job_id = job['id']
        for i in range(1, load+1):
            if not i % echo_interval:
                self.current_progress = i//echo_interval
                print(f"{self.number}-{job_id}.{self.current_progress}", end=" ")
        print(f"\n{self.number}-{job_id}.***")

        self.publish(topic="job_done", payload=job['id'])


    def terminate_me(self, topic:str, payload):
        logger.info(f"terminate: {self.number}")
        self.terminate()
