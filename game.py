import pygame , random

pygame.init()

DIS_WIDTH = 1200
DIS_HEIGHT = 700

screen = pygame.display.set_mode((DIS_WIDTH,DIS_HEIGHT))
pygame.display.set_caption("Monster Wrangler")

FPS = 60
clock = pygame.time.Clock()

#define classes
class Game():
    """A class to control gameplay"""
    def __init__(self,player,monster_class):
        self.score = 0
        self.round_no = 0
        self.round_tym = 0
        self.frame_cnt = 0

        self.plyr = player
        self.monster_grp = monster_class

        self.nxtLvl_snd = pygame.mixer.Sound("assets/next_level.wav")

        self.font = pygame.font.Font("assets/Abrushow.ttf",24)

        blue_img = pygame.image.load("assets/blue_monster.png")
        green_img = pygame.image.load("assets/green_monster.png")
        purple_img = pygame.image.load("assets/purple_monster.png")
        yellow_img = pygame.image.load("assets/yellow_monster.png")
        self.target_monsters_imgs = [blue_img,green_img,purple_img,yellow_img] #corresponds to monster_ type

        self.target_monster_type = random.randint(0,3)
        self.target_monster_img = self.target_monsters_imgs[self.target_monster_type]

        self.target_monster_rect = self.target_monster_img.get_rect()
        self.target_monster_rect.centerx = DIS_WIDTH//2
        self.target_monster_rect.top = 30

    def update(self):
        self.frame_cnt += 1
        if self.frame_cnt == FPS:
            self.round_tym += 1
            self.frame_cnt = 0
        
        self.check_collisions()

    def draw(self):
        WHITE = (255,255,255)
        BLUE = (20,176,235)
        GREEN = (87,201,47)
        PURPLE = (226,73,243)
        YELLOW = (243,157,20)

        colors = [BLUE,GREEN,PURPLE,YELLOW] 

        catch_txt = self.font.render("Current Catch",True,WHITE)
        catch_rect = catch_txt.get_rect()
        catch_rect.centerx = DIS_WIDTH//2
        catch_rect.top = 5

        score_txt = self.font.render("Score: " + str(self.score),True,WHITE)
        score_rect = score_txt.get_rect(topleft = (5,5))

        lives_txt = self.font.render("Lives: " + str(self.plyr.lives),True,WHITE)
        lives_rect = lives_txt.get_rect(topleft = (5,35))

        round_txt = self.font.render("Round: " + str(self.round_no),True,WHITE)
        round_rect = round_txt.get_rect(topleft = (5,65))

        tym_txt = self.font.render("Round Time: " + str(self.round_tym),True,WHITE)
        tym_rect = tym_txt.get_rect(topright = (DIS_WIDTH-10,5))
        warp_txt = self.font.render("Warps: " + str(self.plyr.warps),True,WHITE)
        warp_rect = warp_txt.get_rect(topright = (DIS_WIDTH-10,35))
        
        screen.blit(catch_txt,catch_rect)
        screen.blit(score_txt,score_rect)
        screen.blit(round_txt,round_rect)
        screen.blit(lives_txt,lives_rect)
        screen.blit(tym_txt,tym_rect)
        screen.blit(warp_txt,warp_rect)
        screen.blit(self.target_monster_img,self.target_monster_rect)
        
        pygame.draw.rect(screen,colors[self.target_monster_type],(DIS_WIDTH//2-32 , 30,64,64),2)
        pygame.draw.rect(screen,colors[self.target_monster_type],(0,100,DIS_WIDTH,DIS_HEIGHT-200),4)
       
    def check_collisions(self):
        collided_monster = pygame.sprite.spritecollideany(self.plyr,self.monster_grp)
        if collided_monster:    
            if collided_monster.type == self.target_monster_type:
                self.score += 100*self.round_no
                collided_monster.remove(self.monster_grp)
                if (self.monster_grp):
                    self.plyr.catch_snd.play()
                    self.choose_new_target()
                else:
                    self.plyr.reset()
                    self.start_new_round()
            else:
                self.plyr.die_snd.play()
                self.plyr.lives -= 1
                if self.plyr.lives <= 0:
                    self.pause_game("Final Score: " + str(self.score) , "Press Enter to play again!")
                    self.reset_game()
                self.plyr.reset()
                    
    def start_new_round(self):
        #score bonus
        self.score += int(10000*self.round_no/(1+self.round_tym))
        #reset round values
        self.round_tym = 0
        self.frame_cnt = 0
        self.round_no += 1
        self.plyr.warps += 1

        for monster in self.monster_grp:
            self.monster_grp.remove(monster)
        
        for i in range(self.round_no):
            self.monster_grp.add(Mosnter(random.randint(0,DIS_WIDTH-64),random.randint(100,DIS_HEIGHT-164),self.target_monsters_imgs[0],0))
            self.monster_grp.add(Mosnter(random.randint(0,DIS_WIDTH-64),random.randint(100,DIS_HEIGHT-164),self.target_monsters_imgs[1],1))
            self.monster_grp.add(Mosnter(random.randint(0,DIS_WIDTH-64),random.randint(100,DIS_HEIGHT-164),self.target_monsters_imgs[2],2))
            self.monster_grp.add(Mosnter(random.randint(0,DIS_WIDTH-64),random.randint(100,DIS_HEIGHT-164),self.target_monsters_imgs[3],3))

            self.choose_new_target()

            self.nxtLvl_snd.play() 

    def choose_new_target(self):
        target_monster = random.choice(self.monster_grp.sprites())
        self.target_monster_type = target_monster.type
        self.target_monster_img = target_monster.image
    def pause_game(self,main_txt,sub_txt):
        WHITE = (255,255,255)
        global running
        main_txt = self.font.render(main_txt,True,WHITE)
        main_rect = main_txt.get_rect(center = (DIS_WIDTH//2,DIS_HEIGHT//2))

        sub_txt = self.font.render(sub_txt,True,WHITE)
        sub_rect = sub_txt.get_rect(center = (DIS_WIDTH//2 , DIS_HEIGHT//2 + 64))

        screen.fill((0,0,0))
        screen.blit(main_txt,main_rect)
        screen.blit(sub_txt,sub_rect)
        pygame.display.update()
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type== pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        is_paused = False
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False
    def reset_game(self):
        self.score = 0
        self.round_no = 0
        self.plyr.lives = 5
        self.plyr.warps = 2
        self.plyr.reset()
        self.start_new_round()

class Player(pygame.sprite.Sprite):
    """"A player class user can control"""
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/knight.png")
        self.rect = self.image.get_rect(centerx = DIS_WIDTH//2)
        self.rect.bottom = DIS_HEIGHT

        self.lives = 5
        self.warps = 2
        self.vecloctiy = 8

        self.catch_snd = pygame.mixer.Sound("assets/catch.wav")
        self.die_snd = pygame.mixer.Sound("assets/die.wav")
        self.warp_snd = pygame.mixer.Sound("assets/warp.wav")

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left>0:
            self.rect.x -= self.vecloctiy
        if keys[pygame.K_RIGHT] and self.rect.right<DIS_WIDTH:
            self.rect.x += self.vecloctiy
        if keys[pygame.K_UP] and self.rect.top>100:
            self.rect.y -= self.vecloctiy
        if keys[pygame.K_DOWN] and self.rect.bottom<DIS_HEIGHT-100:
            self.rect.y += self.vecloctiy
    def warp(self):
        if self.warps>0:
            self.warps -= 1
            self.warp_snd.play()
            self.rect.bottom = DIS_HEIGHT
    def reset(self):
        self.rect.centerx = DIS_WIDTH//2
        self.rect.bottom = DIS_HEIGHT

class Mosnter(pygame.sprite.Sprite):
    """A class to create enimies"""
    def __init__(self,x,y,image,monster_type):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect(topleft = (x,y))
        #monster type => int
        # 0 = blue , 1 = green , 2 = purple , 3 = yellow
        self.type = monster_type

        #set random motion
        self.dx = random.choice([-1,1])
        self.dy = random.choice([-1,1])
        self.velocity = random.randint(1,5)
    def update(self):
        self.rect.x += self.dx*self.velocity
        self.rect.y += self.dy*self.velocity

        if self.rect.left<=0 or self.rect.right>=DIS_WIDTH:
            self.dx = -1*self.dx
        if self.rect.top<=100 or self.rect.bottom>=DIS_HEIGHT-100:
            self.dy = -1*self.dy

my_plyr_grp = pygame.sprite.Group()
my_plyr = Player()
my_plyr_grp.add(my_plyr)

my_monster_grp = pygame.sprite.Group()

my_game = Game(my_plyr,my_monster_grp)
my_game.pause_game("Mosnter Wrangler","Press 'Enter' to begin")
my_game.start_new_round()

running= True
while running:
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            running = False
        if events.type == pygame.KEYDOWN:
            if events.key == pygame.K_SPACE:
                my_plyr.warp()

    screen.fill((0,0,0))

    my_plyr_grp.update()
    my_plyr_grp.draw(screen)

    my_monster_grp.update()
    my_monster_grp.draw(screen)

    my_game.update()
    my_game.draw()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()