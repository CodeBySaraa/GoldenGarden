import pygame
import sys
import json
import random
import os
import winshell
from win32com.client import Dispatch
#---------
from flowerdictionary import plants
from buyables import buyables
from assets import resource_path, load_assets

pygame.init()
pygame.mixer.init()

#Hide Windows cursor
pygame.mouse.set_visible(False)

#File creater (adapter for any OS)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")


#=========================
# Window setup
#=========================
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Golden Garden")
icon = pygame.image.load(resource_path("assets/icons/icon.png")).convert_alpha()
pygame.display.set_icon(icon) #Change pygame icon for flower icon
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
#Internal version tracking constant
GAME_VERSION = "1.0.2-beta"
#Assets loading
assets = load_assets()

#Desktop shortcut creation and pointing
if getattr(sys, "frozen", False):
    target = sys.executable
else:
    target = os.path.abspath(sys.argv[0])

#Animation variables for water tiles
water_frame_index = 0
last_water_update = 0
water_animation_speed = 500

#PNG custom cursor
cursor_normal = pygame.image.load(resource_path("assets/cursors/cursor_normal.png")).convert_alpha()
cursor_hand = pygame.image.load(resource_path("assets/cursors/cursor_hand.png")).convert_alpha()

# Background music setup
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)  # -1 = infinite loop

# Sound effects volume
assets['sounds']['buy_sound'].set_volume(0.5)
assets['sounds']['earn_sound'].set_volume(0.4)
assets['sounds']['harvest_sound'].set_volume(0.4)
assets['sounds']['plant_sound'].set_volume(0.4)
assets['sounds']['shovel_sound'].set_volume(0.4)

#PNG BloomBit icon for UI
bloombit_image = pygame.image.load(
    resource_path("assets/ui/BloomBit.png")
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
                assets['background_tiles'],
                weights=[2, 3, 10]
            )[0]
        })
for x in range(garden_rect.left, garden_rect.right, tile_size):
    for y in range(garden_rect.top, garden_rect.bottom, tile_size):
        rect = pygame.Rect(x, y, tile_size, tile_size)
        tiles.append({
            "rect": rect,
            "grass_image": random.choice(assets['grass_tiles']),
            "boosted_image": random.choice(assets['boosted_tiles']),
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
    floating_texts.append({
        "text": "Inventory Full!",
        "x": 400,
        "y": 300,
        "colour": (255, 0, 0),
        "timer": 20
    })
    return False

#=====================
# Overall variables
#=====================
# Daisy seed placing (first slot) and
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
shovel_price = 15 #shovel price for store
shovel_count = 0
shovel_selected = False
shovels = 0
selected_tool = None #Deselects something when you select another thing
#Shovel slot
shovel_slot = pygame.Rect(20, 90, 70, 70)
#Flower shovel mechanics for refund and recovery chance
Shovel_Refund = 0.40
Seed_recovery_chance = 0.50
shovel_price = 15
show_welcome_popup = False #Welcome message first time you open the game
first_launch = True #See if its the first time
welcome_alpha = 0 #Just does a fade-in for the welcome popup
show_desktop_shortcut_prompt = False #Detects first launch and prompts to create desktop shortcut
# Desktop shortcut popup
desktop_popup_rect = pygame.Rect(250, 180, 500, 240)
desktop_yes_button = pygame.Rect(305, 355, 160, 45)
desktop_no_button = pygame.Rect(535, 355, 160, 45)

#Save migration system definition
def migrate_save(save_data):
    save_version = save_data.get("game_version", "1.0")
    if save_version == GAME_VERSION:
        return save_data
    #print(f"Migrating save from {save_version} to {GAME_VERSION}")
    # Future migrations go here
    save_data["game_version"] = GAME_VERSION
    return save_data

#Create desktop shortcut function
def create_desktop_shortcut():
    desktop = winshell.desktop()
    shortcut_path = os.path.join(
        desktop,
        "Golden Garden.lnk"
        )
    if getattr(sys, "frozen", False):
        target = sys.executable
    else:
        target = os.path.abspath(sys.argv[0])
    working_directory = os.path.dirname(target)
    shell = Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = working_directory
    shortcut.IconLocation = target + ",0"
    shortcut.save()

def save_game():

    save_data = {
        "bloombits": bloombits,
        "selected_seed": selected_seed,
        "shovels": shovels,
        "shovel_price": shovel_price,
        "first_launch": first_launch,
        "game_version": GAME_VERSION,
        "show_desktop_shortcut_prompt": show_desktop_shortcut_prompt,

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
        save_data = migrate_save(save_data)
        
def load_game():
    #print("load_game() called")

    global bloombits
    global selected_seed
    global shovels
    global shovel_price
    global first_launch

    try:
        with open(save_file, "r") as file:
            save_data = json.load(file)
        bloombits = save_data["bloombits"]
        selected_seed = save_data["selected_seed"]
        shovels = save_data.get("shovels", 0)
        shovel_price = save_data.get("shovel_price", 15)
        first_launch = save_data.get("first_launch", True)
        show_desktop_shortcut_prompt = save_data.get("show_desktop_shortcut_prompt", True)
        save_version = save_data.get("game_version", "1.0.0")
        if save_version != GAME_VERSION:
            save_data = migrate_save(save_data)
        if GAME_VERSION != save_version:
            #print("The save version differs from the game version.")
            #print("Migration may be required.")
            pass
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
    except FileNotFoundError:
        #print("No save found. Creating a new one...")
        save_game()
    except Exception as e:
        #print(f"Error loading save: {e}")
        pass

        shovels = 0
        shovel_price = 15
        selected_tool = None
        slots[0]["selected"] = True
        add_seed_to_inventory("Daisy")
        selected_seed = "Daisy"


# GAME LOOP-------------------------------------------------------------------------------------------
load_game()
if first_launch:
    show_desktop_shortcut_prompt = True

while running:
    current_time = pygame.time.get_ticks()
    #Custom cursor handling (makes the normal one standard)
    mouse_pos = pygame.mouse.get_pos()
    hovering_clickable = False
    current_cursor = cursor_normal
    # WATER ANIMATION
    if current_time - last_water_update > water_animation_speed:
        water_frame_index += 1

        if water_frame_index >= len(assets['water_frames']):
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
            # WELCOME POPUP
            # =========================
            if show_welcome_popup:
                if welcome_button.collidepoint(mouse_pos):
                    hovering_clickable = True
                    show_welcome_popup = False
                    first_launch = False
                    welcome_alpha = 0
                    save_game()

                continue
            
            #=========================
            # DESKTOP SHORTCUT PROMPT
            #=========================
            if show_desktop_shortcut_prompt:
                if desktop_yes_button.collidepoint(mouse_pos):
                    #print("YES clicked")
                    create_desktop_shortcut()
                    show_desktop_shortcut_prompt = False
                    save_game()
                elif desktop_no_button.collidepoint(mouse_pos):
                    #print("NO clicked")
                    show_desktop_shortcut_prompt = False
                    save_game()
                continue
            # =========================
            # MENU
            # =========================
            if game_state == "menu":
                if not show_desktop_shortcut_prompt:
                    #print(first_launch)
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
                        # RESET SHOVEL DATA
                        shovels = 0
                        shovel_price = 15
                        selected_tool = None
                        if first_launch:
                            show_welcome_popup = True

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
                            item = button["plant"]
                            if item == "Shovel":
                                if bloombits >= shovel_price:
                                    bloombits -= shovel_price
                                    shovels += 1
                                    shovel_price += 5
                                    assets['buy_sound'].play()
                            else:
                                if bloombits >= plants[item]["buy_price"]:
                                    if add_seed_to_inventory(item):
                                        bloombits -= plants[item]["buy_price"]
                                        assets['sounds']['buy_sound'].play()
                else:
                    # SLOT CLICKING
                    for slot in slots:
                        if slot["rect"].collidepoint(mouse_pos):
                            for other_slot in slots:
                                other_slot["selected"] = False
                            selected_tool = None
                            slot["selected"] = True
                            selected_seed = slot["seed"]
                            shovel_selected = False
                    # TILE INTERACTION
                    for tile in tiles:
                        if tile["rect"].collidepoint(mouse_pos):
                            # SHOVEL
                            if selected_tool == "shovel":
                                if tile["planted"]:
                                    plant_name = tile["plant"]
                                    tile["planted"] = False
                                    tile["plant"] = None
                                    tile["growth_stage"] = 0
                                    tile["plant_time"] = 0
                                    refund = int(plants[plant_name]["buy_price"] * 0.4)
                                    bloombits += refund
                                    if random.random() < 0.25:
                                        add_seed_to_inventory(plant_name)
                                        floating_texts.append({
                                            "text": f"+ {plant_name} Seed",
                                            "x": tile["rect"].centerx - 50,
                                            "y": tile["rect"].centery - 20,
                                            "colour": (120,255,120),
                                            "timer": 13
                                        })
                                    assets['sounds']['shovel_sound'].play()
                                    #Floating text for refund reward '+ x BloomBits'
                                    floating_texts.append({
                                        "text": f"+{refund} BloomBits",
                                        "x": tile["rect"].centerx - 50,
                                        "y": tile["rect"].centery,
                                        "colour": (120, 255, 120),
                                        "timer": 13
                                    })
                                    if shovels > 0:
                                        shovels -= 1
                                    if shovels == 0:
                                        selected_tool = None
                                elif not tile["planted"]:
                                    selected_tool = None
                                break
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
                                assets['sounds']['harvest_sound'].play()
                                assets['sounds']['earn_sound'].play()
                            # PLANT
                            elif not tile["planted"] and not tile["special"]:
                                if selected_seed is not None and selected_tool is None:
                                    for slot in slots:
                                        if slot["selected"]:
                                            if slot["amount"] > 0:
                                                tile["planted"] = True
                                                tile["plant"] = selected_seed
                                                tile["growth_stage"] = 1
                                                tile["plant_time"] = pygame.time.get_ticks()
                                                slot["amount"] -= 1
                                                assets['sounds']['plant_sound'].play()
                                                if slot["amount"] <= 0:
                                                    slot["seed"] = None
                                                    slot["selected"] = False
                                                    selected_seed = None
            # SHOVEL BUTTON
            if shovel_slot.collidepoint(mouse_pos):
                if shovels == 0:
                    if bloombits >= shovel_price:
                        bloombits -= shovel_price
                        shovels = 1
                        assets['buy_sound'].play()
                        shovel_price = int(shovel_price * 1.2)
                else:
                    if selected_tool == "shovel":
                        selected_tool = None
                    else: #Deselects seeds when shovel selected
                        selected_tool = "shovel"
                        for slot in slots:
                            slot["selected"] = False
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
    
    # -------------------------
    # FIRST LAUNCH DESKTOP POPUP
    # -------------------------
    if show_desktop_shortcut_prompt:
        # Don't draw the menu yet
        screen.fill((50, 120, 50))

    #Game state rendering
    if game_state == "menu":
        screen.fill((50, 120, 50))
        title_font = pygame.font.SysFont(None, 100)
        title_text = title_font.render(
            "GOLDEN GARDEN-v1.0.2-beta",
            True,
            (255, 255, 255)
        )
        screen.blit(title_text, (0, 120))
        # Draw buttons
        pygame.draw.rect(screen, (220, 220, 220), start_button)
        pygame.draw.rect(screen, (220, 220, 220), continue_button)
        pygame.draw.rect(screen, (220, 220, 220), exit_button)
        if start_button.collidepoint(mouse_pos) or continue_button.collidepoint(mouse_pos) or exit_button.collidepoint(mouse_pos): #Makes cursor change to hand when hovering over buttons
            hovering_clickable = True
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
        screen.blit(        #Makes it be centered on the button
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
            "Golden Garden v1.0.2-beta | Made with <3 by Saraa_",
            True,
            (255,255,255)
        )
        screen.blit(
            credits_text,
            credits_text.get_rect(
                center=(WIDTH // 2, HEIGHT - 15)
            )
        )
    elif game_state == "playing":
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
                screen.blit(assets['water_frames'][water_frame_index], tile["rect"])
            elif tile["boosted"]:
                screen.blit(tile["boosted_image"], tile["rect"])
            else:
                screen.blit(tile["grass_image"], tile["rect"])
            pygame.draw.rect(screen, (0, 0, 0), tile["rect"], 1)
            tile["boosted"] = False
            if tile["plant"] is not None:
                plant_image = assets['plant_images'][tile["plant"]][tile["growth_stage"]][plant_animation_frame]
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
            if slot["rect"].collidepoint(mouse_pos): #Slot highlight when hovered over and cursor to hand
                hovering_clickable = True
                colour = (220, 220, 220)
            pygame.draw.rect(screen, colour, slot["rect"])
            
            # Seed placeholder and stack amount rendering
            if slot["amount"] > 0:
                if slot["amount"] > 0:
                    seed_image = assets['plant_images'][slot["seed"]]["slot"]
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
        # ==========================
        # SHOVEL SLOT
        # ==========================
        if shovel_slot.collidepoint(mouse_pos):
            hovering_clickable = True
            shovel_colour = (220,220,220)
        else:
            shovel_colour = (180,180,180)
        pygame.draw.rect(screen, shovel_colour, shovel_slot)
        if shovels > 0:
            screen.blit(assets['shovel_image'], (27,100))
        else: #If no shovels, display a plus sign to indicate purchase
            plus_text = slot_font.render("+", True, (255,255,255))
            screen.blit(plus_text, (47,110))

        #Nº of shovels in inventory
        shovel_text = slot_font.render(
            f"x{max(0, shovels)}",
            True,
            (255,255,255)
        )
        #Price of shovel and colour change
        if bloombits >= shovel_price:
            price_colour = (33, 242, 0)      # Green
        else:
            price_colour = (220, 80, 80)     # Red

        # Draw price
        price_text = slot_font.render(
            f"{shovel_price}",
            True,
            price_colour
        )
        screen.blit(price_text, (15,165))

        #Draw bloombit resized
        bloombit_small = pygame.transform.smoothscale(
        bloombit_image.convert_alpha(),
        (20, 20)
        )
        # BloomBit icon
        screen.blit(
            bloombit_small,
            (15 + price_text.get_width() + 4, 164)
        )
        #Higlight shovel slot when selected
        if selected_tool == "shovel":
            if current_cursor == cursor_normal: 
                hovering_clickable = True
            pygame.draw.rect(
                screen,
                (220, 220, 220),
                shovel_slot,
                4
            )
                # Deselect every inventory slot
            for slot in slots:
                slot["selected"] = False
            selected_seed = None

        # Credits text
        credits_font = pygame.font.SysFont(None, 20)
        credits_text = credits_font.render(
            "Made with <3 by Saraa_",
            True,
            (255, 255, 255)
        )
        credits_rect = credits_text.get_rect(
            center=(WIDTH // 2, HEIGHT - 15)
        )
        screen.blit(
            credits_text,
            credits_rect
        )
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
                    mouse_pos = pygame.mouse.get_pos()
                    # Draw button
                    pygame.draw.rect(
                        screen,
                        plant_data["slot_colour"],
                        buy_button
                    )
                    # Border (changes colour when hovered)
                    border_colour = (40, 90, 40)
                    if buy_button.collidepoint(mouse_pos):
                        hovering_clickable = True
                        border_colour = (70, 140, 70)
                    pygame.draw.rect(screen, border_colour, buy_button, 3)

                    # Hover overlay
                    if buy_button.collidepoint(mouse_pos):
                        hovering_clickable = True
                        hover = pygame.Surface((buy_button.width, buy_button.height), pygame.SRCALPHA)
                        hover.fill((255, 255, 255, 45))
                        screen.blit(hover, buy_button.topleft)

                    # BUY text
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
    
        # ================================
        #  RETURN TO MENU POPUP DRAWING
        # ================================

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
    # =========================
    # WELCOME POPUP
    # =========================
    if show_welcome_popup:
        # Dark background
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(min(welcome_alpha, 140)) #Makes the overlay fade happen
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        # Popup box
        popup_rect = pygame.Rect(225, 190, 540, 300)
        if welcome_alpha < 255:
            welcome_alpha += 12 #Makes the box fade happen
        #The actual box fade
        popup_surface = pygame.Surface((540,300), pygame.SRCALPHA)
        popup_surface.set_alpha(welcome_alpha)
        pygame.draw.rect(
            popup_surface,
            (240,230,190),
            (0,0,540,300)
        )
        pygame.draw.rect(
            popup_surface,
            (120,90,40),
            (0,0,540,300),
            5
        )

        title = font.render("Welcome to Golden Garden!", True, (0,0,0))
        popup_surface.blit(title, (85,30))
        line1 = slot_font.render(
            "Thank you for downloading the game!",
            True,
            (0,0,0)
        )
        popup_surface.blit(line1, (95,80))
        line2 = slot_font.render(
            "I hope you enjoy growing your garden.",
            True,
            (0,0,0)
        )
        popup_surface.blit(line2, (92,109))
        line3 = slot_font.render(
            "Happy Gardening!",
            True,
            (0,0,0)
        )
        popup_surface.blit(line3, (174,170))
        # Button of 'start playing'
        welcome_button = pygame.Rect(370, 400, 240, 50)
        hovering_clickable = True
        pygame.draw.rect(
            popup_surface,
            (90,170,90),
            (145,210,240,50)
        )
        pygame.draw.rect(
            popup_surface,
            (40,90,40),
            (145,210,240,50),
            3
        )
        button_text = slot_font.render("Start Playing", True, (255,255,255))
        popup_surface.blit(button_text, (200,225))

        screen.blit(popup_surface, popup_rect.topleft)

    # =========================
    # DESKTOP SHORTCUT POPUP
    # =========================
    #print("Drawing check:", show_desktop_shortcut_prompt)
    #if show_desktop_shortcut_prompt:
        #print("Drawing desktop popup")
        # Dark overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(140)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        # Popup box
        popup_rect = pygame.Rect(250, 180, 500, 240)
        pygame.draw.rect(screen, (225, 255, 225), popup_rect)
        pygame.draw.rect(screen, (90, 90, 90), popup_rect, 4)
        # Title
        title = font.render(
            "Create Desktop Shortcut?",
            True,
            (0, 0, 0)
        )
        screen.blit(title, (305, 205))
        # Text
        line1 = slot_font.render(
            "Would you like Golden Garden to create",
            True,
            (40, 40, 40)
        )
        screen.blit(line1, (295, 255))
        line2 = slot_font.render(
            "a shortcut on your desktop?",
            True,
            (40, 40, 40)
        )
        screen.blit(line2, (340, 282))
        # YES button
        pygame.draw.rect(screen, (80, 170, 80), desktop_yes_button)
        pygame.draw.rect(screen, (40, 90, 40), desktop_yes_button, 3)
        yes_text = slot_font.render(
            "YES",
            True,
            (255,255,255)
        )
        screen.blit(
            yes_text,
            yes_text.get_rect(center=desktop_yes_button.center)
        )
        # NO button
        pygame.draw.rect(screen, (180, 80, 80), desktop_no_button)
        pygame.draw.rect(screen, (90, 40, 40), desktop_no_button, 3)
        no_text = slot_font.render(
            "NO",
            True,
            (255,255,255)
        )
        screen.blit(
            no_text,
            no_text.get_rect(center=desktop_no_button.center)
        )

    # Custom cursor rendering (normal)
    mouse_pos = pygame.mouse.get_pos()
    if hovering_clickable:
        current_cursor = cursor_hand
    else:
        current_cursor = cursor_normal
    screen.blit(current_cursor, mouse_pos)
    pygame.display.flip()
    clock.tick(144)
pygame.quit()