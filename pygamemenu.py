# pygame_fullscreen_menu.py

import sys
import time

import cv2
import numpy as np
import pygame
import mss

class FullscreenMenu:
    def __init__(self, video_path, volume=0.5, fps=30):
        pygame.init()
        pygame.mixer.init()

        self.VIDEO_PATH = video_path
        self.cap = cv2.VideoCapture(self.VIDEO_PATH)
        if not self.cap.isOpened():
            raise IOError(f"Cannot open video: {self.VIDEO_PATH}")

        info = pygame.display.Info()
        self.WIDTH, self.HEIGHT = info.current_w, info.current_h
        self.flags = pygame.FULLSCREEN | pygame.SCALED | pygame.HWSURFACE | pygame.DOUBLEBUF
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), self.flags)
        pygame.display.set_caption("Game Menu")

        self.FONT = pygame.font.SysFont('arial', 48)
        self.SMALL_FONT = pygame.font.SysFont('arial', 36)

        self.volume = volume
        pygame.mixer.music.set_volume(self.volume)

        self.clock = pygame.time.Clock()
        self.fps = fps
    
    def play_intro(self, logo_path, sound_path):
        logo_orig = pygame.image.load(logo_path).convert_alpha()
        logo_ratio = logo_orig.get_width() / logo_orig.get_height()
        screen_ratio = self.WIDTH / self.HEIGHT

        if logo_ratio > screen_ratio:
            new_width = self.WIDTH
            new_height = int(self.WIDTH / logo_ratio)
        else:
            new_height = self.HEIGHT
            new_width = int(self.HEIGHT * logo_ratio)

        logo = pygame.transform.smoothscale(logo_orig, (new_width, new_height))
        logo_rect = logo.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))

        sound = pygame.mixer.Sound(sound_path)
        sound.play()

        fade_duration = 0.5
        show_duration = 1.5
        text_fade_duration = 1.0
        text_show_duration = 2.0
        total_duration = fade_duration * 2 + show_duration + text_fade_duration * 2 + text_show_duration

        start_time = time.time()
        text_start_time = None
        running = True

        while running:
            elapsed = time.time() - start_time
            self.screen.fill((0, 0, 0))

            # Logo fade in
            if elapsed < fade_duration:
                alpha = int((elapsed / fade_duration) * 255)
                logo.set_alpha(alpha)
                self.screen.blit(logo, logo_rect)

            # Logo show
            elif elapsed < fade_duration + show_duration:
                logo.set_alpha(255)
                self.screen.blit(logo, logo_rect)

            # Logo fade out
            elif elapsed < fade_duration * 2 + show_duration:
                alpha = int(255 - ((elapsed - fade_duration - show_duration) / fade_duration) * 255)
                logo.set_alpha(alpha)
                self.screen.blit(logo, logo_rect)

            # Text fade in
            elif elapsed < fade_duration * 2 + show_duration + text_fade_duration:
                if text_start_time is None:
                    text_start_time = time.time()
                text_elapsed = time.time() - text_start_time
                alpha = int((text_elapsed / text_fade_duration) * 255)
                text = self.SMALL_FONT.render("A game by Cocciclaque", True, (255, 255, 255))
                text.set_alpha(alpha)
                self.screen.blit(text, text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2)))

            # Text show
            elif elapsed < fade_duration * 2 + show_duration + text_fade_duration + text_show_duration:
                text = self.SMALL_FONT.render("A game by Cocciclaque" , True, (255, 255, 255))
                text.set_alpha(255)
                self.screen.blit(text, text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2)))

            # Text fade out
            elif elapsed < total_duration:
                fade_out_elapsed = elapsed - (fade_duration * 2 + show_duration + text_fade_duration + text_show_duration)
                alpha = int(255 - (fade_out_elapsed / text_fade_duration) * 255)
                text = self.SMALL_FONT.render("A game by", True, (255, 255, 255))
                text.set_alpha(max(0, alpha))
                self.screen.blit(text, text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2)))

            else:
                running = False

            pygame.display.flip()

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.clock.tick(self.fps)


    def _draw_menu(self, options, selected_idx):
        for i, txt in enumerate(options):
            col = (255, 255, 0) if i == selected_idx else (255, 255, 255)
            lbl = self.FONT.render(txt, True, col)
            self.screen.blit(lbl, lbl.get_rect(center=(self.WIDTH//2, self.HEIGHT//2 + i*60)))

    def _draw_options(self, opts, sel):
        for i, (fn, _) in enumerate(opts):
            txt = fn()
            col = (0, 255, 255) if i == sel else (200, 200, 200)
            lbl = self.SMALL_FONT.render(txt, True, col)
            self.screen.blit(lbl, lbl.get_rect(center=(self.WIDTH//2, self.HEIGHT//2 + i*50)))

    def _draw_background(self):
        ret, frame = self.cap.read()
        if not ret:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (self.WIDTH, self.HEIGHT))
        return pygame.image.frombuffer(frame.tobytes(), (self.WIDTH, self.HEIGHT), 'RGB')

    def options_menu(self):
        fullscreen = True
        opts = [ (lambda: f"Fullscreen: {'On' if fullscreen else 'Off'}", 'toggle_fullscreen'),
                 (lambda: f"Volume: {int(self.volume*100)}%", 'change_volume'),
                 (lambda: 'Back', 'back') ]
        sel = 0
        running = True
        while running:
            menu = [(fn(), act) for fn, act in opts]
            bg = self._draw_background()
            self.screen.blit(bg, (0, 0))
            self._draw_options(menu, sel)
            pygame.display.flip()
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_UP:
                        sel = (sel - 1) % len(menu)
                    if ev.key == pygame.K_DOWN:
                        sel = (sel + 1) % len(menu)
                    if ev.key == pygame.K_RETURN:
                        _, act = menu[sel]
                        if act == 'toggle_fullscreen':
                            fullscreen = not fullscreen
                            flags = self.flags if fullscreen else pygame.RESIZABLE | pygame.SCALED
                            self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), flags)
                        elif act == 'change_volume':
                            self.volume = min(1.0, self.volume + 0.1)
                            pygame.mixer.music.set_volume(self.volume)
                        elif act == 'back':
                            running = False
            self.clock.tick(self.fps)

    def run(self):
        menu_options = ['Start Game', 'Options', 'Quit']
        selected = 0
        running = True
        while running:
            bg = self._draw_background()
            self.screen.blit(bg, (0, 0))
            self._draw_menu(menu_options, selected)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = (selected - 1) % len(menu_options)
                    elif event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(menu_options)
                    elif event.key == pygame.K_RETURN:
                        choice = menu_options[selected]
                        if choice == 'Start Game':
                            print("Starting game...")
                        elif choice == 'Options':
                            self.options_menu()
                        elif choice == 'Quit':
                            running = False
            self.clock.tick(self.fps)

        pygame.quit()

if __name__ == '__main__':
    menu = FullscreenMenu('background.mp4')
    menu.play_intro('studio_logo.png', 'studio_intro.mp3')
    menu.run()
