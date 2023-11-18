from pygame import *
import pygame
from random import randint
import time 

import math

import sys

interpreter_path = sys.executable
print("Путь к интерпретатору Python:", interpreter_path)



# подгружаем отдельно функции для работы со шрифтом
font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))

font2 = font.Font(None, 36)

#фоновая музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
tresure_sound = mixer.Sound('fire.ogg')

# нам нужны такие картинки:
img_back = "galaxy.jpg" # фон игры
 
img_bullet = "bullet.png" # пуля
img_hero = "rocket.png" # герой
img_enemy = "ufo.png" # враг
 
score = 0 # сбито кораблей
goal = 50 # столько кораблей нужно сбить для победы
lost = 0 # пропущено кораблей
max_lost = 3 # проиграли, если пропустили столько

bonus = False

mixer.music.set_volume(0.1)

# класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
  # конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)

        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
  # метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# класс главного игрока
class Player(GameSprite):
    # метод для управления спрайтом стрелками клавиатуры
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
  # метод "выстрел" (используем место игрока, чтобы создать там пулю)
    def fire(self):
        if bonus == False:
            bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
            bullets.add(bullet)
        else:
            bullet1 = Bullet(img_bullet, self.rect.centerx - 20, self.rect.top, 15, 20, -15)
            bullet2 = Bullet(img_bullet, self.rect.centerx + 20, self.rect.top, 15, 20, -15)
            bullets.add(bullet1, bullet2)

# класс спрайта-врага   
class Enemy(GameSprite):
    # движение врага
    def update(self):
        self.rect.y += self.speed
        global lost
        # исчезает, если дойдет до края экрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
 
# класс спрайта-пули   
class Bullet(GameSprite):
    # движение врага
    def update(self):
        self.rect.y += self.speed
        # исчезает, если дойдет до края экрана
        if self.rect.y < 0:
            self.kill()


# Класс спрайта-монетки
class Coin(GameSprite):
    def __init__(self, player_image, size_x, size_y, player_speed):
        super().__init__(player_image, randint(80, win_width - 80), randint(80, win_height - 80) , size_x, size_y, player_speed)
        self.angle = 0 # Угол, который будет изменяться для создания плавного движения

    def update(self):
        # Изменение угла для создания плавного движения
        self.angle += 0.05

        # Плавное перемещение по экрану с использованием тригонометрических функций
        self.rect.x = 50 + int(200 * math.cos(self.angle))
        self.rect.y = 50 + int(200 * math.sin(self.angle))

        # Обработка границ экрана, чтобы монета не выходила за пределы
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > win_width - self.rect.width:
            self.rect.x = win_width - self.rect.width

        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > win_height - self.rect.height:
            self.rect.y = win_height - self.rect.height






coins = sprite.Group()

# Основной цикл игры:
# ... (ваш код)

# Цикл для появления монеток каждые 10 секунд
last_coin_time = time.time()
coin_interval = 10  # интервал в секундах
 
# Создаем окошко
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
 
# создаем спрайты
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
 
# создание группы спрайтов-врагов
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)
 
bullets = sprite.Group()
 
# переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
# Основной цикл игры:
run = True # флаг сбрасывается кнопкой закрытия окна
while run:
    # событие нажатия на кнопку Закрыть
    for e in event.get():
        if e.type == QUIT:
            run = False
        # событие нажатия на пробел - спрайт стреляет
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()
    
    current_time = time.time()

    if current_time - last_coin_time >= coin_interval:
        coin = Coin("coin.png",  50, 50, randint(1, 3))
        coins.add(coin)
        last_coin_time = current_time


  # сама игра: действия спрайтов, проверка правил игры, перерисовка
    if not finish:
        # обновляем фон
        window.blit(background,(0,0))

        # пишем текст на экране
        text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        # производим движения спрайтов
        ship.update()
        monsters.update()
        bullets.update()
        coins.update()

        # обновляем их в новом местоположении при каждой итерации цикла
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        coins.draw(window)
    
        # проверка столкновения пули и монстров (и монстр, и пуля при касании исчезают)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            # этот цикл повторится столько раз, сколько монстров подбито
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        # возможный проигрыш: пропустили слишком много или герой столкнулся с врагом
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            lost += 1
            if lost > 3:
                finish = True # проиграли, ставим фон и больше не управляем спрайтами.
                window.blit(lose, (200, 200))
            else: 
                continue
        # проверка выигрыша: сколько очков набрали?
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        coin_collides = sprite.groupcollide(bullets, coins, True, True)
        for c in coin_collides:
            tresure_sound.play()
            num = randint(0,1)
            if num == 0:
                bonus = True
            else:
                ship.speed += 2 


        display.update()
    # цикл срабатывает каждую 0.05 секунд
    pygame.time.delay(50)