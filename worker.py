import json
import time

from holon.HolonicAgent import HolonicAgent
from holon.logistics.loading_coordinator import LoadingCoordinator
import logit


logger = logit.get_logger()
        

class Worker(HolonicAgent):
    def __init__(self, cfg, worker_id):
        super().__init__(cfg)
        
        self.number = worker_id
        self.current_progress = 0
        self.total_load = 0

        logger.debug(f"{self.short_id}> Init Experiment done.")


    def on_connected(self):
        self.loading_coordinator = LoadingCoordinator(
            agent=self,
            loading_evaluator=self.evaluate_loading)
        self.loading_coordinator.subscribe(topic="job", topic_handler=self.do_job)        
        self.subscribe("worker_termination", topic_handler=self.terminate_me)
        
        
    def evaluate_loading(self, topic, payload):
        if self.total_load:
            return 100 - int(self.current_progress / self.total_load * 100)
        else:
            return 0


    def do_job(self, topic:str, payload):
        job = json.loads(payload.decode())
        logger.debug(f"{self.short_id}> job: {job}")

        # echo_interval = 1000000
        self.current_progress = 0
        self.total_load = int(job['load'])
        job_id = job['id']
        for i in range(0, self.total_load):
            self.current_progress = i
            # print(f"{i} ")
            # time.sleep(0.01)
            # if not i % echo_interval:
                # print(f"{self.number}-{job_id}.{self.current_progress}", end=" ")
                
        self.current_progress = 0
        self.total_load = 0
        logger.warning(f"{self.short_id}> Completed job, Worker: {self.number}, Job: {job_id}")

        self.publish(topic="job_done", payload=job['id'])


    def terminate_me(self, topic:str, payload):
        logger.info(f"{self.short_id}> terminate: {self.number}")
        self.terminate()
