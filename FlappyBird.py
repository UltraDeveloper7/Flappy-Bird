import sys,random,pygame

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class FlappyBird():
    def __init__(self, bird_choice, background_choice, pipe_choice):
        pygame.mixer.get_init()
        pygame.init()
        self.gravity = 0.42
        self.bird_movement = 0
        self.game_active = True
        self.can_score = True
        self.score = 0
        self.high_score = 0
        self.score_countdown = 0
        self.floor_x_pos = 0
        self.pipe_list = []
        self.pipe_height = [400, 600, 800]
        self.bird_index = 0

        # Initialize display variables
        self.screen_width = 576
        self.screen_height = 1024
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height))
        pygame.display.set_caption('Flappy Bird')
        self.clock = pygame.time.Clock()
        self.game_font = pygame.font.Font('04B_19.ttf', 40)

        # Load all surfaces and convert alpha
        self.bg_surface = pygame.transform.scale2x(pygame.image.load(
            background_choice).convert_alpha())
        self.floor_surface = pygame.transform.scale2x(
            pygame.image.load('assets/base.png').convert_alpha())
        self.floor_width = self.floor_surface.get_width()
        self.pipe_surface = pygame.transform.scale2x(
            pygame.image.load(pipe_choice).convert_alpha())

        # Initialize the bird movement frames
        if 'assets/redbird-midflap.png' in bird_choice:
            self.bird_downflap = pygame.transform.scale2x(
                pygame.image.load('assets/redbird-downflap.png').convert_alpha())
            self.bird_midflap = pygame.transform.scale2x(
                pygame.image.load('assets/redbird-midflap.png').convert_alpha())
            self.bird_upflap = pygame.transform.scale2x(
                pygame.image.load('assets/redbird-upflap.png').convert_alpha())
        elif 'assets/bluebird-midflap.png' in bird_choice:
            self.bird_downflap = pygame.transform.scale2x(
                pygame.image.load('assets/bluebird-downflap.png').convert_alpha())
            self.bird_midflap = pygame.transform.scale2x(
                pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
            self.bird_upflap = pygame.transform.scale2x(
                pygame.image.load('assets/bluebird-upflap.png').convert_alpha())
        elif 'assets/yellowbird-midflap.png' in bird_choice:
            self.bird_downflap = pygame.transform.scale2x(
                pygame.image.load('assets/yellowbird-downflap.png').convert_alpha())
            self.bird_midflap = pygame.transform.scale2x(
                pygame.image.load('assets/yellowbird-midflap.png').convert_alpha())
            self.bird_upflap = pygame.transform.scale2x(
                pygame.image.load('assets/yellowbird-upflap.png').convert_alpha())
        self.bird_frames = [self.bird_downflap, self.bird_midflap, self.bird_upflap]
        self.bird_surface = self.bird_frames[self.bird_index]
        self.bird_rect = self.bird_surface.get_rect(center=(100, 512))

        # Game Over Surface
        self.game_over_surface = pygame.transform.scale2x(
            pygame.image.load('assets/gameover.png').convert_alpha())
        self.game_over_rect = self.game_over_surface.get_rect(center=(288, 512))
        self.game_over_text_surface = self.game_font.render("Press Space to Restart", True, BLACK)
        self.game_over1_text_surface = self.game_font.render("or Q for quitting", True, BLACK)
        self.text_width = self.game_over_text_surface.get_width()
        self.text_width1 = self.game_over1_text_surface.get_width()
        self.text_x = self.screen_width // 2 - self.text_width // 2
        self.text_y = 580
        self.text_x1 = self.screen_width // 2 - self.text_width1 // 2
        self.text_y1 = 620


        # Sounds
        self.flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
        self.death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
        self.score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
        self.score_sound_countdown = 100

        # Create the event-instances
        self.BIRDFLAP = pygame.USEREVENT + 1
        pygame.time.set_timer(self.BIRDFLAP, 200)
        self.SPAWNPIPE = pygame.USEREVENT
        pygame.time.set_timer(self.SPAWNPIPE, 1200)
        self.SCOREEVENT = pygame.USEREVENT + 2
        pygame.time.set_timer(self.SCOREEVENT, 100)

    def draw_floor(self):
        """Draw the floor surface on the screen."""
        self.screen.blit(self.floor_surface, (self.floor_x_pos, 900))
        self.screen.blit(self.floor_surface, (self.floor_x_pos + self.floor_width, 900))

    def create_pipe(self):
        """Create two pipe rectangles: top and bottom pipes."""
        random_pipe_pos = random.choice(self.pipe_height)
        bottom_pipe = self.pipe_surface.get_rect(midtop=(700, random_pipe_pos))
        top_pipe = self.pipe_surface.get_rect(midbottom=(700, random_pipe_pos - 300))
        return bottom_pipe, top_pipe

    def draw_pipes(self, pipes):
        """Draw the pipes on the screen."""
        for pipe in pipes:
            if pipe.bottom >= self.screen_height:
                self.screen.blit(self.pipe_surface, pipe)
            else:
                flip_pipe = pygame.transform.flip(self.pipe_surface, False, True)
                self.screen.blit(flip_pipe, pipe)
                
            if (pipe.centerx + pipe.width/2) < self.bird_rect.centerx:
                if not self.score_countdown:
                    self.score += 1
                    self.score_sound.play()
                    self.score_countdown = 100
        if self.score_countdown:
            self.score_countdown -= 1

    def move_pipes(self, pipes):
        """Move the pipes to the left."""
        for pipe in pipes:
            pipe.centerx -= 5
        visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
        return visible_pipes
    
    def check_collision(self, pipes):
        """Check if the bird collides with pipes or goes out of the screen."""
        for pipe in pipes:
            if self.bird_rect.colliderect(pipe):
                self.death_sound.play()
                self.can_score = True
                return False
        if self.bird_rect.top <= -100 or self.bird_rect.bottom >= 900:
            self.can_score = True
            return False
        return True
    
    def pipe_score_check(self):
        """Check if the bird passes the pipes to add score."""
        if self.pipe_list:
            for pipe in self.pipe_list:
                if pipe.centerx < 10 and not pipe.bottom > 800:
                    if not self.can_score:
                        self.score += 1
                        self.score_sound.play()
                        self.can_score = True
                if pipe.centerx < -50:
                    self.pipe_list.remove(pipe)
                    break
        self.high_score = self.update_score(self.score, self.high_score)

    def rotate_bird(self, bird):
        """Rotate the bird image based on its movement."""
        new_bird = pygame.transform.rotozoom(bird, -self.bird_movement * 2, 1)
        return new_bird

    def bird_animation(self):
        """Animate the bird's wings by updating the bird index."""
        new_bird = self.bird_frames[self.bird_index]
        new_bird_rect = new_bird.get_rect(center=(100, self.bird_rect.centery))
        return new_bird, new_bird_rect

    def score_display(self, game_state):
        """Display the score on the screen."""
        if game_state == 'main_game':
            score_surface = self.game_font.render(
                str(int(self.score)), True, "WHITE")
            score_rect = score_surface.get_rect(center=(288, 100))
            self.screen.blit(score_surface, score_rect)
        if game_state == 'game_over':
            score_surface = self.game_font.render(
                f'Score: {int(self.score)}', True, "WHITE")
            score_rect = score_surface.get_rect(center=(288, 100))
            self.screen.blit(score_surface, score_rect)

            high_score_surface = self.game_font.render(
                f'High score: {int(self.high_score)}', True, "WHITE")
            high_score_rect = high_score_surface.get_rect(center=(288, 850))
            self.screen.blit(high_score_surface, high_score_rect)

    def update_score(self, score, high_score):
        """Update the high score based on the current score."""
        if score > high_score:
            high_score = score
        return high_score    
    
    def reset_game(self):
        """Reset the game when the user presses the space bar after game over."""
        self.game_active = True
        self.pipe_list = []
        self.bird_rect.center = (100, 512)
        self.bird_movement = 0
        self.score = 0
        self.can_score = True            

    def run(self):
        """Main game loop."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.game_active:
                        self.bird_movement = 0
                        self.bird_movement -= 12
                        self.flap_sound.play()
                    if event.key == pygame.K_SPACE and not self.game_active:
                        self.game_active = True
                        self.reset_game()
                if event.type == self.SPAWNPIPE:
                    self.pipe_list.extend(self.create_pipe())
                
                if event.type == self.BIRDFLAP:
                    if self.bird_index < 2:
                        self.bird_index += 1
                    else:
                        self.bird_index = 0

                    self.bird_surface, self.bird_rect = self.bird_animation()

                if event.type == self.SCOREEVENT:
                    if self.game_active:
                        self.pipe_score_check()
                        self.score_sound_countdown -= 1
                        if self.score_sound_countdown <= 0:
                            self.score_sound.play()
                            self.score_sound_countdown = 100

            self.screen.blit(self.bg_surface,(0,0))

            if self.game_active:
                # Bird
                self.bird_movement += self.gravity
                rotated_bird = self.rotate_bird(self.bird_surface)
                self.bird_rect.centery += self.bird_movement
                self.screen.blit(rotated_bird, self.bird_rect)
                self.game_active = self.check_collision(self.pipe_list)

                # Pipes
                self.pipe_list = self.move_pipes(self.pipe_list)
                self.draw_pipes(self.pipe_list)

                # Score
                self.score_display('main_game')
            else:
                self.screen.blit(self.game_over_surface, self.game_over_rect)
                self.screen.blit(self.game_over_text_surface,(self.text_x,self.text_y))
                self.screen.blit(self.game_over1_text_surface,(self.text_x1, self.text_y1))
                self.high_score = self.update_score(self.score, self.high_score)
                self.score_display('game_over')
                
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    self.reset_game()

            # Floor
            self.floor_x_pos -= 1
            self.draw_floor()
            if self.floor_x_pos <= -self.floor_width:
                self.floor_x_pos = 0

            pygame.display.update()
            self.clock.tick(120)