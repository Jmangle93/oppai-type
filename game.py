import random
import pygame
import pygame_menu
from pygame.locals import QUIT,KEYDOWN,K_ESCAPE,K_RETURN,K_BACKSPACE,K_SPACE,TEXTINPUT,USEREVENT
import hiragana_sets
import katakana_sets

TIME_EVENT = USEREVENT + 1

class OppaiType:
    def __init__(self):
        pygame.init()
        self.size = self.weight, self.height = 800, 600
        self._hiragana_sets = hiragana_sets.default
        self._katakana_sets = katakana_sets.vowels + katakana_sets.k
        self._prompt_queue = self._hiragana_sets.copy()
        self._score = 0
        self._high_score = 0
        self._timer = 0
        self._time_limit = 30
        self._time_remaining = self._time_limit
        self._user_input = ""
        self._round_running = False
        self._running = False
        self.missed_characters = []
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
                ('あ ...', hiragana_sets.vowels),
                ('か ...', hiragana_sets.k),
                ('が ...', hiragana_sets.g),
                ('さ ...', hiragana_sets.s),
                ('ざ ...', hiragana_sets.z),
                ('た ...', hiragana_sets.t),
                ('だ ...', hiragana_sets.d),
                ('な ...', hiragana_sets.n),
                ('は ...', hiragana_sets.h),
                ('ば ...', hiragana_sets.b),
                ('ぱ ...', hiragana_sets.p),
                ('ま ...', hiragana_sets.m),
                ('や ...', hiragana_sets.y),
                ('ら ...', hiragana_sets.r),
                ('わ ...', hiragana_sets.w),
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
            default=45,
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
            self._prompt_queue.pop(0)
            if not self._prompt_queue:
                self.setup_prompt_queue()
        else:
            print("Incorrect input!")
            if not any(c == self._prompt_queue[0][1] for c, _ in self.missed_characters):
                self.missed_characters.append((self._prompt_queue[0][1], 1))
            else:
                for i, (c, n) in enumerate(self.missed_characters):
                    if c == self._prompt_queue[0][1]:
                        self.missed_characters[i] = (c, n + 1)
                        break
        self._user_input = ""

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
        self._timer = 0
        self._user_input = ""
        self._score = 0
        self._time_remaining = self._time_limit
        self.setup_prompt_queue()
        pygame.time.set_timer(self.time_event, 1000)

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
        elif event.type == TEXTINPUT:
            if event.text:
                self._user_input += event.text
        elif event.type == KEYDOWN:
            self.handle_keydown(event)
        elif event.type == TIME_EVENT:
            self._timer += 1

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
        else:
            self._display_surf.blit(
                self.font.render('Press space to start', True, (100, 200, 200)),
                (50, 50),
            )
        if self.missed_characters:
            missed_text = ", ".join(f"{c}:{n}" for n, c in self.missed_characters)
            self._display_surf.blit(
                self.font.render(f'Missed: {missed_text}', True, (200, 100, 100)),
                dest=(50, 250),
            )
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
