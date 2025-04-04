from collections import defaultdict
from dataclasses import dataclass, field
import random
from typing import Dict, List, Tuple
import pygame
import pygame_menu
from pygame.locals import QUIT,KEYDOWN,K_ESCAPE,K_RETURN,K_BACKSPACE,K_SPACE,TEXTINPUT,USEREVENT
import hiragana_sets
import katakana_sets


TIME_EVENT = USEREVENT + 1
FINE_TIME_EVENT = USEREVENT + 2

"""
CharacterStats is a helper dataclass designed to track typing performance metrics for individual characters.
It provides properties to calculate accuracy, average speed, and consistency based on the typing data.

Attributes:
    attempts (int): The total number of attempts made to type this character.
    correct (int): The number of correct attempts for this character.
    total_time (float): The total time (in seconds) spent typing this character.

Properties:
    accuracy (float): The percentage of correct attempts out of total attempts. Returns 0.0 if no attempts are made.
    average_speed (float): The average time (in seconds) spent per correct attempt. Returns 0.0 if no correct attempts are made.
    consistency (float): The ratio of correct attempts to total attempts. Returns 0.0 if no attempts are made.
"""
@dataclass
class CharacterStats:
    attempts: int = 0
    correct: int = 0
    total_time: float = 0.0  # Total time spent typing this character
    individual_times: List[float] = field(default_factory=list)

    @property
    def accuracy(self) -> float:
        return (self.correct / self.attempts) * 100 if self.attempts > 0 else 0.0

    @property
    def average_speed(self) -> float:
        return self.total_time / self.correct if self.correct > 0 else 0.0

    @property
    def consistency(self) -> float:
        if len(self.individual_times) < 2:
            return 1.0  # Perfect consistency if few attempts
        mean = sum(self.individual_times) / len(self.individual_times)
        variance = sum((x - mean) ** 2 for x in self.individual_times) / len(self.individual_times)
        return 1 / (variance + 1)  # Inverse of variance (higher is more consistent)
    
    def update(self, time_taken: float, was_correct: bool) -> None:
        """
        Update the character's stats based on a new attempt.

        Args:
            time_taken (float): The time taken for this attempt.
            was_correct (bool): Whether the attempt was correct or not.
        """
        self.attempts += 1
        if was_correct:
            self.correct += 1
            self.total_time += time_taken
        self.individual_times.append(time_taken)

class CharacterTracker:
    def __init__(self):
        self.stats: Dict[str, CharacterStats] = defaultdict(CharacterStats)

    def update_stats(self, japanese: str, time_taken: float, was_correct: bool):
        self.stats[japanese].update(time_taken, was_correct)

    def get_stats(self, character: str) -> CharacterStats:
        return self.stats[character]

class OppaiType:
    def __init__(self):
        pygame.init()
        self.size = self.weight, self.height = 800, 600
        self.scroll_offset = 0
        self.scroll_speed = 10
        self.panel_width = 400
        self.panel_height = 400
        self.panel_x = self.weight - self.panel_width
        self.panel_y = 0
        self._character_tracker = CharacterTracker()
        self._hiragana_sets = hiragana_sets.default.characters
        self._katakana_sets = katakana_sets.vowels + katakana_sets.k
        self._prompt_queue = self._hiragana_sets.copy()
        self._score = 0
        self._high_score = 0
        self._attempt_timer = 0.0
        self._timer = 0.0
        self._time_limit = 30
        self._time_remaining = self._time_limit
        self._user_input = ""
        self._round_running = False
        self._running = False
        self._winning = False
        self.missed_characters = []
        self.fine_time_event = pygame.event.Event(FINE_TIME_EVENT)
        self.time_event = pygame.event.Event(TIME_EVENT)
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.menu_theme = pygame_menu.themes.THEME_DARK
        self.font = pygame.font.Font('fonts/ZenKakuGothicAntique-Regular.ttf', 30)
        self.menu_theme.widget_font = self.font
        self._main_menu = pygame_menu.Menu(
            'Main Menu',
            self.weight,
            self.height,
            theme=self.menu_theme,
        )
        self._options_menu = pygame_menu.Menu(
            'Options',
            self.weight,
            self.height,
            theme=self.menu_theme,
        )
        self.sugoi_oppai = pygame.image.load('images/sugoi_oppai.png').convert()
        self.sugoi_oppai = pygame.transform.scale(self.sugoi_oppai, (self.weight // 2, self.height // 2))
        self.setup_menus()

    def setup_prompt_queue(self):
        self._prompt_queue = self._katakana_sets.copy()
        self._prompt_queue.extend(self._hiragana_sets.copy())
        random.shuffle(self._prompt_queue)

    def setup_menus(self):
        # Main
        self._main_menu.add.button('Play', self.start_game)
        self._main_menu.add.button('Options', self._options_menu)
        self._main_menu.add.button('Quit', pygame_menu.events.EXIT)
        # Options
        self._options_menu.add.dropselect_multiple(
            'Hiragana Sets',
            [
                ('あ ...', hiragana_sets.vowels.characters),
                ('か ...', hiragana_sets.k.characters),
                ('が ...', hiragana_sets.g.characters),
                ('さ ...', hiragana_sets.s.characters),
                ('ざ ...', hiragana_sets.z.characters),
                ('た ...', hiragana_sets.t.characters),
                ('だ ...', hiragana_sets.d.characters),
                ('な ...', hiragana_sets.n.characters),
                ('は ...', hiragana_sets.h.characters),
                ('ば ...', hiragana_sets.b.characters),
                ('ぱ ...', hiragana_sets.p.characters),
                ('ま ...', hiragana_sets.m.characters),
                ('や ...', hiragana_sets.y.characters),
                ('ら ...', hiragana_sets.r.characters),
                ('わ ...', hiragana_sets.w.characters),
            ],
            default=[0, 1, 3, 5],
            onreturn=lambda value: setattr(
                self,
                '_hiragana_sets',
                [item for _, h_set in value[0] for item in h_set],
            ),
        )
        self._options_menu.add.dropselect_multiple(
            'Katakana Sets',
            [
                ('ア ...', katakana_sets.vowels),
                ('カ ...', katakana_sets.k),
                ('ガ ...', katakana_sets.g),
                ('サ ...', katakana_sets.s),
                ('ザ ...', katakana_sets.z),
                ('タ ...', katakana_sets.t),
                ('ダ ...', katakana_sets.d),
                ('ナ ...', katakana_sets.n),
                ('ハ ...', katakana_sets.h),
                ('バ ...', katakana_sets.b),
                ('パ ...', katakana_sets.p),
                ('マ ...', katakana_sets.m),
                ('ヤ ...', katakana_sets.y),
                ('ラ ...', katakana_sets.r),
                ('ワ ...', katakana_sets.w),
            ],
            default=[0, 1],
            onreturn=lambda value: setattr(
                self,
                '_katakana_sets',
                [item for _, h_set in value[0] for item in h_set],
            ),
        )
        self._options_menu.add.range_slider(
            'Time Limit',
            default=30,
            range_values=(10, 120),
            increment=1,
            onchange=lambda value: setattr(self, '_time_limit', value),
            )
        self._options_menu.add.button('Back', pygame_menu.events.BACK)

    def main_menu(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == QUIT:
                    pygame.quit()
                    return
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        return
            if self._main_menu.is_enabled():
                self._main_menu.mainloop(self._display_surf)
            pygame.display.flip()

    def handle_keydown(self, event):
        if event.key == K_ESCAPE:
            self._running = False
        if self._round_running:
            if event.key == K_RETURN:
                self.check_user_input()
            elif event.key == K_BACKSPACE:
                self._user_input = self._user_input[:-1]
        elif event.key == K_SPACE:
            self.start_round()

    def check_user_input(self):
        if self._user_input.lower().strip() == self._prompt_queue[0][0]:
            self._score += 1
            self._winning = True
            self._character_tracker.update_stats(
                self._prompt_queue[0][1],
                self._attempt_timer,
                True,
            )
            self._prompt_queue.pop(0)
            if not self._prompt_queue:
                self.setup_prompt_queue()
        else:
            print("Incorrect input!")
            self._winning = False
            self._character_tracker.update_stats(
                self._prompt_queue[0][1],
                self._attempt_timer,
                False,
            )
        self._user_input = ""
        self._attempt_timer = 0.0

    def check_score(self):
        if self._score > self._high_score:
            self._high_score = self._score
            print(f"New High Score: {self._high_score}")
        else:
            print(f"Final Score: {self._score}")
            print(f"High Score: {self._high_score}")
        self._round_running = False
        self._score = 0

    def start_game(self):
        self._main_menu.disable()
        self._main_menu.full_reset()
        print("Game started!")
        self._running = True
        self.main_loop()

    def start_round(self):
        self._round_running = True
        self._timer = 0.0
        self._attempt_timer = 0.0
        self._user_input = ""
        self._score = 0
        self._time_remaining = self._time_limit
        self.setup_prompt_queue()
        pygame.time.set_timer(self.time_event, 1000)
        pygame.time.set_timer(self.fine_time_event, 50)

    def display_scrollable_stats(self):
        pygame.draw.rect(
            self._display_surf,
            (100, 200, 200),
            (self.panel_x, self.panel_y, self.panel_width, self.panel_height),
        )
        for i, (character, stats) in enumerate(self._character_tracker.stats.items()):
            text = f"{character}: {stats.accuracy:.2f}% | {stats.average_speed:.2f}s | {stats.consistency:.2f}"
            text_surface = self.font.render(text, True, (0, 0, 0))
            text_y = self.panel_y + (i * self.font.get_height() + 10) - self.scroll_offset

            if self.panel_y <= text_y < self.panel_y + self.panel_height + self.font.get_height():
                self._display_surf.blit(text_surface, (self.panel_x + 10, text_y))

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
        elif event.type == TEXTINPUT:
            if event.text:
                self._user_input += event.text
        elif event.type == KEYDOWN:
            self.handle_keydown(event)
        elif event.type == TIME_EVENT:
            self._timer += 1.0
        elif event.type == FINE_TIME_EVENT:
            self._attempt_timer += 0.05
        elif event.type == pygame.MOUSEWHEEL:
            self.scroll_offset -= event.y * self.scroll_speed
            self.scroll_offset = max(0, min(self.scroll_offset, len(self._character_tracker.stats) * self.font.get_height() + 10 - self.panel_height))

    def on_update(self):
        self._time_remaining = self._time_limit - self._timer
        if self._round_running and self._time_remaining <= 0:
            self._round_running = False
            print("Time's up!")
            self.check_score()

    def on_render(self):
        self._display_surf.fill((0, 0, 0))
        self._display_surf.blit(
            self.font.render(f'High Score: {self._high_score}', True, (100, 200, 200)),
            (50, 10)
        )
        if self._round_running:
            self._display_surf.blit(
                self.font.render(
                    f'Time Remaining: {self._time_remaining} s',
                    True,
                    (100, 200, 200),
                ),
                (50, 50),
            )
            _, prompt = self._prompt_queue[0]
            self._display_surf.blit(
                self.font.render(f'{prompt}', True, (100, 200, 200)),
                dest=(50, 100),
            )
            self._display_surf.blit(
                self.font.render(f'Input: {self._user_input}', True, (100, 200, 200)),
                dest=(50, 150),
            )
            self._display_surf.blit(
                self.font.render(f'Score: {self._score}', True, (100, 200, 200)),
                dest=(50, 200),
            )
            if self._winning:
                self._display_surf.blit(
                    self.sugoi_oppai,
                    (self.weight - self.sugoi_oppai.get_width() * 1.1, self.height - self.sugoi_oppai.get_height() * 1.1),
                )
        else:
            self._display_surf.blit(
                self.font.render('Press space to start', True, (100, 200, 200)),
                (50, 50),
            )
            self.display_scrollable_stats()
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def main_loop(self):
        """
        The main game loop that runs continuously while the game is active.

        This method handles the following tasks:
        - Processes all incoming events by calling `on_event` for each event.
        - Updates the game state by calling `on_update`.
        - Renders the game visuals by calling `on_render`.
        - Cleans up resources by calling `on_cleanup` when the loop ends.

        The loop continues running as long as the `_running` attribute is set to True.
        """
        while self._running:
            events = pygame.event.get()
            for event in events:
                self.on_event(event)

            self.on_update()
            self.on_render()

        self.on_cleanup()

if __name__ == "__main__" :
    game = OppaiType()
    game.main_menu()
