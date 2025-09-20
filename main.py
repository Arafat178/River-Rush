import pygame
from pygame import mixer
import json
import random
import requests

pygame.init()


screen = pygame.display.set_mode((600,800))

mixer.music.load('assets/sounds/bgm.ogg')
river1 = pygame.image.load("assets/images/river1.png")
river2 = pygame.image.load("assets/images/river2.png")
river3 = pygame.image.load("assets/images/river3.png")
river4 = pygame.image.load("assets/images/river4.png")
river5 = pygame.image.load("assets/images/river5.png")
river6 = pygame.image.load("assets/images/river6.png")
boat = pygame.image.load("assets/images/boat1.png")
wood1 = pygame.image.load("assets/images/wood1.png")
wood2 = pygame.image.load("assets/images/wood2.png")
wood3 = pygame.image.load("assets/images/wood3.png")

river_speed = 0
def riverXY(x,y,river_speed):
    if river_speed>=0 and river_speed<=50:
        screen.blit(river1,(x,y))
    elif river_speed>=51 and river_speed<=100:
        screen.blit(river2, (x, y))
    elif river_speed >= 101 and river_speed <= 150:
        screen.blit(river3, (x, y))
    elif river_speed >= 151 and river_speed <= 200:
        screen.blit(river4, (x, y))
    elif river_speed >= 201 and river_speed <= 250:
        screen.blit(river5, (x, y))
    else:
        screen.blit(river6,(x,y))

boat_x = 300
boat_y = 520
boat_xChange = 0 #change

def boatXY(x,y):
    screen.blit(boat,(x,y))

#floating wood
wood1_x = 170
wood1_y = -50

wood2_x = 320
wood2_y = -200

wood3_x = 350
wood3_y = -350

wood4_x = 220
wood4_y = -480

wood5_x = 190
wood5_y = -630

wood_speed = 2 #change

def woodXY(x,y,wood_img):
    screen.blit(wood_img,(x,y))


# user interface
gameStart = False
button_start = pygame.Rect(200, 690, 250, 80)
button_pad = pygame.Rect(0, 650, 600, 150)  # x,y,w,h
button_left = pygame.Rect(20, 660, 120, 120)
button_right = pygame.Rect(460, 660, 120, 120)

font_btn= pygame.font.SysFont('freesansbold.ttf', 40)

def draw_start_button():
    pygame.draw.rect(screen, (10, 200, 10), button_start, border_radius=20)
    text = font_btn.render("START", True, (0, 0, 0))
    screen.blit(text, (button_start.x + 50, button_start.y + 20))
def draw_button_pad():
    pygame.draw.rect(screen, (200, 150, 200), button_pad)
def draw_buttons():
    pygame.draw.rect(screen, (100, 100, 100), button_left, border_radius= 20)
    text = font_btn.render("<<", True, (0, 0, 0))
    screen.blit(text, (button_left.x + 30, button_left.y + 50))

    pygame.draw.rect(screen, (100, 100, 100), button_right, border_radius=20)
    text = font_btn.render(">>", True, (0, 0, 0))
    screen.blit(text, (button_right.x + 60, button_right.y + 50))

# On-screen keyboard
keys_rows = [
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
    ["Z", "X", "C", "V", "B", "N", "M", "DEL", "ENT"]
]

key_buttons = []
key_width = 55
key_height = 60
padding = 5
start_x = 5
start_y = 450

for row_idx, row in enumerate(keys_rows):
    for col_idx, k in enumerate(row):
        rect = pygame.Rect(
            start_x + col_idx * (key_width + padding),
            start_y + row_idx * (key_height + padding),
            key_width, key_height
        )
        key_buttons.append((k, rect))
#name box
name_font = pygame.font.SysFont('freesansbold.ttf', 50)

input_box = pygame.Rect(150, 350, 400, 60)  # x, y, width, height
color_inactive = (100, 100, 100)
color_active = (0, 200, 0)
color = color_inactive
player_name = ""
done = False

#game over text
gfont = pygame.font.SysFont('freesansbold.ttf',100)

def gameXY(x,y):
    game = gfont.render('GAME OVER',True,(110,0,0))
    screen.blit(game,(x,y))

score_value = 0
sfont = pygame.font.SysFont('freesansbold.ttf',40)

def scoreXY(x,y,score_value,player_name):
    score = sfont.render('SCORE: '+str(score_value),True,(100,0,100))
    screen.blit(score,(x,y))
    playerName = sfont.render('Player: '+player_name,True,(100,0,100))
    screen.blit(playerName,(x-100,y+45))

#score save in fire base
save_name_score = False
# Firebase URL
FIREBASE_URL = "https://bambooblitz-413ec-default-rtdb.asia-southeast1.firebasedatabase.app/rivergame.json"

def save_score(player_name, score_value):
    data = {
        "name": player_name,
        "score": score_value
    }
    response = requests.post(FIREBASE_URL, data=json.dumps(data))
    if response.status_code == 200:
        print("Score saved successfully!")
    else:
        print("Error saving score:", response.text)

#get score from firebase
def get_top_scores():
    response = requests.get(FIREBASE_URL)
    if response.status_code == 200:
        data = response.json()
        # convert to list and sort by score descending
        scores = [{"name": v["name"], "score": v["score"]} for k, v in data.items()]
        top_scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:10]
        return top_scores
    else:
        print("Error fetching scores:", response.text)
        return []

def get_rank_str(index):
    if index == 0:
        return "1st"
    elif index == 1:
        return "2nd"
    elif index == 2:
        return "3rd"
    else:
        return f"{index+1}th"



gameOver = False
clock = pygame.time.Clock()
running = True
background_music_start = False
gameOver_music = False

while running:
    screen.fill((255,255,255))
    if gameStart == True and gameOver == False:
        if background_music_start==False:
            mixer.music.play(-1)
            mixer.music.set_volume(0.3)
            background_music_start = True
        river_speed +=5
    riverXY(0,0,river_speed)
    if river_speed >=300:
        river_speed = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_start.collidepoint(event.pos) and gameStart == False:
                if player_name.strip() != "":  # name input na deya porjonto game start hobe na
                    gameStart = True
                    jump_s = mixer.Sound('assets/sounds/coinS.ogg')
                    jump_s.play()
            if button_right.collidepoint(event.pos) and boat_x <= 523 and gameStart == True:
                jump_s = mixer.Sound('assets/sounds/coinS.ogg')
                jump_s.play()
                boat_xChange = 4
            if button_left.collidepoint(event.pos) and boat_x >= 121 and gameStart == True:
                jump_s = mixer.Sound('assets/sounds/coinS.ogg')
                jump_s.play()
                boat_xChange = -4
            if gameStart == False:  # only during name entry
                for k, rect in key_buttons:
                    if rect.collidepoint(event.pos):
                        if k == "DEL":  # backspace
                            player_name = player_name[:-1]
                        elif k == "ENT":  # start game
                            if player_name.strip() != "":
                                gameStart = True
                        else:  # regular letter
                            if len(player_name) < 16:
                                player_name += k

        if event.type == pygame.MOUSEBUTTONUP:
            boat_xChange = 0

    #woods floating after game start
    if gameStart == True and gameOver == False:
        wood1_y += wood_speed
        if wood1_y >= 710:
            wood1_x = 390 - random.randrange(0, 210, 30)
            wood1_y = -80-random.randrange(0, 20, 5)
            score_value +=1

        wood2_y += wood_speed
        if wood2_y >= 720:
            wood2_x = 170 + random.randrange(0, 140, 40)
            wood2_y = -80 - random.randrange(0, 20, 5)
            score_value += 1

        wood3_y += wood_speed
        if wood3_y >= 730:
            wood3_x = 390 - random.randrange(20, 220, 20)
            wood3_y = -80 - random.randrange(0, 20, 10)
            score_value += 1

        wood4_y += wood_speed
        if wood4_y >= 740:
            wood4_x = 210 + random.randrange(0, 130, 20)
            wood4_y = -80 - random.randrange(0, 20, 5)
            score_value += 1

        wood5_y += wood_speed
        if wood5_y >= 750:
            wood5_x = 250 + random.randrange(0, 80, 20)
            wood5_y = -80 - random.randrange(0, 20, 5)
            score_value += 1

        # wood speed increase with score value
        if score_value % 20 == 0 and score_value != 0:
            wood_speed = 3 + (score_value // 20) * 0.5

    woodXY(wood1_x,wood1_y,wood1)
    woodXY(wood2_x, wood2_y, wood2)
    woodXY(wood3_x, wood3_y, wood3)
    woodXY(wood4_x, wood4_y, wood2)
    woodXY(wood5_x, wood5_y, wood3)

    #boat control
    if gameOver == False:
        boat_x +=boat_xChange

    if boat_x <= 170:
        boat_x = 170
    if boat_x >= 400:
        boat_x = 400

    boatXY(boat_x,boat_y)

    #collision check amon boat and woods
    # Boat rectangle
    boat_rect = pygame.Rect(boat_x+10, boat_y+35, boat.get_width()-10, boat.get_height()-25)

    # Wood rectangles (adjusted hitboxes)
    wood1_rect = pygame.Rect(wood1_x + 4, wood1_y+5, wood1.get_width() - 10, wood1.get_height() - 7)
    wood2_rect = pygame.Rect(wood2_x, wood2_y+5, wood2.get_width() - 4, wood2.get_height() - 10)
    wood3_rect = pygame.Rect(wood3_x + 10, wood3_y + 9, wood3.get_width() - 7, wood3.get_height() - 4)
    wood4_rect = pygame.Rect(wood4_x, wood4_y+5, wood2.get_width() - 4, wood2.get_height() - 10)
    wood5_rect = pygame.Rect(wood5_x + 10, wood5_y + 9, wood3.get_width() - 7, wood3.get_height() - 4)

    if (boat_rect.colliderect(wood1_rect) or
            boat_rect.colliderect(wood2_rect) or
            boat_rect.colliderect(wood3_rect) or
            boat_rect.colliderect(wood4_rect) or
            boat_rect.colliderect(wood5_rect)):
        gameOver = True
        if gameOver_music == False:
            mixer.music.stop()
            gameover_s = mixer.Sound('assets/sounds/gmover.ogg')
            gameover_s.play()
            gameOver_music = True

    if gameOver == True:
        gameXY(100,150)
        if save_name_score == False:
            save_score(player_name,score_value)
            get_top_scores()
            save_name_score = True
        y_offset = 290
        # Draw canvas rectangle
        canvas_rect = pygame.Rect(160, y_offset-60, 300, 370)
        pygame.draw.rect(screen, (200, 200, 255), canvas_rect)
        title_font = pygame.font.SysFont('freesansbold.ttf', 50)
        title_text = title_font.render("Leaderboard", True, (50, 0, 100))
        screen.blit(title_text, (180, y_offset-40))

        score_font = pygame.font.SysFont('freesansbold.ttf', 35)
        for idx, player in enumerate(get_top_scores()):
            rank = get_rank_str(idx)
            name = player["name"]
            score = player["score"]
            text = score_font.render(f"{rank}: {name} - {score}", True, (10, 50, 10))
            screen.blit(text, (180, y_offset))
            y_offset += 30

    #draw button pad
    draw_button_pad()
    if gameStart == True:
        scoreXY(250,670,score_value,player_name)
    if gameStart == True:
        draw_buttons()
    if gameStart == False:
        draw_start_button()
        # draw input box
        pygame.draw.rect(screen, (200, 200, 200), input_box)  # fill background
        pygame.draw.rect(screen, color, input_box, 2)  # border

        if player_name == "":
            # show placeholder when box is inactive and empty
            placeholder_surface = name_font.render("Enter your name", True, (150, 150, 150))
            screen.blit(placeholder_surface, (input_box.x + 5, input_box.y + 10))
        else:
            # show actual typed name
            text_surface = name_font.render(player_name, True, (0, 0, 0))
            screen.blit(text_surface, (input_box.x + 5, input_box.y + 10))

            # draw keyboard
        for k, rect in key_buttons:
            pygame.draw.rect(screen, (180, 180, 180), rect, border_radius=8)
            key_text = font_btn.render(k, True, (0, 0, 0))
            screen.blit(key_text, (rect.x + 10, rect.y + 10))

    clock.tick(60)  # change
    pygame.display.flip()

