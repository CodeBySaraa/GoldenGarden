import pygame
import sys
import json
import random
import os

pygame.init()
pygame.mixer.init()

#File creater (adapter for any OS)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# Window setup
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Golden Garden")
clock = pygame.time.Clock()
running = True
font = pygame.font.SysFont(None, 40)
button_font = pygame.font.SysFont(None, 50)
# Create a smaller font specifically for the inventory slot numbers
slot_font = pygame.font.SysFont(None, 28)
#Menu buttons
start_button = pygame.Rect(350, 260, 300, 70)
continue_button = pygame.Rect(350, 360, 300, 70)
exit_button = pygame.Rect(350, 460, 300, 70)

#PNG randomisation of garden layout
 # os.path.join(ASSETS_DIR, "tiles", "water", "w1.png")
grass_tiles = [
    pygame.image.load(os.path.join(ASSETS_DIR, "tiles", "grass_normal", "gt1.png")),
    pygame.image.load(os.path.join(ASSETS_DIR, "tiles", "grass_normal", "gt2.png")),
    pygame.image.load(os.path.join(ASSETS_DIR, "tiles", "grass_normal", "gt3.png")),
    pygame.image.load(os.path.join(ASSETS_DIR, "tiles", "grass_normal", "gt4.png"))
]

#PNG animation for water layout
water_frames = [
    pygame.image.load(os.path.join(ASSETS_DIR, "tiles", "water", "w1.png")),
    pygame.image.load(os.path.join(ASSETS_DIR, "tiles", "water", "w2.png")),
    pygame.image.load(os.path.join(ASSETS_DIR, "tiles", "water", "w3.png"))
]
water_frame_index = 0
last_water_update = 0
water_animation_speed = 500

#PNG randomisation of background layout
background_tiles = [
    pygame.image.load(os.path.join(ASSETS_DIR, "tiles", "background", "bg1.png")),
    pygame.image.load(os.path.join(ASSETS_DIR, "tiles", "background", "bg2.png")),
    pygame.image.load(os.path.join(ASSETS_DIR, "tiles", "background", "bg3.png"))
]

#PNG randomisation for boosted tile layout
boosted_tiles = [
    pygame.image.load(os.path.join(ASSETS_DIR, "tiles", "grass_boosted", "gb1.png")),
    pygame.image.load(os.path.join(ASSETS_DIR, "tiles", "grass_boosted", "gb2.png"))
]

#PNG plants
plant_images = {

    "Daisy": {
        "slot": pygame.image.load(
            os.path.join(ASSETS_DIR, "plants", "daisy", "daisy_slotview", "daisy_slotview.png")
        ).convert_alpha(),
        1: [
            pygame.image.load(
               os.path.join(ASSETS_DIR, "plants", "daisy", "daisy_stage1", "daisy-1-1.png")
            ).convert_alpha(),
            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "daisy", "daisy_stage1", "daisy-1-2.png")
            ).convert_alpha()
        ],
        2: [
            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "daisy", "daisy_stage2", "daisy-2-1.png")
            ).convert_alpha(),
            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "daisy", "daisy_stage2", "daisy-2-2.png")
            ).convert_alpha()
        ],
        3: [
            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "daisy", "daisy_stage3", "daisy-3-1.png")
            ).convert_alpha(),
            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "daisy", "daisy_stage3", "daisy-3-2.png")
            ).convert_alpha()
        ]
    },
    "Tulip": {
        "slot": pygame.image.load(
            os.path.join(ASSETS_DIR, "plants", "tulip", "tulip_slotview", "tulip_slotview.png")
        ).convert_alpha(),

        1: [
            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "tulip", "tulip_stage1", "tulip-1-1.png")
            ).convert_alpha(),

            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "tulip", "tulip_stage1", "tulip-1-2.png")
            ).convert_alpha()
        ],

        2: [
            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "tulip", "tulip_stage2", "tulip-2-1.png")
            ).convert_alpha(),

            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "tulip", "tulip_stage2", "tulip-2-2.png")
            ).convert_alpha()
        ],

        3: [
            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "tulip", "tulip_stage3", "tulip-3-1.png")
            ).convert_alpha(),

            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "tulip", "tulip_stage3", "tulip-3-2.png")
            ).convert_alpha()
        ]
    },
    "Sunflower": {
        "slot": pygame.image.load(
            os.path.join(ASSETS_DIR, "plants", "sunflower", "sunflower_slotview", "sunflower_slotview.png")
        ).convert_alpha(),

        1: [
            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "sunflower", "sunflower_stage1", "sunflower-1-1.png")
            ).convert_alpha(),

            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "sunflower", "sunflower_stage1", "sunflower-1-2.png")
            ).convert_alpha()
        ],

        2: [
            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "sunflower", "sunflower_stage2", "sunflower-2-1.png")
            ).convert_alpha(),

            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "sunflower", "sunflower_stage2", "sunflower-2-2.png")
            ).convert_alpha()
        ],

        3: [
            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "sunflower", "sunflower_stage3", "sunflower-3-1.png")
            ).convert_alpha(),

            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "sunflower", "sunflower_stage3", "sunflower-3-2.png")
            ).convert_alpha()
        ]
    },
    "Rose": {
        "slot": pygame.image.load(
            os.path.join(ASSETS_DIR, "plants", "rose", "rose_slotview", "rose_slotview.png")
        ).convert_alpha(),

        1: [
            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "rose", "rose_stage1", "rose-1-1.png")
            ).convert_alpha(),

            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "rose", "rose_stage1", "rose-1-2.png")
            ).convert_alpha()
        ],

        2: [
            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "rose", "rose_stage2", "rose-2-1.png")
            ).convert_alpha(),

            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "rose", "rose_stage2", "rose-2-2.png")
            ).convert_alpha()
        ],

        3: [
            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "rose", "rose_stage3", "rose-3-1.png")
            ).convert_alpha(),

            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "rose", "rose_stage3", "rose-3-2.png")
            ).convert_alpha()
        ]
    },
    "Lavender": {
        "slot": pygame.image.load(
            os.path.join(ASSETS_DIR, "plants", "lavender", "lavender_slotview", "lavender_slotview.png")
        ).convert_alpha(),

        1: [
            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "lavender", "lavender_stage1", "lavender-1-1.png")
            ).convert_alpha(),

            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "lavender", "lavender_stage1", "lavender-1-2.png")
            ).convert_alpha()
        ],

        2: [
            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "lavender", "lavender_stage2", "lavender-2-1.png")
            ).convert_alpha(),

            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "lavender", "lavender_stage2", "lavender-2-2.png")
            ).convert_alpha()
        ],

        3: [
            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "lavender", "lavender_stage3", "lavender-3-1.png")
            ).convert_alpha(),

            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "lavender", "lavender_stage3", "lavender-3-2.png")
            ).convert_alpha()
        ]
    },
    "Blue Orchid": {
        "slot": pygame.image.load(
            os.path.join(ASSETS_DIR, "plants", "blueorchid", "blueorchid_slotview", "blueorchid_slotview.png")
        ).convert_alpha(),

        1: [
            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "blueorchid", "blueorchid_stage1", "blueorchid-1-1.png")
            ).convert_alpha(),

            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "blueorchid", "blueorchid_stage1", "blueorchid-1-2.png")
            ).convert_alpha()
        ],

        2: [
            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "blueorchid", "blueorchid_stage2", "blueorchid-2-1.png")
            ).convert_alpha(),

            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "blueorchid", "blueorchid_stage2", "blueorchid-2-2.png")
            ).convert_alpha()
        ],

        3: [
            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "blueorchid", "blueorchid_stage3", "blueorchid-3-1.png")
            ).convert_alpha(),

            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "blueorchid", "blueorchid_stage3", "blueorchid-3-2.png")
            ).convert_alpha()
        ]
    },
    "Cherry Blossom": {
        "slot": pygame.image.load(
            os.path.join(ASSETS_DIR, "plants", "cherryblossom", "cherryblossom_slotview", "cherryblossom_slotview.png")
        ).convert_alpha(),

        1: [
            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "cherryblossom", "cherryblossom_stage1", "cherryblossom-1-1.png")
            ).convert_alpha(),

            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "cherryblossom", "cherryblossom_stage1", "cherryblossom-1-2.png")
            ).convert_alpha()
        ],

        2: [
            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "cherryblossom", "cherryblossom_stage2", "cherryblossom-2-1.png")
            ).convert_alpha(),

            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "cherryblossom", "cherryblossom_stage2", "cherryblossom-2-2.png")
            ).convert_alpha()
        ],

        3: [
            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "cherryblossom", "cherryblossom_stage3", "cherryblossom-3-1.png")
            ).convert_alpha(),

            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "cherryblossom", "cherryblossom_stage3", "cherryblossom-3-2.png")
            ).convert_alpha()
        ]
    },
    "Golden Lily": {
        "slot": pygame.image.load(
            os.path.join(ASSETS_DIR, "plants", "goldenlily", "goldenlily_slotview", "goldenlily-slotview.png")
        ).convert_alpha(),

        1: [
            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "goldenlily", "goldenlily_stage1", "goldenlily-1-1.png")
            ).convert_alpha(),

            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "goldenlily", "goldenlily_stage1", "goldenlily-1-2.png")
            ).convert_alpha()
        ],

        2: [
            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "goldenlily", "goldenlily_stage2", "goldenlily-2-1.png")
            ).convert_alpha(),

            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "goldenlily", "goldenlily_stage2", "goldenlily-2-2.png")
            ).convert_alpha()
        ],

        3: [
            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "goldenlily", "goldenlily_stage3", "goldenlily-3-1.png")
            ).convert_alpha(),

            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "goldenlily", "goldenlily_stage3", "goldenlily-3-2.png")
            ).convert_alpha()
        ]
    },
    "Moon Blossom": {
        "slot": pygame.image.load(
            os.path.join(ASSETS_DIR, "plants", "moonblossom", "moonblossom_slotview", "moonblossom-slotview.png")
        ).convert_alpha(),

        1: [
            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "moonblossom", "moonblossom_stage1", "moonblossom-1-1.png")
            ).convert_alpha(),

            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "moonblossom", "moonblossom_stage1", "moonblossom-1-2.png")
            ).convert_alpha()
        ],

        2: [
            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "moonblossom", "moonblossom_stage2", "moonblossom-2-1.png")
            ).convert_alpha(),

            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "moonblossom", "moonblossom_stage2", "moonblossom-2-2.png")
            ).convert_alpha()
        ],

        3: [
            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "moonblossom", "moonblossom_stage3", "moonblossom-3-1.png")
            ).convert_alpha(),

            pygame.image.load(
                os.path.join(ASSETS_DIR, "plants", "moonblossom", "moonblossom_stage3", "moonblossom-3-2.png")
            ).convert_alpha()
        ]
    }
}
# Background music
pygame.mixer.music.load(
    os.path.join(ASSETS_DIR, "sounds", "background_music.ogg")
)
pygame.mixer.music.set_volume(0.4)  # Volume from 0.0 to 1.0
pygame.mixer.music.play(-1)  # -1 = infinite loop

# Sound effects
buy_sound = pygame.mixer.Sound(
    os.path.join(ASSETS_DIR, "sounds", "buy.ogg")
)
earn_sound = pygame.mixer.Sound(
    os.path.join(ASSETS_DIR, "sounds", "earn.ogg")
)

harvest_sound = pygame.mixer.Sound(
    os.path.join(ASSETS_DIR, "sounds", "harvest.ogg")
)
plant_sound = pygame.mixer.Sound(
    os.path.join(ASSETS_DIR, "sounds", "plant.ogg")
)
buy_sound.set_volume(0.5)
earn_sound.set_volume(0.4)
harvest_sound.set_volume(0.4)
plant_sound.set_volume(0.4)

#PNG BloomBit icon for UI
bloombit_image = pygame.image.load(
    os.path.join(ASSETS_DIR, "ui", "BloomBit.png")
).convert()
bloombit_image.set_colorkey((255, 255, 255))
bloombit_image = pygame.transform.scale(bloombit_image, (55, 55))

# Garden tiles setup
garden_rect = pygame.Rect(120, 120, 720, 480)
tile_size = 60
tiles = []
background_tile_size = 60
background_map = []

for x in range(0, WIDTH, background_tile_size):
    for y in range(0, HEIGHT, background_tile_size):

        background_map.append({
            "rect": pygame.Rect(
                x,
                y,
                background_tile_size,
                background_tile_size
            ),
            "image": random.choices(
                background_tiles,
                weights=[2, 3, 10]
            )[0]
        })
for x in range(garden_rect.left, garden_rect.right, tile_size):
    for y in range(garden_rect.top, garden_rect.bottom, tile_size):
        rect = pygame.Rect(x, y, tile_size, tile_size)
        tiles.append({
            "rect": rect,
            "grass_image": random.choice(grass_tiles),
            "boosted_image": random.choice(boosted_tiles),
                        
            "planted": False,
            "special": False,
            "boosted": False,
            "plant": None,
            "growth_stage": 0,
            "plant_time": 0
            })

# Slots setup
slots = []
slot_size = 70
slot_x = 900
slot_y = 140
slot_gap = 20
for i in range(5):
    rect = pygame.Rect(
        slot_x,
        slot_y + i * (slot_size + slot_gap),
        slot_size,
        slot_size
    )
    slots.append({
        "rect": rect,
        "selected": False,
        "seed": None,
        "amount": 0
    })

def add_seed_to_inventory(seed_name):

    # First try stacking onto existing seeds
    for slot in slots:
        if slot["seed"] == seed_name:
            if slot["amount"] < max_stack:
                slot["amount"] += 1
                return True

    # Then search for empty slot
    for slot in slots:

        if slot["seed"] is None:

            slot["seed"] = seed_name
            slot["amount"] = 1
            return True

    # Inventory full
    print("Inventory is full")
    floating_texts.append({
        "text": "Inventory Full!",
        "x": 400,
        "y": 300,
        "colour": (255, 0, 0),
        "timer": 20
    })
    return False

# Daisy seed placing (first slot) and overall stuff
slots[0]["selected"] = True
add_seed_to_inventory("Daisy")
selected_seed = "Daisy"
bloombits = 0
store_open = False
store_scroll = 0 #store scrolling mechanics
max_scroll = 500
save_file = "savegame.json" #Implement save/load functionality
floating_texts = []
floating_font = pygame.font.SysFont(None, 45)
max_stack = 10
plant_animation_frame = 0 #plant animation variables
last_plant_animation = 0
plant_animation_speed = 500
game_state = "menu"      #Decides what to draw on screen
show_menu_popup = False
menu_popup_rect = pygame.Rect(250, 200, 500, 250) #Popup menu in gameplay
yes_button = pygame.Rect(320, 360, 120, 50)
no_button = pygame.Rect(560, 360, 120, 50)
#---PLANT DICTIONARY---
plants = {

    "Daisy": {
        "buy_price": 2,
        "sell_price": 3,
        "grow_stage_2": 5000,
        "grow_stage_3": 10000,
        "slot_colour": (255, 255, 0),
        "stage_1_colour": (255, 0, 0),
        "stage_2_colour": (255, 255, 0),
        "stage_3_colour": (0, 255, 0)
    },
    
    "Tulip": {
        "buy_price": 5,
        "sell_price": 7,
        "grow_stage_2": 7000,
        "grow_stage_3": 14000,
        "slot_colour": (255, 255, 0),
        "stage_1_colour": (200, 25, 47),
        "stage_2_colour": (253, 255, 0),
        "stage_3_colour": (0, 255, 10)
    },

    "Sunflower": {
        "buy_price": 12,
        "sell_price": 18,
        "grow_stage_2": 9000,
        "grow_stage_3": 18000,
        "slot_colour": (0, 100, 255),
        "stage_1_colour": (0, 100, 255),
        "stage_2_colour": (140, 20, 240),
        "stage_3_colour": (255, 105, 180)
    },

    "Rose": {
        "buy_price": 35,
        "sell_price": 50,
        "grow_stage_2": 14000,
        "grow_stage_3": 25000,
        "slot_colour": (220, 20, 60),
        "stage_1_colour": (150, 0, 30),
        "stage_2_colour": (220, 20, 60),
        "stage_3_colour": (255, 100, 150)
    },

    "Lavender": {
        "buy_price": 80,
        "sell_price": 120,
        "grow_stage_2": 18000,
        "grow_stage_3": 35000,
        "slot_colour": (170, 100, 255),
        "stage_1_colour": (100, 50, 180),
        "stage_2_colour": (170, 100, 255),
        "stage_3_colour": (220, 180, 255)
    },
    "Blue Orchid": {
        "buy_price": 150,
        "sell_price": 220,
        "grow_stage_2": 14000,
        "grow_stage_3": 25000,
        "slot_colour": (220, 20, 60),
        "stage_1_colour": (150, 0, 30),
        "stage_2_colour": (220, 20, 60),
        "stage_3_colour": (255, 100, 150)
    },
    "Cherry Blossom": {
        "buy_price": 350,
        "sell_price": 500,
        "grow_stage_2": 14000,
        "grow_stage_3": 25000,
        "slot_colour": (220, 20, 60),
        "stage_1_colour": (150, 0, 30),
        "stage_2_colour": (220, 20, 60),
        "stage_3_colour": (255, 100, 150)
    },
    "Golden Lily": {
        "buy_price": 900,
        "sell_price": 1400,
        "grow_stage_2": 14000,
        "grow_stage_3": 25000,
        "slot_colour": (220, 20, 60),
        "stage_1_colour": (150, 0, 30),
        "stage_2_colour": (220, 20, 60),
        "stage_3_colour": (255, 100, 150)
    },
    "Moon Blossom": {
        "buy_price": 2500,
        "sell_price": 4000,
        "grow_stage_2": 14000,
        "grow_stage_3": 25000,
        "slot_colour": (220, 20, 60),
        "stage_1_colour": (150, 0, 30),
        "stage_2_colour": (220, 20, 60),
        "stage_3_colour": (255, 100, 150)
    }
}

def save_game():

    save_data = {

        "bloombits": bloombits,
        "selected_seed": selected_seed,

        "slots": [],
        "tiles": []

    }

    # Save slots
    for slot in slots:

        save_data["slots"].append({
            "seed": slot["seed"],
            "amount": slot["amount"]
        })

    # Save tiles
    for tile in tiles:

        save_data["tiles"].append({

            "plant": tile["plant"],
            "growth_stage": tile["growth_stage"],
            "plant_time": tile["plant_time"],
            "planted": tile["planted"]

        })

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxjsonxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    with open(save_file, "w") as file:
        json.dump(save_data, file)
        
def load_game():

    global bloombits
    global selected_seed

    try:

        with open(save_file, "r") as file:
            save_data = json.load(file)
        bloombits = save_data["bloombits"]
        selected_seed = save_data["selected_seed"]


        # Load slots
        for i in range(len(slots)):

            slots[i]["seed"] = save_data["slots"][i]["seed"]
            slots[i]["amount"] = save_data["slots"][i]["amount"]

        # Load tiles
        for i in range(len(tiles)):

            tiles[i]["plant"] = save_data["tiles"][i]["plant"]
            tiles[i]["growth_stage"] = save_data["tiles"][i]["growth_stage"]
            tiles[i]["planted"] = save_data["tiles"][i]["planted"]
                # Reset timer safely
            tiles[i]["plant_time"] = pygame.time.get_ticks()
    except:
        print("No save file found")
        slots[0]["selected"] = True
        add_seed_to_inventory("Daisy")
        selected_seed = "Daisy"


# GAME LOOP-------------------------------------------------------------------------------------------
load_game()
while running:
    current_time = pygame.time.get_ticks()
        # WATER ANIMATION
    if current_time - last_water_update > water_animation_speed:
        water_frame_index += 1

        if water_frame_index >= len(water_frames):
            water_frame_index = 0

        last_water_update = current_time
    # PLANT ANIMATION
    if current_time - last_plant_animation > plant_animation_speed:
        plant_animation_frame += 1
        if plant_animation_frame >= 2:
            plant_animation_frame = 0
        last_plant_animation = current_time

    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_game()
            pygame.quit()
            sys.exit()
        # -------------------------
        # KEYBOARD INPUT
        # -------------------------
        elif event.type == pygame.KEYDOWN:
            #OPEN MENU
            if event.key == pygame.K_ESCAPE:
                if game_state == "playing":
                    if show_menu_popup:
                        show_menu_popup = False
                    else:
                        show_menu_popup = True
            # OPEN/CLOSE STORE
            if game_state == "playing":
                if event.key == pygame.K_e:
                    store_open = not store_open
        # -------------------------
        # MOUSE INPUT
        # -------------------------
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # =========================
            # MENU
            # =========================
            if game_state == "menu":
                # START/NEW GAME BUTTON
                if start_button.collidepoint(mouse_pos): 
                    # RESET TILES
                    for tile in tiles:
                        tile["plant"] = None
                        tile["growth_stage"] = 0
                        tile["planted"] = False
                        tile["plant_time"] = 0
                    # RESET INVENTORY
                    for slot in slots:
                        slot["seed"] = None
                        slot["amount"] = 0
                        slot["selected"] = False
                    slots[0]["selected"] = True
                    add_seed_to_inventory("Daisy")
                    selected_seed = "Daisy"
                    game_state = "playing"
                    #RESET BLOOMBITS
                    bloombits = 0

                # CONTINUE
                elif continue_button.collidepoint(mouse_pos):
                    load_game()
                    game_state = "playing"
                
                # EXIT BUTTON
                elif exit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

            # =========================
            # GAMEPLAY
            # =========================
            elif game_state == "playing":
                #MENU POPUP HANDLING
                if show_menu_popup:
                    if yes_button.collidepoint(mouse_pos):
                        save_game()
                        game_state = "menu"
                        show_menu_popup = False
                        store_open = False
                    elif no_button.collidepoint(mouse_pos):
                        show_menu_popup = False
                    continue
                # STORE BUTTONS
                if store_open:
                    for button in store_buttons:
                        if button["rect"].collidepoint(mouse_pos):
                            plant_name = button["plant"]
                            if bloombits >= plants[plant_name]["buy_price"]:
                                if add_seed_to_inventory(plant_name):
                                    bloombits -= plants[plant_name]["buy_price"]
                                    buy_sound.play()
                else:
                    # SLOT CLICKING
                    for slot in slots:
                        if slot["rect"].collidepoint(mouse_pos):
                            for other_slot in slots:
                                other_slot["selected"] = False
                            slot["selected"] = True
                            selected_seed = slot["seed"]
                    # TILE INTERACTION
                    for tile in tiles:
                        if tile["rect"].collidepoint(mouse_pos):
                            # HARVEST
                            if tile["growth_stage"] == 3:
                                harvested_plant = tile["plant"]
                                tile["planted"] = False
                                tile["plant"] = None
                                tile["growth_stage"] = 0
                                tile["plant_time"] = 0
                                reward = plants[harvested_plant]["sell_price"]
                                bloombits += reward
                                #Floating text for harvest reward '+ x BloomBits'
                                floating_texts.append({
                                    "text": f"+{reward} BloomBits",
                                    "x": tile["rect"].centerx - 50,
                                    "y": tile["rect"].centery,
                                    "colour": (255, 215, 0),
                                    "timer": 13
                                })
                                harvest_sound.play()
                                earn_sound.play()
                            # PLANT
                            elif not tile["planted"] and not tile["special"]:
                                if selected_seed is not None:
                                    for slot in slots:
                                        if slot["selected"]:
                                            if slot["amount"] > 0:
                                                tile["planted"] = True
                                                tile["plant"] = selected_seed
                                                tile["growth_stage"] = 1
                                                tile["plant_time"] = pygame.time.get_ticks()
                                                slot["amount"] -= 1
                                                plant_sound.play()
                                                if slot["amount"] <= 0:
                                                    slot["seed"] = None
                                                    slot["selected"] = False
                                                    selected_seed = None
        # -------------------------
        # STORE SCROLL
        # -------------------------
        elif event.type == pygame.MOUSEWHEEL:
            if store_open:
                store_scroll -= event.y * 30
                store_scroll = max(0, min(store_scroll, max_scroll))

    # PLANT GROWTH SYSTEM
    for tile in tiles:
        if tile["planted"]:

            plant_data = plants[tile["plant"]]
            growth_time = current_time - tile["plant_time"]

            if growth_time >= plant_data["grow_stage_3"]:
                tile["growth_stage"] = 3

            elif growth_time >= plant_data["grow_stage_2"]:
                tile["growth_stage"] = 2
    #Game state rendering
    if game_state == "menu":
        screen.fill((50, 120, 50))
        title_font = pygame.font.SysFont(None, 100)
        title_text = title_font.render(
            "GOLDEN GARDEN - v1.0",
            True,
            (255, 255, 255)
        )
        screen.blit(title_text, (100, 120))
        # Draw buttons
        pygame.draw.rect(screen, (220, 220, 220), start_button)
        pygame.draw.rect(screen, (220, 220, 220), continue_button)
        pygame.draw.rect(screen, (220, 220, 220), exit_button)
        #Button text rendering        
        start_text = button_font.render(
            "Start New Game",
            True,
            (0, 0, 0)
        )
        continue_text = button_font.render(
            "Continue Game",
            True,
            (0, 0, 0)
        )
        exit_text = button_font.render(
            "Exit",
            True,
            (0, 0, 0)
        )
        screen.blit(#Makes it be centered on the button
            start_text,
            start_text.get_rect(center=start_button.center)
        )
        screen.blit(
            continue_text,
            continue_text.get_rect(center=continue_button.center)
        )
        screen.blit(
            exit_text,
            exit_text.get_rect(center=exit_button.center)
        )
        # CREDITS
        credits_font = pygame.font.SysFont(None, 20)
        credits_text = credits_font.render(
            "Golden Garden v1.0 | Made with <3 by Saraa_",
            True,
            (255,255,255)
        )
        screen.blit(
            credits_text,
            credits_text.get_rect(
                center=(WIDTH // 2, HEIGHT - 15)
            )
        )
        pygame.display.flip()
        clock.tick(60)
        continue
    
    # Draw background tiles
    for bg_tile in background_map:
            screen.blit(bg_tile["image"], bg_tile["rect"])
            
            # BloomBits display background
            ui_rect = pygame.Rect(20, 20, 220, 60)
            pygame.draw.rect(screen, (50, 50, 50), ui_rect)
            pygame.draw.rect(screen, (255, 255, 255), ui_rect, 3)
            money_text = font.render(str(bloombits), True, (255, 255, 255))
            screen.blit(money_text, (35, 32))
            
            # BloomBit icon
            screen.blit(bloombit_image, (175, 22))
    # Draw tiles
    for tile in tiles:
        colour = (0, 100, 0)
        if tile["boosted"]:
            colour = (85, 107, 47)
        if tile["special"]: #Boosted tile rendering
            screen.blit(water_frames[water_frame_index], tile["rect"])
        elif tile["boosted"]:
            screen.blit(tile["boosted_image"], tile["rect"])
        else:
            screen.blit(tile["grass_image"], tile["rect"])
        pygame.draw.rect(screen, (0, 0, 0), tile["rect"], 1)
        tile["boosted"] = False
        if tile["plant"] is not None:
            plant_image = plant_images[tile["plant"]][tile["growth_stage"]][plant_animation_frame]
            screen.blit(
                plant_image,
                (tile["rect"].x + 5, tile["rect"].y + 5)
            )
            plant_data = plants[tile["plant"]]
            plant_colour = plant_data["stage_1_colour"]
            if tile["growth_stage"] == 2:
                plant_colour = plant_data["stage_2_colour"]
            elif tile["growth_stage"] == 3:
                plant_colour = plant_data["stage_3_colour"]
            # Define plant rect inside the tile before drawing
            plant_rect = pygame.Rect(
                tile["rect"].x + 5,
                tile["rect"].y + 5,
                tile_size - 10,
                tile_size - 10,
            )

        corner_positions = [
            (garden_rect.left, garden_rect.top),
            (garden_rect.right - tile_size, garden_rect.top),
            (garden_rect.left, garden_rect.bottom - tile_size),
            (garden_rect.right - tile_size, garden_rect.bottom - tile_size)
        ]

        for tile in tiles:
            if tile["rect"].topleft in corner_positions:
                tile["special"] = True
        
        #Boosted tiles setup (around water tiles)
        boost_positions = []

        # Top-left corner
        boost_positions.extend([
            (garden_rect.left + tile_size, garden_rect.top),
            (garden_rect.left, garden_rect.top + tile_size),
            (garden_rect.left + tile_size, garden_rect.top + tile_size)
        ])

        # Top-right corner
        boost_positions.extend([
            (garden_rect.right - tile_size * 2, garden_rect.top),
            (garden_rect.right - tile_size, garden_rect.top + tile_size),
            (garden_rect.right - tile_size * 2, garden_rect.top + tile_size)
        ])

        # Bottom-left corner
        boost_positions.extend([
            (garden_rect.left + tile_size, garden_rect.bottom - tile_size),
            (garden_rect.left, garden_rect.bottom - tile_size * 2),
            (garden_rect.left + tile_size, garden_rect.bottom - tile_size * 2)
        ])

        # Bottom-right corner
        boost_positions.extend([
            (garden_rect.right - tile_size * 2, garden_rect.bottom - tile_size),
            (garden_rect.right - tile_size, garden_rect.bottom - tile_size * 2),
            (garden_rect.right - tile_size * 2, garden_rect.bottom - tile_size * 2)
        ])

        for tile in tiles:
            if tile["rect"].topleft in boost_positions:
                tile["boosted"] = True
        
    # Fence
    pygame.draw.rect(screen, (139, 69, 19), garden_rect, 6)
    
    # Slots UI
    for slot in slots:
        colour = (180, 180, 180)
        if slot["selected"]:
            colour = (220, 220, 220)
        pygame.draw.rect(screen, colour, slot["rect"])
        
        # Seed placeholder and stack amount rendering
        if slot["amount"] > 0:
            if slot["amount"] > 0:
                seed_image = plant_images[slot["seed"]]["slot"]
                screen.blit(
                    seed_image,
                    (slot["rect"].x + 10, slot["rect"].y + 10)
                )
                amount_text = slot_font.render(str(slot["amount"]), True, (0, 0, 0))
                screen.blit(
                    amount_text,
                    (slot["rect"].x + 5, slot["rect"].y + 45)
                )
            #Stack quantity on top of slot graphics
            amount_text = slot_font.render(str(slot["amount"]), True, (0, 0, 0))
            screen.blit(amount_text, (slot["rect"].x + 5, slot["rect"].y + 45))
            
        # Border
        border_colour = (50, 50, 50)
        if slot["selected"]:
            border_colour = (255, 255, 255)
        pygame.draw.rect(screen, border_colour, slot["rect"], 4)
        
  # Store UI Rendering Window
    if store_open:
        # Store background
        store_rect = pygame.Rect(250, 80, 500, 550)
        pygame.draw.rect(screen, (220, 190, 120), store_rect)
        pygame.draw.rect(screen, (80, 60, 20), store_rect, 5)
        # Store title
        title_text = font.render("Seed Store", True, (0, 0, 0))
        screen.blit(title_text, (410, 100))

        # Store scrolling plants
        y_offset = 160 - store_scroll
        store_buttons = []
        for plant_name, plant_data in plants.items():
            # Only draw visible items
            if y_offset > 120 and y_offset < 560:
                # Plant text
                text = font.render(
                    f"{plant_name}: {plant_data['buy_price']} BloomBits",
                    True,
                    (0, 0, 0)
                )
                screen.blit(text, (290, y_offset))
                # Buy button
                buy_button = pygame.Rect(365, y_offset + 40, 270, 40)
                pygame.draw.rect(
                    screen,
                    plant_data["slot_colour"],
                    buy_button
                )
                button_text = font.render("BUY", True, (0, 0, 0))
                screen.blit(button_text, (470, y_offset + 47))
                # Save button info
                store_buttons.append({
                    "rect": buy_button,
                    "plant": plant_name
                })
            y_offset += 110
        #Footer section store closing hint
        hint_text = font.render("Press E to close", True, (40, 40, 40))
        screen.blit(hint_text, (420, 585))

    # Floating text rendering
    for text in floating_texts[:]:
        text_surface = floating_font.render(
            text["text"],
            True,
            text["colour"]
        )
        screen.blit(
            text_surface,
            (text["x"], text["y"])
        )
        # Move upward slowly
        text["y"] -= 0.5
        # Reduce timer
        text["timer"] -= 1
        # Delete expired text
        if text["timer"] <= 0:
            floating_texts.remove(text)
    
    # =========================
    # MENU POPUP DRAWING
    # =========================

    if show_menu_popup:
        # Dark transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(120)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        # Popup background
        pygame.draw.rect(screen, (230, 230, 230), menu_popup_rect)
        pygame.draw.rect(screen, (40, 40, 40), menu_popup_rect, 5)
        # Text
        popup_text = font.render(
            "Return to main menu?",
            True,
            (0, 0, 0)
        )
        screen.blit(
            popup_text,
            popup_text.get_rect(center=(500, 260))
        )
        # YES button
        pygame.draw.rect(screen, (80, 180, 80), yes_button)
        yes_text = font.render("YES", True, (255, 255, 255))
        screen.blit(
            yes_text,
            yes_text.get_rect(center=yes_button.center)
        )
        # NO button
        pygame.draw.rect(screen, (180, 80, 80), no_button)
        no_text = font.render("NO", True, (255, 255, 255))
        screen.blit(
            no_text,
            no_text.get_rect(center=no_button.center)
        )
    # Credits text
    credits_font = pygame.font.SysFont(None, 20)
    credits_text = credits_font.render(
        "Made with <3 by Saraa_",
        True,
        (0, 0, 0)
    )
    credits_rect = credits_text.get_rect(
        center=(WIDTH // 2, HEIGHT - 15)
    )
    screen.blit(
        credits_text,
        credits_rect
    )
    pygame.display.flip()
    clock.tick(60)
pygame.quit()