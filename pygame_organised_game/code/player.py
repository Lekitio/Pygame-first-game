from enemies import *
from settings import *
from sprites import VisualSprite

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
        self.acc = 10
        self.direction = 0
        #Jump
        self.init_jump()
        self.init_slice()

        self.wall_collision_sprites = wall_collision_sprites
        self.enemy_collision_sprites = enemy_collision_sprites

        self.weapon = Player_weapon(pos, groups, self)

    def init_slice(self):
        #constants
        self.slice_cooldown = 50
        self.hitting_distance = 20 #pixels?
        self.slice_dmg = 1

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
        
        self.weapon.hitting(keys, dt)

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
        self.direction = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])

        max_speed = 1
        
        if self.velocity.x * self.direction < 0: #you are turning
            self.velocity.x = 0
        if self.direction != 0:
            self.velocity.x += self.direction * self.acc*dt

            #only while walking do i care about max speed
            if abs(self.velocity.x) > max_speed:
                self.velocity.x = max_speed*self.direction
        else:
            self.velocity.x = 0


            #slice
            # self.can_slice = False
            # self.last_slice_time = pygame.time.get_ticks()


        # self.slicing_cooldown()

        #chck if you change state, falling -> on ground or on ground -> jumping or maybe not necessary if very fast


    # def slicing_cooldown(self):
    #     if not self.can_slice:
    #         self.current_slice_time = pygame.time.get_ticks()
    #         if self.current_slice_time >= self.last_slice_time + self.slice_cooldown:

    

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
        if keys[jump_key] and self.on_ground and self.can_jump:
            self.velocity.y = -self.jump_force
            self.on_ground = False
        
        # downwards
        if self.velocity.y > 0:
            self.velocity.y += self.jump_velocity_multiplier * GRAVITY * delta_time
            #why times delta_time here?
            
        #if släppa and upwards
        if not keys[jump_key] and self.velocity.y < 0:
            self.velocity.y *= 0.1

        # a speed cap

    #collision checking
    def wall_collision(self, xy_coordinate):
        for sprite in self.wall_collision_sprites: #this is checking all
            if sprite.rect.colliderect(self.hitbox_rect): 
                if xy_coordinate == "x":
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

    # def collision(self, direction):
    #     self.wall_collision(direction)
    #     self.enemy_collision(direction) #lets do that for now, since we have no knife
        

    # def enemy_collision(self, enemy_sprites):
    #     for e_sprite in enemy_sprites:
    #         if e_sprite.recct.colliderect(self.hitbox_rect): #if this enemy is hitting player


    def update(self, dt):
        self.input(dt)
        self.move(dt)
        
class Player_weapon(VisualSprite):
    #(Player) makes player_weapon be able to acess player
    #Making the weapon to handle combat features
    #both to organise well and to avoid conflicts with collision as a player
    def __init__(self, pos, groups, player):#means: Go get these informations from my parent class anc return here with them
        self.image = pygame.image.load(join("images", "sword.png")).convert_alpha()
        self.scalar = 0.02
        self.image = pygame.transform.smoothscale_by(self.image, self.scalar)

        self.player = player

        super().__init__(pos, self.image, groups)
        #weapon_rect = Player.hitbox_rect.copy()
    
    def update(self, dt):
        self.rect.center = self.player.rect.center
        self.rect.center = (self.rect.center[0] +18, self.rect.center[1])

    def hitting(self, keys, dt):
        if keys[slice_key] and self.can_slice:

            temp = self.hitbox_rect.copy()
            temp.x += self.direction*self.hitting_distance
            self.enemy_collision(temp) #this is just attacking left and right
            #sends in a rectangle
            #does this change hitbox rect?
    
    def enemy_collision(self, checking_rect): #returns the list of all the enemy getting collided with
        collide_list = [enemy for enemy in self.player.enemy_collision_sprites if checking_rect.colliderect(enemy.rect)] #when looking at individual sprites they are treated as rects?
        # pygame.sprite.spritecollide(checking_rect, self.enemy_collision_sprites, False)
        #(check, list_check, kill?)
        
        for enemy in collide_list:
            enemy.handle_hit(self.slice_dmg) #sends it to the enemy class tot ake care of
            
    
            # self.apply_knockback()
                        # self.apply_knockback()
                #removes enemy from all sprite groups

                #make them do some animation

                #make screen freeze
            # self.screen_freeze(duration=100) #miliseconds
            # else:
            #     #flash red
            #     enemy.trigger_flash(color=(255, 0, 0))

            #     #they and the player take knockback
            #     self.apply_knockback(enemy)
            #     enemy.apply_knockback()

    # def apply_knockback(self, enemy):
    #     #make the player take knockback
    #     #use
    #     self.direction
    #     #for help


