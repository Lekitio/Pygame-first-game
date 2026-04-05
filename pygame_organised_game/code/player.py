
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.Surface((40, 60))
        self.rect = self.image.get_frect(bottomleft = pos)
        self.hitbox_rect = self.rect.inflate(-10, 0)
        #Movement
        self.velocity = pygame.math.Vector2()
        self.speed = 300
        self.collision_sprites = collision_sprites
        #Jump
        self.init_jump()

    def init_jump(self):
        #variables ig?
        self.can_jump = True
        self.current_jump_time = 0
        self.last_jump_time = 0
        self.on_ground = True

        #constants
        self.jump_force = 800
        self.jump_key = pygame.K_z
        self.jump_cooldown = 100
        self.jump_speed_cap = 600
        self.jump_velocity_multiplier = 0.6

        #pos change to checcking collisions instead
        # self.groundy = ground.top

    def input(self, dt):
        keys = pygame.key.get_pressed()
        self.jump(keys, dt) # changes y velocity
        self.velocity.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])

    def move(self, dt):
        self.hitbox_rect.x += self.velocity.x * self.speed * dt
        self.collision("x")
        self.hitbox_rect.y += self.velocity.y * dt
        self.collision("y")
        self.rect.center = self.hitbox_rect.center

#Jump methods
    def can_jump_cooldown(self):
        if not self.can_jump:
            self.current_jump_time = pygame.time.get_ticks()
            if self.current_jump_time >= self.last_jump_time + self.jump_cooldown:
                self.can_jump = True

    def landing(self):
        if self.on_ground == False:
            self.last_jump_time = pygame.time.get_ticks()
        self.on_ground = True
        self.velocity.y = 0
        self.can_jump = False
        self.can_jump_cooldown()

    def jump(self, keys, delta_time):
        if keys[self.jump_key] and self.on_ground and self.can_jump:
            self.velocity.y = -self.jump_force
            self.on_ground = False
        self.velocity.y += GRAVITY * delta_time #always affected by gravity
        
        # downwards
        if self.velocity.y > 0:
            self.velocity.y += self.jump_velocity_multiplier * GRAVITY * delta_time
            #why times delta_time here?
            
        #if släppa and upwards
        if not keys[self.jump_key] and self.velocity.y < 0:
            self.velocity.y *= 0.1

        # a speed cap
        self.velocity.y = min(self.jump_speed_cap, self.velocity.y)


    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == "x":
                    if self.velocity.x > 0:
                        #moving right
                        self.hitbox_rect.right = sprite.rect.left
                    elif self.velocity.x < 0:
                        #Moving left
                        self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.velocity.y < 0:
                        #moving up
                        self.hitbox_rect.top = sprite.rect.bottom + 0.1 # so when it falls it wont hit
                        self.velocity.y = 0 #stop jumping

                    elif self.velocity.y > 0:
                        #moving down
                        self.hitbox_rect.bottom = sprite.rect.top
                        self.landing()
    
    def update(self, dt):
        self.input(dt)
        self.move(dt)
        