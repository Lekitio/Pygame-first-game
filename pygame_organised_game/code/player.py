
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, wall_collision_sprites, enemy_collision_sprites):
        super().__init__(groups)
        self.scalar = 0.16
        self.image = pygame.image.load(join("images", "playerdeafult2_1.png")).convert_alpha()
        self.image = pygame.transform.smoothscale_by(self.image, self.scalar)
        # self.image.fill((30,50,50))
        self.rect = self.image.get_frect(bottomleft = pos)
        self.hitbox_rect = self.rect.inflate(-40, -10) #this checks collisions

        #Movement
        self.velocity = pygame.math.Vector2()
        self.speed = 300
        self.wall_collision_sprites = wall_collision_sprites
        self.acc = 10
        #Jump
        self.init_jump()

    def init_slice(self):
        #constants
        self.slice_key = pygame.K_x
        self.slice_cooldown = 50

        #variables
        self.slicing = False
        self.can_slice = True


    def init_jump(self):
        #variables ig?
        self.can_jump = True
        self.current_jump_time = 0
        self.last_jump_time = 0
        self.on_ground = True
        self.can_jump_check = True

        #constants
        self.jump_force = 800
        self.jump_key = pygame.K_z
        self.jump_cooldown = 100
        self.jump_speed_cap = 800
        self.jump_velocity_multiplier = 0.6

        #jumping buffer
        # self.jump_buffer = 0.1

        #pos change to checcking collisions instead
        # self.groundy = ground.top

    def input(self, dt):
        keys = pygame.key.get_pressed()
        # preferably get_just_pressed but bugs out # if pygame.key.get_just_pressed()[pygame.K_x] and self.on_ground:
        self.jump(keys, dt) # changes y velocity
        self.walking_acceleration(keys, dt)
        # self.velocity.x = (keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        
        self.hitting(keys, dt)

    def move(self, dt):
        #jump mechanics
        self.velocity.y += GRAVITY * dt #always affected by gravity
        self.velocity.y = min(self.jump_speed_cap, self.velocity.y)

        # moving and collision
        self.hitbox_rect.x += self.velocity.x * self.speed * dt
        self.wall_collision("x")
        self.hitbox_rect.y += self.velocity.y * dt
        self.wall_collision("y")
        self.rect.center = self.hitbox_rect.center

        

    def walking_acceleration(self, keys, dt):
        direction = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])

        max_speed = 1
        
        if self.velocity.x * direction < 0: #you are turning
            self.velocity.x = 0
        if direction != 0:
            self.velocity.x += direction * self.acc*dt

            #only while walking do i care about max speed
            if abs(self.velocity.x) > max_speed:
                self.velocity.x = max_speed*direction
        else:
            self.velocity.x = 0

    def hitting(self):
        if self.keys[self.slice_key] and self.can_slice:
            #slice
            self.can_slice = False
            self.last_slice_time = pygame.time.get_ticks()

        self.slicing_cooldown()

        #chck if you change state, falling -> on ground or on ground -> jumping or maybe not necessary if very fast


    def slicing_cooldown(self):
        if not self.can_slice:
            self.current_slice_time = pygame.time.get_ticks()
            if self.current_slice_time >= self.last_slice_time + self.slice_cooldown:

    

#Jump methods
    def can_jump_cooldown(self):
        if not self.can_jump:
            self.current_jump_time = pygame.time.get_ticks()
            if self.current_jump_time >= self.last_jump_time + self.jump_cooldown:
                self.can_jump = True
                self.can_jump_check = True

    # def jump_off_platform(self):
    #     #timer ig so you can jump for a period after off platform
    #     #if not jumping and off ground, eg velocity.y >= 0
    #     if not self.can_jump:
    #         now = pygame.time.get_ticks()
    #         if now >= self.last_jump_time + self.jump_buffer:

    def landing(self):
        if self.can_jump_check:
            self.last_jump_time = pygame.time.get_ticks()
        self.velocity.y = 0
        self.can_jump_check = False
        self.can_jump = False
        self.can_jump_cooldown()
        # if not self.can_jump_check and self.on_ground:
            #during this short time period
            #jump has a buffer until its set to False
        


    def jump(self, keys, delta_time):
        if keys[self.jump_key] and self.on_ground and self.can_jump:
            self.velocity.y = -self.jump_force
            self.on_ground = False
        
        # downwards
        if self.velocity.y > 0:
            self.velocity.y += self.jump_velocity_multiplier * GRAVITY * delta_time
            #why times delta_time here?
            
        #if släppa and upwards
        if not keys[self.jump_key] and self.velocity.y < 0:
            self.velocity.y *= 0.1

        # a speed cap

    #collision checking
    def wall_collision(self, direction):
        for sprite in self.wall_collision_sprites: #this is checking all
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
                        self.on_ground = True
                        self.landing()
    
    def enemy_collision(self, slice_direction):
        for enemy_sprite in self.wall_collision_sprites:
            if enemy_sprite.rect.colliderect(self.hitbox_rect):
                #if players hitbox is hitting the enemy_sprite
                #now I have the "id" of the enemy i'm hitting -> can modify it?


    # def collision(self, direction):
    #     self.wall_collision(direction)
    #     self.enemy_collision(direction) #lets do that for now, since we have no knife
        
    
    # def do_damage(self, e_sprite):
    #     e_sprite.health -= self.damage
    #     #make particles


    # def enemy_collision(self, enemy_sprites):
    #     for e_sprite in enemy_sprites:
    #         if e_sprite.recct.colliderect(self.hitbox_rect): #if this enemy is hitting player


    def update(self, dt):
        self.input(dt)
        self.move(dt)
        
