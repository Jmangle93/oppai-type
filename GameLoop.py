import time
import threading

class TextBasedGame:
  def __init__(self, duration=30):
    self.duration = duration
    self.running = False
    self.success_count = 0
    self.time_remaining = duration

  def succeeded(self):
    return self.success_count >= 10

  def run_timer(self):
    start_time = time.time()
    while self.running and (time.time() - start_time < self.duration) and not self.succeeded():
      elapsed = int(time.time() - start_time)
      self.time_remaining = self.duration - elapsed
      time.sleep(1)
    self.running = False
    print("\nGame Over!")

  def prompt_user(self):
    while self.running and not self.succeeded():
      print(f"\rTime Remaining: {self.time_remaining}s | Success Count: {self.success_count}")
      prompt = "Type 'success' to score a point: "
      response = input(prompt)
      if response.strip().lower() == "success":
        self.success_count += 1

  def start_game(self):
    self.running = True
    timer_thread = threading.Thread(target=self.run_timer, daemon=True)
    prompt_thread = threading.Thread(target=self.prompt_user, daemon=True)

    timer_thread.start()
    prompt_thread.start()

    timer_thread.join()
    self.running = False  # Ensure prompt thread stops
    prompt_thread.join()

    print(f"Final Success Count: {self.success_count}")
