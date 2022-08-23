import random
import sys
import pygame
import copy
import time


pygame.mixer.init()
pygame.font.init()
suits = ["clubs", "diamonds", "hearts", "spades"]

music_on = True
sfx_on = True


class Card:
    def __init__(self, value, suit, image):
        self.value = value
        self.suit = suit
        self.image = image

    def __str__(self):
        if self.value == 11:
            return f"jack_of_{self.suit}"
        elif self.value == 12:
            return f"queen_of_{self.suit}"
        elif self.value == 13:
            return f"king_of_{self.suit}"
        elif self.value == 1:
            return f"ace_of_{self.suit}"
        else:
            return f"{self.value}_of_{self.suit}"

    def __copy__(self):
        copy_card = Card(self.value, self.suit, self.image)
        return copy_card


class Pile:
    def __init__(self):
        self.cards = []

    def __str__(self):
        card_list = []
        for card in self.cards:
            card_list.append(str(card))
        return str(card_list)

    def __copy__(self):
        copy_pile = Pile()
        for card in self.cards:
            copy_pile.cards.append(copy.copy(card))
        return copy_pile

    def draw_card(self, pile):
        try:
            pile.cards.append(self.cards[-1])
            self.cards.pop()
            if sfx_on is True:
                PLAY_CARD_SOUND.play()
        except IndexError:
            if sfx_on is True:
                INVALID_SOUND.play()

    def draw_all_cards(self, pile):
        if len(self.cards) > 1:
            if sfx_on is True:
                SHUFFLE_CARD_SOUND.play()
        else:
            if sfx_on is True:
                PLAY_CARD_SOUND.play()
        for card in self.cards:
            pile.cards.append(card)
        self.cards = []

    def getimage(self, index):  # function to get image of any card
        searched_card = self.cards[index]
        return searched_card.image


class Deck(Pile):
    def create(self):
        for s in suits:
            for v in range(1, 14):
                card = Card(v, s, image=None)
                card_image = pygame.image.load(f"Assets/{str(card)}.png")
                card = Card(v, s, card_image)
                self.cards.append(card)

    def create_small(self):
        for s in suits:
            for v in range(1, 14):
                if v == 1 or v >= 6:
                    card = Card(v, s, image=None)
                    card_image = pygame.image.load(f"Assets/{str(card)}.png")
                    card = Card(v, s, card_image)
                    self.cards.append(card)

    def shuffle(self):
        random.shuffle(self.cards)


class Environment:
    def __init__(self):
        self.spots = []

    def __str__(self):
        str_list = []
        for spot in self.spots:
            str_list.append(str(spot))
        return str(str_list)

    def __copy__(self):
        copy_environment = Environment()
        for spot in self.spots:
            copy_environment.spots.append(copy.copy(spot))
        return copy_environment

    def add(self):
        x = 10 + (len(self.spots)) * (WIDTH_CARD + 10)
        spot = Spot(x)
        self.spots.append(spot)

    def get_spot_pile(self, index):
        try:
            searched_spot = self.spots[index]
            return searched_spot.pile
        except IndexError:
            pass

    def remove(self):
        for spot in self.spots:
            if not spot.pile.cards:
                self.spots.remove(spot)

    def check_if_movable(self, selection_index):
        try:
            if selection_index == 0:
                return False
            elif self.get_spot_pile(selection_index - 1).cards[-1].suit \
                    == self.get_spot_pile(selection_index + 1).cards[-1].suit:
                return True
            elif self.get_spot_pile(selection_index - 1).cards[-1].value \
                    == self.get_spot_pile(selection_index + 1).cards[-1].value:
                return True
            else:
                return False
        except IndexError:
            pass
        except AttributeError:
            pass


class Spot:
    def __init__(self, x):
        self.position_x = x
        self.position_y = (HEIGHT-HEIGHT_CARD)//2
        self.pile = Pile()

    def __str__(self):
        return str(self.pile)

    def __copy__(self):
        copy_spot = Spot(self.position_x)
        copy_spot.pile = copy.copy(self.pile)
        return copy_spot


class Button:
    def __init__(self, b_x, b_y, b_img, hover_img, b_name):
        self.name = b_name
        self.coordinate_x = b_x
        self.coordinate_y = b_y
        self.image = b_img
        self.hover = hover_img
        self.rect = pygame.Rect(self.coordinate_x, self.coordinate_y, self.image.get_width(), self.image.get_height())
        self.clicked = False
        self.hovering = False

    def __str__(self):
        return self.name

    def draw(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            WIN.blit(self.hover, (self.coordinate_x, self.coordinate_y))
            self.hovering = True
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:
                self.clicked = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        else:
            WIN.blit(self.image, (self.coordinate_x, self.coordinate_y))
            self.hovering = False


class ToggleButton:
    def __init__(self, b_x, b_y, true_image, true_hover, false_image, false_hover):
        self.coordinates = (b_x, b_y)
        self.true_image = true_image
        self.true_hover = true_hover
        self.false_image = false_image
        self.false_hover = false_hover
        self.rect = pygame.Rect(b_x, b_y, true_image.get_width(), true_image.get_height())
        self.clicked = False
        self.hovering = False
        self.state = True

    def draw(self):
        pos = pygame.mouse.get_pos()
        if self.state is True:
            if self.rect.collidepoint(pos):
                self.hovering = True
                WIN.blit(self.true_hover, self.coordinates)
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:
                    self.state = not self.state
                    self.clicked = True
            else:
                WIN.blit(self.true_image, self.coordinates)
                self.hovering = False
        else:
            if self.rect.collidepoint(pos):
                self.hovering = True
                WIN.blit(self.false_hover, self.coordinates)
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:
                    self.state = not self.state
                    self.clicked = True
            else:
                WIN.blit(self.false_image, self.coordinates)
                self.hovering = False
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False


BUTTON_NAMES = ["medium", "hard", "exit"]
buttons = []
button_x = 50
for name in BUTTON_NAMES:
    button_image = pygame.image.load(f"Assets/button_{name}.png")
    hover_image = pygame.image.load(f"Assets/button_hover_{name}.png")
    button_y = 310
    button = Button(button_x, button_y, button_image, hover_image, name)
    buttons.append(button)
    button_x += 50 + button_image.get_width()


WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("EGO GAME")

UNDO_BUTTON_NAME = "undo_button"
UNDO_BUTTON_IMG = pygame.image.load(f"Assets/{UNDO_BUTTON_NAME}.png.")
UNDO_BUTTON_X = WIDTH - UNDO_BUTTON_IMG.get_width()
UNDO_BUTTON_Y = 0
UNDO_BUTTON_HOVER = pygame.image.load(f"Assets/{UNDO_BUTTON_NAME}_hover.png.")
undo_button = Button(UNDO_BUTTON_X, UNDO_BUTTON_Y, UNDO_BUTTON_IMG, UNDO_BUTTON_HOVER, UNDO_BUTTON_NAME)

WIDTH_CARD, HEIGHT_CARD = 57, 89

GREEN = (34, 177, 76)
DARK_GREEN = (49, 135, 70)
WHITE = (255, 255, 255)
DARKER_GREEN = (31, 109, 51)

GAME_OVER = pygame.USEREVENT + 1
WINNER = pygame.USEREVENT + 2

SHUFFLE_CARD_SOUND = pygame.mixer.Sound("Assets/shuffle_card.mp3")
PLAY_CARD_SOUND = pygame.mixer.Sound("Assets/place_card.mp3")
INVALID_SOUND = pygame.mixer.Sound("Assets/invalid.mp3")
WIN_SOUND = pygame.mixer.Sound("Assets/win_sound.mp3")
UNDO_SOUND = pygame.mixer.Sound("Assets/undo.mp3")
BACKGROUND_MUSIC = pygame.mixer.Sound("Assets/background_music.mp3")

TITLE = pygame.image.load("Assets/egogame_title.png")

FONT = pygame.font.Font("Assets/Minecraftia-Regular.ttf", 20)

card_selection = pygame.image.load("Assets/card_selection.png")

card_button_img = pygame.image.load("Assets/invisible_card.png")
draw_card_button = Button(
    (WIDTH - card_button_img.get_width())//2, 100, card_button_img, card_selection, "invisible_button")

ALERT_IMG = pygame.image.load("Assets/alert.png.")
ALERT_LEFT_IMG = pygame.image.load("Assets/alert_left.png")

RIGHT_BUTTON_IMG = pygame.image.load("Assets/right_button.png")
RIGHT_BUTTON_HOVER = pygame.image.load("Assets/right_button_hover.png")
LEFT_BUTTON_IMG = pygame.image.load("Assets/left_button.png")
LEFT_BUTTON_HOVER = pygame.image.load("Assets/left_button_hover.png")

right_button = Button(WIDTH - RIGHT_BUTTON_IMG.get_width() - 10, (HEIGHT - RIGHT_BUTTON_IMG.get_height())//2,
                      RIGHT_BUTTON_IMG, RIGHT_BUTTON_HOVER, "right_button")
left_button = Button(10, (HEIGHT - LEFT_BUTTON_IMG.get_height())//2, LEFT_BUTTON_IMG, LEFT_BUTTON_HOVER, "left_button")

CLUE_IMAGE = pygame.image.load("Assets/clue.png")
CLUE_HOVER = pygame.image.load("Assets/clue_hover.png")
clue_button = Button(WIDTH*2//3 - CLUE_IMAGE.get_width()//2, 0, CLUE_IMAGE, CLUE_HOVER, "clue_button")

HELP_IMAGE = pygame.image.load("Assets/help.png")
HELP_HOVER = pygame.image.load("Assets/help_hover.png")
help_button = Button(WIDTH//3 - HELP_IMAGE.get_width()//2, 0, HELP_IMAGE, HELP_HOVER, "clue_button")

HELP_SCREEN = pygame.image.load("Assets/help_screen.png")

SETTINGS_IMG = pygame.image.load("Assets/settings_button.png")
SETTINGS_HOVER = pygame.image.load("Assets/settings_button_hover.png")
settings_button = Button(0, 0, SETTINGS_IMG, SETTINGS_HOVER, "settings_button")


def draw_window(environment, selection, general_x, t, deck, selection_index):
    WIN.fill(GREEN)
    for spots in environment.spots:
        spot_rect = pygame.Rect(spots.position_x + general_x, spots.position_y, WIDTH_CARD, HEIGHT_CARD)
        pygame.draw.rect(WIN, GREEN, spot_rect)
        y = 0
        for card in spots.pile.cards:
            WIN.blit(card.image, (spots.position_x + general_x, spots.position_y + y))
            y += 5
    try:
        if len(environment.spots) > 0:
            WIN.blit(card_selection, (selection.x - 2 + general_x,
                                      selection.y - 2 + ((len(environment.spots[selection_index].pile.cards) - 1) * 5)))
    except IndexError:
        pass
    if selection.x - 2 + general_x > WIDTH:
        WIN.blit(ALERT_IMG, (WIDTH - ALERT_IMG.get_width(), 100))
    if selection.x - 2 + general_x < 0:
        WIN.blit(ALERT_LEFT_IMG, (10, 100))
    if len(deck.cards) > 0:
        pile = pygame.image.load(f"Assets/card_pile_{len(deck.cards)}.png.")
        WIN.blit(pile, ((WIDTH - WIDTH_CARD) // 2, HEIGHT - 10 - pile.get_height()))
        global draw_card_button
        draw_card_button = Button(
            (WIDTH - card_button_img.get_width())//2, HEIGHT - pile.get_height()-12, card_button_img,
            card_selection, "invisible_button")
        draw_card_button.draw()
    try:
        if environment.spots[-1].position_x + general_x + WIDTH_CARD > WIDTH:
            right_button.draw()
    except IndexError:
        pass
    if general_x < 0:
        left_button.draw()
    help_button.draw()
    clue_button.draw()
    settings_button.draw()
    t = FONT.render("Time: " + str(t) + " seconds", True, WHITE)
    WIN.blit(t, (WIDTH - t.get_width(), HEIGHT - t.get_height()))
    cards_left = FONT.render("Cards left: " + str(len(deck.cards)), True, WHITE)
    WIN.blit(cards_left, (0, HEIGHT - t.get_height()))
    undo_button.draw()


def falling(a, t, v, s0):
    y = (a/2 * t * t + v*t + s0)//1
    return y


def card_fall_frame(card_list, a, t, v, s0,):
    card_list[2] = falling(a, t, v, s0)


def draw_loose_animation(environment, general_x):
    all_cards = []
    falling_timer = Stopwatch()
    display_animation = True
    acceleration = 2000
    start_time = 0
    for spots in environment.spots:
        y = 0
        spots.pile.cards.reverse()
        for card in spots.pile.cards:
            card_list = [card.image, spots.position_x + general_x, spots.position_y + y]
            all_cards.append(card_list)
            y += 5
    while display_animation:
        try:
            for card in all_cards:
                start_position = copy.copy(card[2])
                start_position2 = copy.copy(all_cards[all_cards.index(card) + 1][2])
                falling_timer.start()
                start = True
                while card[2] < HEIGHT:
                    if card[2] < HEIGHT * 3 / 4:
                        card_fall_frame(card, acceleration, falling_timer.real_measure(),
                                        acceleration * falling_timer.real_measure(), start_position)
                    else:
                        if start is True:
                            start_time = copy.copy(falling_timer.real_measure())
                            start = False
                        card_fall_frame(card, acceleration, falling_timer.real_measure(),
                                        acceleration * falling_timer.real_measure(), start_position)
                        card_fall_frame(all_cards[all_cards.index(card) + 1], acceleration,
                                        falling_timer.real_measure() - start_time,
                                        0, start_position2)
                    WIN.fill(GREEN)
                    for c in all_cards:
                        WIN.blit(c[0], (c[1], c[2]))
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                break
                    pygame.display.update()
        except IndexError:
            display_animation = False


def jumping_card(graph_x):
    if graph_x >= 420:
        graph_y = (graph_x-560)*(graph_x-560)//100
    elif graph_x >= 140:
        graph_y = (graph_x-280)*(graph_x-280)//100
    else:
        graph_y = graph_x * graph_x//100
    return graph_y


def draw_win_animation(environment, general_x):
    all_cards = []
    display_animation = True
    WIN.fill(GREEN)
    text = FONT.render("Click the mouse button to skip.", True, WHITE)
    WIN.blit(text, ((WIDTH - text.get_width())//2, HEIGHT//4))
    for spots in environment.spots:
        y = 0
        spots.pile.cards.reverse()
        for card in spots.pile.cards:
            card_list = [card.image, spots.position_x + general_x, spots.position_y + y]
            print(spots.position_y)
            all_cards.append(card_list)
            y += 5

    for c in all_cards:
        WIN.blit(c[0], (c[1], c[2]))
    pygame.display.update()
    all_cards.reverse()
    for card in all_cards:
        start_y = card[2]
        start_x = copy.copy(card[1])
        graph_x = 0
        if display_animation is True:
            while card[1] <= 900 and start_y + jumping_card(graph_x) < WIDTH:
                card[2] = start_y + jumping_card(graph_x)
                WIN.blit(card[0], (start_x + graph_x, card[2]))
                graph_x += 5
                card[1] = start_x + graph_x
                pygame.time.delay(25)
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            display_animation = False
                            break


def draw_help():
    pygame.image.save(WIN, "Assets/screenshot.jpg")
    background = pygame.image.load("Assets/screenshot.jpg")
    display_help = True
    help_index = 0
    animation_index = 0
    img = []
    text = []
    text1 = []
    while display_help:
        WIN.blit(background, (0, 0))
        WIN.blit(HELP_SCREEN, (0, 0))
        title = FONT.render("Rules and Controls", True, WHITE)
        WIN.blit(title, (((WIDTH - title.get_width())//2), 10))
        if help_index == -1:
            display_help = False
        if help_index == 0:
            img = pygame.image.load("Assets/help1.png")
            text = FONT.render("Tap the pile to draw cards.", True, WHITE)
            text1 = FONT.render("", True, WHITE)
            left_button.draw()
            right_button.draw()
        if help_index == 1:
            animation_list = [pygame.image.load("Assets/help2_1.png"), pygame.image.load("Assets/help2_2.png"),
                              pygame.image.load("Assets/help2_3.png")]
            img = animation_list[animation_index]
            text = FONT.render("Use the a and d key to move your selection.", True, WHITE)
            text1 = FONT.render("", True, WHITE)
            left_button.draw()
            right_button.draw()
            animation_index += 1
            pygame.time.delay(500)
            if animation_index == 3:
                animation_index = 0
        if help_index == 2:
            img = pygame.image.load("Assets/help3_1.png")
            text = FONT.render("If two cards have the same value or suit,", True, WHITE)
            text1 = FONT.render("the card between them can be moved to the left.", True, WHITE)
            left_button.draw()
            right_button.draw()
        if help_index == 3:
            img = pygame.image.load("Assets/help3.png")
            text = FONT.render("Click anywhere on the screen to move the card", True, WHITE)
            text1 = FONT.render("", True, WHITE)
            left_button.draw()
            right_button.draw()
        if help_index == 4:
            img = pygame.image.load("Assets/help4.png")
            text = FONT.render("If you're stuck, click the lightbulb.", True, WHITE)
            text1 = FONT.render("It will select a movable card or draw a new one.", True, WHITE)
            left_button.draw()
            right_button.draw()
        if help_index == 5:
            img = pygame.image.load("Assets/help5.png")
            text = FONT.render("Click the undo button to undo your last move.", True, WHITE)
            text1 = FONT.render("", True, WHITE)
            left_button.draw()
            right_button.draw()
        if help_index == 6:
            img = pygame.image.load("Assets/help6.png")
            text = FONT.render("Use the arrows to navigate the environment", True, WHITE)
            text1 = FONT.render("", True, WHITE)
            left_button.draw()
            right_button.draw()
        if help_index == 7:
            img = pygame.image.load("Assets/help7.png")
            text = FONT.render("Your final goal is to have two piles left.", True, WHITE)
            text1 = FONT.render("Have fun!", True, WHITE)
            left_button.draw()
            right_button.draw()
        if help_index == 8:
            display_help = False
        WIN.blit(img, (((WIDTH - img.get_width())//2), 10 + title.get_height()))
        WIN.blit(text, (((WIDTH - text.get_width())//2), 20 + title.get_height() + img.get_height()))
        WIN.blit(
            text1, (((WIDTH - text1.get_width()) // 2), 30 + title.get_height() + img.get_height() + text.get_height()))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if right_button.hovering is True:
                        help_index += 1
                    if left_button.hovering is True:
                        help_index -= 1
        pygame.display.update()


B2G_IMG = pygame.image.load("Assets/button_backtogame.png.")
B2G_HOVER = pygame.image.load("Assets/button_hover_backtogame.png.")
b2g_button = Button((WIDTH - B2G_IMG.get_width())//2, 50, B2G_IMG, B2G_HOVER, "b2g_button")

RETRY_IMG = pygame.image.load("Assets/button_retry.png.")
RETRY_HOVER = pygame.image.load("Assets/button_hover_retry.png.")
retry_button = Button(
    (WIDTH - RETRY_IMG.get_width())//2, 60 + B2G_IMG.get_height(), RETRY_IMG, RETRY_HOVER, "retry button")

MUSICON_IMG = pygame.image.load("Assets/button_musicon.png")
MUSICON_HOVER = pygame.image.load("Assets/button_hover_musicon.png")
MUSICOFF_IMG = pygame.image.load("Assets/button_musicoff.png")
MUSICOFF_HOVER = pygame.image.load("Assets/button_hover_musicoff.png")
music_button = ToggleButton((WIDTH - MUSICOFF_IMG.get_width())//2,
                            70 + 2*B2G_IMG.get_height(), MUSICON_IMG, MUSICON_HOVER, MUSICOFF_IMG, MUSICOFF_HOVER)

SFXON_IMG = pygame.image.load("Assets/button_sfxon.png")
SFXON_HOVER = pygame.image.load("Assets/button_hover_sfxon.png")
SFXOFF_IMG = pygame.image.load("Assets/button_sfxoff.png")
SFXOFF_HOVER = pygame.image.load("Assets/button_hover_sfxoff.png")
sfx_button = ToggleButton(
    (WIDTH - SFXOFF_IMG.get_width())//2, 80 + 3*B2G_IMG.get_height(), SFXON_IMG, SFXON_HOVER, SFXOFF_IMG, SFXOFF_HOVER)

EXIT_IMG = pygame.image.load("Assets/button_exit2.png")
EXIT_HOVER = pygame.image.load("Assets/button_hover_exit2.png")
exit_button = Button(
    (WIDTH - EXIT_IMG.get_width())//2, 90 + 4*B2G_IMG.get_height(), EXIT_IMG, EXIT_HOVER, "exit_button2")


def draw_settings():
    global sfx_on
    global music_on
    pygame.image.save(WIN, "Assets/screenshot.jpg")
    background = pygame.image.load("Assets/screenshot.jpg")
    display_settings = True
    while display_settings:
        WIN.blit(background, (0, 0))
        WIN.blit(HELP_SCREEN, (0, 0))
        title = FONT.render("GAME PAUSED", True, WHITE)
        WIN.blit(title, (((WIDTH - title.get_width()) // 2), 10))
        b2g_button.draw()
        retry_button.draw()
        if sfx_on is False:
            sfx_button.state = False
        else:
            sfx_button.state = True
        if music_on is False:
            music_button.state = False
        else:
            music_button.state = True
        music_button.draw()
        sfx_button.draw()
        exit_button.draw()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if b2g_button.hovering is True:
                        display_settings = False
                    if retry_button.hovering is True:
                        return True
                    if exit_button.hovering is True:
                        BACKGROUND_MUSIC.stop()
                        main()
        if music_button.clicked is True:
            if music_button.state is False:
                music_on = False
                BACKGROUND_MUSIC.stop()
            else:
                BACKGROUND_MUSIC.stop()
                music_on = True
                BACKGROUND_MUSIC.play(loops=-1)
        if sfx_button.clicked is True:
            if sfx_button.state is True:
                sfx_on = True
            else:
                sfx_on = False

        pygame.display.update()


help_button_title = copy.copy(help_button)
help_button_title.coordinate_x = WIDTH - help_button_title.image.get_width()
help_button_title.coordinate_y = 0
help_button_title.rect = pygame.Rect(help_button_title.coordinate_x, help_button_title.coordinate_y,
                                     help_button_title.image.get_width(), help_button_title.image.get_height())

SFX_ON = pygame.image.load("Assets/sfx_on.png")
SFX_ON_HOVER = pygame.image.load("Assets/sfx_on_hover.png")
SFX_OFF = pygame.image.load("Assets/sfx_off.png")
SFX_OFF_HOVER = pygame.image.load("Assets/sfx_off_hover.png")
sfx_title_button = ToggleButton(
    WIDTH - SFX_ON.get_width() - HELP_IMAGE.get_width(), 0, SFX_ON, SFX_ON_HOVER, SFX_OFF, SFX_OFF_HOVER)

MUSIC_ON = pygame.image.load("Assets/music_on.png")
MUSIC_ON_HOVER = pygame.image.load("Assets/music_on_hover.png")
MUSIC_OFF = pygame.image.load("Assets/music_off.png")
MUSIC_OFF_HOVER = pygame.image.load("Assets/music_off.png")
music_title_button = ToggleButton(
    WIDTH - HELP_IMAGE.get_width() - 2*MUSIC_ON.get_width(), 0, MUSIC_ON, MUSIC_ON_HOVER, MUSIC_OFF, MUSIC_OFF_HOVER)


def draw_titlecard():
    WIN.fill(DARKER_GREEN)
    WIN.blit(TITLE, (WIDTH//2-TITLE.get_width()//2, 50))
    for b in buttons:
        b.draw()
    help_button_title.draw()
    music_title_button.draw()
    sfx_title_button.draw()
    if sfx_on is False:
        sfx_title_button.state = False
    else:
        sfx_title_button.state = True
    if music_on is False:
        music_title_button.state = False
    else:
        music_title_button.state = True


def check_win(deck, environment):
    keep_playing = False
    if len(deck.cards) == 0:
        if len(environment.spots) == 2:
            pygame.event.post(pygame.event.Event(WINNER))
        elif len(environment.spots) > 2:
            for index in range(0, len(environment.spots)):
                if environment.check_if_movable(index) is True:
                    return True
            if keep_playing is False:
                pygame.event.post(pygame.event.Event(GAME_OVER))


end_button_retry = copy.copy(retry_button)
end_button_retry.coordinate_x = (WIDTH - end_button_retry.image.get_width())//2
end_button_retry.coordinate_y = 200
end_button_retry.rect = pygame.Rect(end_button_retry.coordinate_x, end_button_retry.coordinate_y,
                                    end_button_retry.image.get_width(), end_button_retry.image.get_height())
end_button_exit = copy.copy(exit_button)
end_button_exit.coordinate_x = (WIDTH - end_button_exit.image.get_width())//2
end_button_exit.coordinate_y = 300
end_button_exit.rect = pygame.Rect(end_button_exit.coordinate_x, end_button_exit.coordinate_y,
                                   end_button_exit.image.get_width(), end_button_exit.image.get_height())


def draw_winner(t, environment, general_x):
    draw_win_animation(environment, general_x)
    if music_on is True:
        WIN_SOUND.play()
    display_win = True
    while display_win:
        WIN.fill(DARK_GREEN)
        win = FONT.render("You win!!", True, WHITE)
        WIN.blit(win, (WIDTH // 2 - win.get_width() // 2, 100))
        draw_time = FONT.render("Time: " + str(t) + " seconds", True, WHITE)
        WIN.blit(draw_time, (WIDTH // 2 - draw_time.get_width() // 2, 150))
        end_button_exit.draw()
        end_button_retry.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if end_button_exit.hovering is True:
                        display_win = False
                    if end_button_retry.hovering is True:
                        return True

        pygame.display.update()


def draw_game_over(environment, general_x):
    draw_loose_animation(environment, general_x)
    display_loose = True
    while display_loose:
        WIN.fill(DARK_GREEN)
        draw_text = FONT.render("Game over!", True, WHITE)
        WIN.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2, HEIGHT//3))
        end_button_exit.draw()
        end_button_retry.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if end_button_exit.hovering is True:
                        return False
                    if end_button_retry.hovering is True:
                        return True
        pygame.display.update()


def save_state(environment, environment_state, deck, deck_state):
    environment_state.append(copy.copy(environment))
    deck_state.append(copy.copy(deck))


def undo(environment_state, deck_state):
    environment_state.pop()
    deck_state.pop()


def game(difficulty):
    game_clock.start()
    environment_state = []
    deck_state = []
    environment = Environment()
    deck = Deck()
    if difficulty == "medium":
        deck.create_small()
    else:

        deck.create()
    deck.shuffle()
    original_deck = copy.copy(deck)
    clock = pygame.time.Clock()
    selection = pygame.Rect(10, (HEIGHT - HEIGHT_CARD) // 2, WIDTH_CARD, HEIGHT_CARD)
    selection_index = 0
    general_x = 0
    play_game = True
    save_state(environment, environment_state, deck, deck_state)
    while play_game:
        clock.tick(60)
        environment = environment_state[-1]
        deck = deck_state[-1]
        draw_window(environment, selection, general_x, game_clock.measure(), deck, selection_index)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == WINNER:
                if draw_winner(game_clock.measure(), environment, general_x) is True:
                    deck = original_deck
                    deck_state.clear()
                    environment.spots.clear()
                    environment_state.clear()
                    save_state(environment, environment_state, deck, deck_state)
                    game_clock.start()
                else:
                    BACKGROUND_MUSIC.stop()
                    main()
            if event.type == GAME_OVER:
                if draw_game_over(environment, general_x) is True:
                    deck = original_deck
                    deck_state.clear()
                    environment.spots.clear()
                    environment_state.clear()
                    save_state(environment, environment_state, deck, deck_state)
                    game_clock.start()
                else:
                    BACKGROUND_MUSIC.stop()
                    main()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print("click")
                    if left_button.hovering is True and general_x < 0:
                        general_x += (10 + WIDTH_CARD)
                        selection.x -= (WIDTH_CARD + 10)
                        selection_index -= 1
                    elif draw_card_button.hovering is True:
                        environment.add()
                        deck.draw_card(environment.get_spot_pile(-1))
                        save_state(environment, environment_state, deck, deck_state)
                    elif undo_button.hovering is True and len(environment_state) > 1:
                        environment_state.pop()
                        deck_state.pop()
                        if sfx_on is True:
                            UNDO_SOUND.play()
                    elif right_button.hovering is True:
                        if environment.spots[-1].position_x + general_x + WIDTH_CARD > WIDTH:
                            general_x -= (10 + WIDTH_CARD)
                            if selection.x < WIDTH:
                                selection.x += (WIDTH_CARD + 10)
                                selection_index += 1

                    elif clue_button.hovering is True:
                        possible_move = False
                        for spot in environment.spots:
                            if environment.check_if_movable(environment.spots.index(spot)) is True:
                                selection.x += (10 + WIDTH_CARD) * (environment.spots.index(spot) - selection_index)
                                selection_index = environment.spots.index(spot)
                                possible_move = True
                                break
                        if possible_move is not True:
                            environment.add()
                            deck.draw_card(environment.get_spot_pile(-1))
                            save_state(environment, environment_state, deck, deck_state)
                    elif help_button.hovering is True:
                        pause = game_clock.pause()
                        draw_help()
                        game_clock.unpause(pause)
                    elif settings_button.hovering is True:
                        pause = game_clock.pause()
                        if draw_settings() is True:
                            deck = original_deck
                            deck_state.clear()
                            environment.spots.clear()
                            environment_state.clear()
                            save_state(environment, environment_state, deck, deck_state)
                        game_clock.unpause(pause)
                    else:
                        if environment.check_if_movable(selection_index) is True and selection_index != 0:
                            for q in range(selection_index, len(environment.spots)):
                                pile = environment.get_spot_pile(q)
                                pile.draw_all_cards(environment.get_spot_pile(q - 1))
                            environment.remove()
                            save_state(environment, environment_state, deck, deck_state)
                            selection_index -= 1
                            selection.x -= (WIDTH_CARD + 10)
                            if environment.spots[-1].position_x + general_x + WIDTH_CARD < WIDTH and general_x < 0:
                                general_x += (10 + WIDTH_CARD)
                        else:
                            if sfx_on is True:
                                INVALID_SOUND.play()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and selection_index > 0:
                    selection.x -= (WIDTH_CARD + 10)
                    selection_index -= 1
                if event.key == pygame.K_d and selection_index < len(environment.spots)-1:
                    selection.x += (WIDTH_CARD + 10)
                    selection_index += 1
                if event.key == pygame.K_RETURN:
                    for q in range(selection_index, len(environment.spots)):
                        pile = environment.get_spot_pile(q)
                        pile.draw_all_cards(environment.get_spot_pile(q - 1))
                    environment.remove()
                    save_state(environment, environment_state, deck, deck_state)
                    selection_index -= 1
                    selection.x -= (WIDTH_CARD + 10)
                    if environment.spots[-1].position_x + general_x + WIDTH_CARD < WIDTH and general_x < 0:
                        general_x += (10 + WIDTH_CARD)
                if event.key == pygame.K_SPACE:
                    draw_win_animation(environment, general_x)

        check_win(deck, environment)

        pygame.display.update()
    main()


class Stopwatch:
    def __init__(self):
        self.real_time = 0
        self.time = self.real_time//1
        self.start_time = None
        self.paused_time = 0

    def start(self):
        self.start_time = time.time()
        self.real_time = 0
        self.paused_time = 0

    def measure(self):
        self.real_time = (time.time() - self.start_time - self.paused_time)
        self.time = int(self.real_time)
        return self.time

    def real_measure(self):
        self.real_time = time.time() - self.start_time - self.paused_time
        return self.real_time

    def pause(self):
        begin_pause_time = time.time()
        return begin_pause_time

    def unpause(self, begin_paused_time):
        self.paused_time += time.time() - begin_paused_time


game_clock = Stopwatch()


def main():
    global sfx_on
    global music_on
    run = True
    if music_on is True:
        BACKGROUND_MUSIC.play(loops=-1)
    while run:
        buttons[0].clicked = False
        buttons[1].clicked = False
        draw_titlecard()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if help_button_title.hovering is True:
                        draw_help()
                    if sfx_title_button.hovering is True:
                        sfx_on = not sfx_on
                    if music_title_button.hovering is True:
                        music_on = not music_on
                        if music_on is True:
                            BACKGROUND_MUSIC.play(loops=-1)
                        else:
                            BACKGROUND_MUSIC.stop()
        if buttons[0].clicked is True:
            game("medium")
        if buttons[1].clicked is True:
            game("hard")
        if buttons[2].clicked is True:
            pygame.quit()
            sys.exit()
        pygame.display.update()

    main()


if __name__ == "__main__":
    main()
