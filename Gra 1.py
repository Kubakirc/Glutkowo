import pygame
FPS=60
SZEROKOSC=1536
WYSOKOSC=1024
SZEROKOSC_GRACZA=90
WYSOKOSC_GRACZA=150

pygame.init()
screen=pygame.display.set_mode((SZEROKOSC,WYSOKOSC))

background=pygame.image.load("glutkowo_background.png")
ludek = pygame.image.load("gracz.png")
ludek.set_colorkey("#ffffff")

pilka = pygame.image.load("Piłka.png")
pilka.set_colorkey("#ffffff")
pilka = pygame.transform.scale(pilka, (SZEROKOSC_GRACZA/3, SZEROKOSC_GRACZA/3))

wyrzutnia = pygame.image.load("Wyrzurtnia.png")
wyrzutnia.set_colorkey("#ffffff")
wyrzutnia = pygame.transform.scale(wyrzutnia, (SZEROKOSC_GRACZA, SZEROKOSC_GRACZA))


class Gracz:
    sprite_left = pygame.transform.scale(ludek, (SZEROKOSC_GRACZA, WYSOKOSC_GRACZA))
    sprite_right = pygame.transform.flip(sprite_left, True, False)
    
    def __init__(self, hp):
        self.pos_x = SZEROKOSC/4
        self.pos_y = WYSOKOSC/10*7
        self.sprite = Gracz.sprite_right
        self.kierunek = "right"
        self.hp = hp
    
    def draw(self, screen:pygame.Surface):
        screen.blit(self.sprite, (self.pos_x, self.pos_y))
    
    def move_right(self):
        self.sprite = Gracz.sprite_right
        if self.pos_x > SZEROKOSC-SZEROKOSC_GRACZA:
            self.pos_x = SZEROKOSC-SZEROKOSC_GRACZA
        else:
            self.pos_x += 5
        self.kierunek = "right"
    def move_left(self):
        self.kierunek = "left"
        self.sprite = Gracz.sprite_left
        if self.pos_x < 0:
            self.pos_x = 0 
        else:
            self.pos_x -= 5
    
    def skakanie(self):
        if self.pos_y > 0:
            self.pos_y -= 10
        if self.pos_y < 0:
            self.pos_y = pos_ziemia
    
    def spadanie(self):
        if self.pos_y<pos_ziemia:
            self.pos_y+=7
        else: 
            self.pos_y=pos_ziemia

class Pocisk:
    sprite = pilka
    
    def __init__(self, x, y, zadawane_hp):
        self.pos_x = x
        self.pos_y = y
        self.hp = zadawane_hp
        self.speed = 10
    
    def draw(self, screen:pygame.Surface):
        screen.blit(Pocisk.sprite, (self.pos_x, self.pos_y))

class Bazooka:
    sprite_left = wyrzutnia
    sprite_right=pygame.transform.flip(sprite_left, True, False)
    rotation_offset = pygame.math.Vector2(50, 70)
    
    def __init__(self):
        self.sprite = Bazooka.sprite_right
        self.rotation_offset = Bazooka.rotation_offset
    
    def aktualizacja_współrzędnych(self, x, y, kierunek_gracza):
        self.pos_x = x
        self.pos_y = y
        if kierunek_gracza=="left":
            self.sprite=Bazooka.sprite_left
        else:
            self.sprite=Bazooka.sprite_right
    def oś_obrotu(self, offset:list, screen:pygame.Surface):
        x = self.pos_x + offset[0]
        y = self.pos_y + offset[1]
        center = (x, y)
        pygame.draw.circle(screen, "red", center, 4)
    
    def draw(self, screen:pygame.Surface):
        pos_x = self.pos_x
        pos_y = self.pos_y
        
        screen.blit(self.sprite, (pos_x - self.sprite.get_width()//2, pos_y - self.sprite.get_height()//2 ))
        self.oś_obrotu([50, 70], screen)
    
    def rotate (self, pozycja_myszki):
        odleglosc = pygame.math.Vector2(pozycja_myszki)-(self.pos_x,self.pos_y)
        wektor_osi_x = pygame.math.Vector2(1, 0)
        kat = odleglosc.angle_to(wektor_osi_x) - 42
        if self.sprite == Bazooka.sprite_left:
            kat=kat-90
        self.sprite = pygame.transform.rotate(self.sprite, kat)
        self.rotation_offset = Bazooka.rotation_offset.rotate(kat)


pos_ziemia = WYSOKOSC/10*7

gracz = Gracz(100)
bazoka = Bazooka()
pocisk = None
burki = []

clock=pygame.time.Clock()
run_game = True
while run_game:
    screen.fill("black")
    screen.blit(background)
    # dest: RectLike = (0, 0)
    # destination powinno być zmienną typu RectLike
    # RectLike = (liczba, liczba)
    # dest: typ_zmiennej = (0, 0)
    
    event_list = pygame.event.get()
    for event in event_list:
        if event.type==pygame.QUIT:
            run_game=False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click_pos = pygame.mouse.get_pos()
                click_x = click_pos[0]
                click_y = click_pos[1]
                pocisk = Pocisk(click_x, click_y, 10)
        
    keyboard = pygame.key.get_pressed()
    if keyboard[pygame.K_RIGHT] or keyboard[pygame.K_d]:
        gracz.move_right()

    if keyboard[pygame.K_LEFT]or keyboard[pygame.K_a]:
        gracz.move_left()
            
    if keyboard[pygame.K_SPACE] or keyboard[pygame.K_w]:
        gracz.skakanie()
    else:
        gracz.spadanie()
    
    bazoka.aktualizacja_współrzędnych(gracz.pos_x, gracz.pos_y+30, gracz.kierunek)
    
    pozycja_myszki = pygame.mouse.get_pos()  # (x, y)
    bazoka.rotate(pozycja_myszki)
    
    gracz.draw(screen)
    bazoka.draw(screen)
    
    if isinstance(pocisk, Pocisk):
        pocisk.draw(screen)
    
    pygame.display.update()
    clock.tick(FPS)





pygame.quit()
