from config import get_config
import multiprocessing
import signal

from holon.HolonicAgent import HolonicAgent
import logit

from abdi_config import AbdiConfig

#
logger = logit.get_logger()


class Experiment(HolonicAgent):
    def __init__(self, cfg):
        super().__init__(cfg)

        # self.head_agents.append(DocumentImport(cfg))
        # self.head_agents.append(KnowledgeManagement(cfg))

        logger.debug(f"Init Experiment done.")

 
if __name__ == '__main__':
    logger.info(f'***** Experiment start *****')

    def signal_handler(signal, frame):
        logger.warning("System was interrupted.")
    signal.signal(signal.SIGINT, signal_handler)

    multiprocessing.set_start_method('spawn')

    Experiment(AbdiConfig(get_config())).start()
    