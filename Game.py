# import pykakasi
import random
import time
import threading
from hiragana_sets import vowels, k, s, t, n, h, m, y, r, w, g, z, d, b, p

class OppaiTypeGame:
  def __init__(self, duration=45):
    self.duration = duration
    self.loop_running = False
    self.looping = False
    self.success_count = 0
    self.best_score = 0
    self.time_remaining = duration
    self.setup_prompts()

  def check_play_again(self):
    if input("Do you want to play again? (y/n): ").strip().lower() != 'y':
      self.looping = False
      print("Thanks for playing!")
      self.looping = False
    else:
      self.setup_prompts()
      self.success_count = 0

  def check_score(self):
    if self.success_count > self.best_score:
      self.best_score = self.success_count
      print(f"New Best Score: {self.best_score}")
    else:
      print(f"Final Score: {self.success_count}")
      print(f"Best Score: {self.best_score}")
  
  def setup_prompts(self):
    self.prompts = vowels + k + s + t + n + h + m + y + r + w
    random.shuffle(self.prompts)

  def get_prompt(self):
    if self.prompts:
      return self.prompts.pop()
    else:
      self.setup_prompts()
      return self.prompts.pop()

  def run_timer(self):
    start_time = time.time()
    while self.loop_running and (time.time() - start_time < self.duration):
      elapsed = int(time.time() - start_time)
      self.time_remaining = self.duration - elapsed
      time.sleep(1)
    self.loop_running = False
    print("\nTime's up!")
    self.check_score()
    self.check_play_again()

  def run_prompts(self):
    while self.loop_running:
      print(f"\rTime Remaining: {self.time_remaining}s | Success Count: {self.success_count}")
      expected, prompt = self.get_prompt() 
      response = input(f'{prompt} = ')
      while response.strip().lower() != expected:
        print(f"Incorrect! Try again.")
        response = input(prompt)
      if response.strip().lower() == expected:
        self.success_count += 1
        print(f"Success! Current count: {self.success_count}")

  def run_game(self):
    self.looping = True
    while self.looping:
      self.loop_running = True
      timer_thread = threading.Thread(target=self.run_timer, daemon=True)
      prompt_thread = threading.Thread(target=self.run_prompts, daemon=True)

      timer_thread.start()
      prompt_thread.start()

      timer_thread.join()
      self.loop_running = False  # Ensure prompt thread stops
      prompt_thread.join()
