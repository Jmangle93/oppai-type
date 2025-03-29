import pykakasi
import time
import threading
import random

class OppaiTypeGame:
  def __init__(self, duration=40):
    self.duration = duration
    self.running = False
    self.success_count = 0
    self.time_remaining = duration
    self.kakasi = pykakasi.kakasi()
    self.setup_prompts()

  def succeeded(self):
    return self.success_count >= 10
  
  def setup_prompts(self):
    self.prompts = [
      ("あ", "a"),
      ("い", "i"),
      ("う", "u"),
      ("え", "e"),
      ("お", "o"),
      ("か", "ka"),
      ("き", "ki"),
      ("く", "ku"),
      ("け", "ke"),
      ("こ", "ko"),
      ("さ", "sa"),
      ("し", "shi"),
      ("す", "su"),
      ("せ", "se"),
      ("そ", "so"),
      ("た", "ta"),
      ("ち", "chi"),
      ("つ", "tsu"),
      ("て", "te"),
      ("と", "to"),
      ("な", "na"),
      ("に", "ni"),
      ("ぬ", "nu"),
      ("ね", "ne"),
      ("の", "no"),
      ("は", "ha"),
      ("ひ", "hi"),
      ("ふ", "fu"),
      ("へ", "he"),
      ("ほ", "ho"),
    ]
    random.shuffle(self.prompts)

  def get_prompt(self):
    return self.prompts.pop() if self.prompts else (None, None)

  def run_timer(self):
    start_time = time.time()
    while self.running and (time.time() - start_time < self.duration) and not self.succeeded():
      elapsed = int(time.time() - start_time)
      self.time_remaining = self.duration - elapsed
      time.sleep(1)
    self.running = False
    print("\nGame Over!")

  def run_prompts(self):
    while self.running and not self.succeeded():
      print(f"\rTime Remaining: {self.time_remaining}s | Success Count: {self.success_count}")
      prompt, expected = self.get_prompt() 
      response = input(f'{prompt} = ')
      while response.strip().lower() != expected:
        print(f"Incorrect! Try again.")
        response = input(prompt)
      if response.strip().lower() == expected:
        self.success_count += 1
        print(f"Success! Current count: {self.success_count}")

  def run_game(self):
    self.running = True
    timer_thread = threading.Thread(target=self.run_timer, daemon=True)
    prompt_thread = threading.Thread(target=self.run_prompts, daemon=True)

    timer_thread.start()
    prompt_thread.start()

    timer_thread.join()
    self.running = False  # Ensure prompt thread stops
    prompt_thread.join()

    print(f"Final Success Count: {self.success_count}")
