import time

class Stopwatch:
    def __init__(self):
        self.start_time = None
        self.laps = []
        self.running = False


    def start(self):
        if not self.running:
            self.start_time = time.time()
            self.laps = []
            self.running = True

        return self.start_time


    def stop(self):
        if self.running:
            elapsed_time = time.time() - self.start_time
            self.laps.append(elapsed_time)
            self.running = False

        return self.laps


    def lap(self):
        if self.running:
            current_time = time.time() - self.start_time
            self.laps.append(current_time)

        return self.laps


    def reset(self):
        self.start_time = None
        self.laps = []
        self.running = False


    def format_time(timestamp):
        # Format the timestamp as hh:mm:ss.fff
        time_struct = time.localtime(timestamp)
        return time.strftime("%H:%M:%S", time_struct) + f".{int(timestamp * 1000) % 1000:03d}"


    def format_elapsed_time(elapsed):
        # Convert elapsed time to hh:mm:ss.fff
        hours, rem = divmod(elapsed, 3600)
        minutes, seconds = divmod(rem, 60)
        milliseconds = (seconds - int(seconds)) * 1000
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}.{int(milliseconds):03d}"


if __name__ == '__main__':
    # Example usage
    stopwatch = Stopwatch()
    print(f"start: {Stopwatch.format_time(stopwatch.start())}")
    time.sleep(2)  # Simulate the stopwatch running for 2 seconds
    # print(f"lap: {stopwatch.lap()}")
    # time.sleep(1)  # Simulate running for another 1 second
    stopwatch.stop()
    print(f"stop: {Stopwatch.format_elapsed_time(stopwatch.stop()[0])}")
    stopwatch.reset()
