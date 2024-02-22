import multiprocessing
from multiprocessing import Process

class ExampleClass:
    def __init__(self, value):
        print("init")
        self.value = value
        self.value1 = "value1"

    def run_in_process(self):
        self.value += 1
        print(f"Value in process: {self.value}")
        print(f"Value1 in process: {self.value1}")

def create_and_start_process(example_instance):
    process = Process(target=example_instance.run_in_process)
    process.start()
    # process.join()

if __name__ == '__main__':
    multiprocessing.set_start_method('spawn')
    example = ExampleClass(value=10)
    create_and_start_process(example)
    print(f"Value in example: {example.value}")
    print(f"Value1 in example: {example.value1}")
    