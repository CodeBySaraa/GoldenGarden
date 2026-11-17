import os
import pygame
import sys

#==========================
# Directories adapter
#==========================
def resource_path(relative_path):
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

#=========================
# Load assets variable
#=========================
def load_assets():

    grass_tiles = [
    pygame.image.load(resource_path("assets/tiles/grass_normal/gt1.png")),
    pygame.image.load(resource_path("assets/tiles/grass_normal/gt2.png")),
    pygame.image.load(resource_path("assets/tiles/grass_normal/gt3.png")),
    pygame.image.load(resource_path("assets/tiles/grass_normal/gt4.png"))
    ]
    water_frames = [
    pygame.image.load(resource_path("assets/tiles/water/w1.png")),
    pygame.image.load(resource_path("assets/tiles/water/w2.png")),
    pygame.image.load(resource_path("assets/tiles/water/w3.png"))
    ]
    background_tiles = [
    pygame.image.load(resource_path("assets/tiles/background/bg1.png")),
    pygame.image.load(resource_path("assets/tiles/background/bg2.png")),
    pygame.image.load(resource_path("assets/tiles/background/bg3.png"))
    ]
    boosted_tiles = [
    pygame.image.load(resource_path("assets/tiles/grass_boosted/gb1.png")),
    pygame.image.load(resource_path("assets/tiles/grass_boosted/gb2.png"))
    ]

    plant_images = {
        "Daisy": {
            "slot": pygame.image.load(
                resource_path("assets/plants/daisy/daisy_slotview/daisy_slotview.png")
            ).convert_alpha(),
            1: [
                pygame.image.load(
                resource_path("assets/plants/daisy/daisy_stage1/daisy-1-1.png")
                ).convert_alpha(),
                pygame.image.load(
                    resource_path("assets/plants/daisy/daisy_stage1/daisy-1-2.png")
                ).convert_alpha()
            ],
            2: [
                pygame.image.load(
                    resource_path("assets/plants/daisy/daisy_stage2/daisy-2-1.png")
                ).convert_alpha(),
                pygame.image.load(
                    resource_path("assets/plants/daisy/daisy_stage2/daisy-2-2.png")
                ).convert_alpha()
            ],
            3: [
                pygame.image.load(
                    resource_path("assets/plants/daisy/daisy_stage3/daisy-3-1.png")
                ).convert_alpha(),
                pygame.image.load(
                    resource_path("assets/plants/daisy/daisy_stage3/daisy-3-2.png")
                ).convert_alpha()
            ]
        },
        "Tulip": {
            "slot": pygame.image.load(
                resource_path("assets/plants/tulip/tulip_slotview/tulip_slotview.png")
            ).convert_alpha(),

            1: [
                pygame.image.load(
                    resource_path("assets/plants/tulip/tulip_stage1/tulip-1-1.png")
                ).convert_alpha(),

                pygame.image.load(
                    resource_path("assets/plants/tulip/tulip_stage1/tulip-1-2.png")
                ).convert_alpha()
            ],

            2: [
                pygame.image.load(
                    resource_path("assets/plants/tulip/tulip_stage2/tulip-2-1.png")
                ).convert_alpha(),

                pygame.image.load(
                    resource_path("assets/plants/tulip/tulip_stage2/tulip-2-2.png")
                ).convert_alpha()
            ],

            3: [
                pygame.image.load(
                    resource_path("assets/plants/tulip/tulip_stage3/tulip-3-1.png")
                ).convert_alpha(),

                pygame.image.load(
                    resource_path("assets/plants/tulip/tulip_stage3/tulip-3-2.png")
                ).convert_alpha()
            ]
        },
        "Sunflower": {
            "slot": pygame.image.load(
                resource_path("assets/plants/sunflower/sunflower_slotview/sunflower_slotview.png")
            ).convert_alpha(),

            1: [
                pygame.image.load(
                    resource_path("assets/plants/sunflower/sunflower_stage1/sunflower-1-1.png")
                ).convert_alpha(),

                pygame.image.load(
                    resource_path("assets/plants/sunflower/sunflower_stage1/sunflower-1-2.png")
                ).convert_alpha()
            ],

            2: [
                pygame.image.load(
                    resource_path("assets/plants/sunflower/sunflower_stage2/sunflower-2-1.png")
                ).convert_alpha(),

                pygame.image.load(
                    resource_path("assets/plants/sunflower/sunflower_stage2/sunflower-2-2.png")
                ).convert_alpha()
            ],

            3: [
                pygame.image.load(
                    resource_path("assets/plants/sunflower/sunflower_stage3/sunflower-3-1.png")
                ).convert_alpha(),

                pygame.image.load(
                    resource_path("assets/plants/sunflower/sunflower_stage3/sunflower-3-2.png")
                ).convert_alpha()
            ]
        },
        "Rose": {
            "slot": pygame.image.load(
                resource_path("assets/plants/rose/rose_slotview/rose_slotview.png")
            ).convert_alpha(),

            1: [
                pygame.image.load(
                    resource_path("assets/plants/rose/rose_stage1/rose-1-1.png")
                ).convert_alpha(),

                pygame.image.load(
                    resource_path("assets/plants/rose/rose_stage1/rose-1-2.png")
                ).convert_alpha()
            ],

            2: [
                pygame.image.load(
                    resource_path("assets/plants/rose/rose_stage2/rose-2-1.png")
                ).convert_alpha(),

                pygame.image.load(
                    resource_path("assets/plants/rose/rose_stage2/rose-2-2.png")
                ).convert_alpha()
            ],

            3: [
                pygame.image.load(
                    resource_path("assets/plants/rose/rose_stage3/rose-3-1.png")
                ).convert_alpha(),

                pygame.image.load(
                    resource_path("assets/plants/rose/rose_stage3/rose-3-2.png")
                ).convert_alpha()
            ]
        },
        "Lavender": {
            "slot": pygame.image.load(
                resource_path("assets/plants/lavender/lavender_slotview/lavender_slotview.png")
            ).convert_alpha(),

            1: [
                pygame.image.load(
                    resource_path("assets/plants/lavender/lavender_stage1/lavender-1-1.png")
                ).convert_alpha(),

                pygame.image.load(
                    resource_path("assets/plants/lavender/lavender_stage1/lavender-1-2.png")
                ).convert_alpha()
            ],

            2: [
                pygame.image.load(
                    resource_path("assets/plants/lavender/lavender_stage2/lavender-2-1.png")
                ).convert_alpha(),

                pygame.image.load(
                    resource_path("assets/plants/lavender/lavender_stage2/lavender-2-2.png")
                ).convert_alpha()
            ],

            3: [
                pygame.image.load(
                    resource_path("assets/plants/lavender/lavender_stage3/lavender-3-1.png")
                ).convert_alpha(),

                pygame.image.load(
                    resource_path("assets/plants/lavender/lavender_stage3/lavender-3-2.png")
                ).convert_alpha()
            ]
        },
        "Blue Orchid": {
            "slot": pygame.image.load(
                resource_path("assets/plants/blueorchid/blueorchid_slotview/blueorchid_slotview.png")
            ).convert_alpha(),

            1: [
                pygame.image.load(
                    resource_path("assets/plants/blueorchid/blueorchid_stage1/blueorchid-1-1.png")
                ).convert_alpha(),

                pygame.image.load(
                    resource_path("assets/plants/blueorchid/blueorchid_stage1/blueorchid-1-2.png")
                ).convert_alpha()
            ],

            2: [
                pygame.image.load(
                    resource_path("assets/plants/blueorchid/blueorchid_stage2/blueorchid-2-1.png")
                ).convert_alpha(),

                pygame.image.load(
                    resource_path("assets/plants/blueorchid/blueorchid_stage2/blueorchid-2-2.png")
                ).convert_alpha()
            ],

            3: [
                pygame.image.load(
                    resource_path("assets/plants/blueorchid/blueorchid_stage3/blueorchid-3-1.png")
                ).convert_alpha(),

                pygame.image.load(
                    resource_path("assets/plants/blueorchid/blueorchid_stage3/blueorchid-3-2.png")
                ).convert_alpha()
            ]
        },
        "Cherry Blossom": {
            "slot": pygame.image.load(
                resource_path("assets/plants/cherryblossom/cherryblossom_slotview/cherryblossom_slotview.png")
            ).convert_alpha(),

            1: [
                pygame.image.load(
                    resource_path("assets/plants/cherryblossom/cherryblossom_stage1/cherryblossom-1-1.png")
                ).convert_alpha(),

                pygame.image.load(
                    resource_path("assets/plants/cherryblossom/cherryblossom_stage1/cherryblossom-1-2.png")
                ).convert_alpha()
            ],

            2: [
                pygame.image.load(
                    resource_path("assets/plants/cherryblossom/cherryblossom_stage2/cherryblossom-2-1.png")
                ).convert_alpha(),

                pygame.image.load(
                    resource_path("assets/plants/cherryblossom/cherryblossom_stage2/cherryblossom-2-2.png")
                ).convert_alpha()
            ],

            3: [
                pygame.image.load(
                    resource_path("assets/plants/cherryblossom/cherryblossom_stage3/cherryblossom-3-1.png")
                ).convert_alpha(),

                pygame.image.load(
                    resource_path("assets/plants/cherryblossom/cherryblossom_stage3/cherryblossom-3-2.png")
                ).convert_alpha()
            ]
        },
        "Golden Lily": {
            "slot": pygame.image.load(
                resource_path("assets/plants/goldenlily/goldenlily_slotview/goldenlily-slotview.png")
            ).convert_alpha(),

            1: [
                pygame.image.load(
                    resource_path("assets/plants/goldenlily/goldenlily_stage1/goldenlily-1-1.png")
                ).convert_alpha(),

                pygame.image.load(
                    resource_path("assets/plants/goldenlily/goldenlily_stage1/goldenlily-1-2.png")
                ).convert_alpha()
            ],

            2: [
                pygame.image.load(
                    resource_path("assets/plants/goldenlily/goldenlily_stage2/goldenlily-2-1.png")
                ).convert_alpha(),

                pygame.image.load(
                    resource_path("assets/plants/goldenlily/goldenlily_stage2/goldenlily-2-2.png")
                ).convert_alpha()
            ],

            3: [
                pygame.image.load(
                    resource_path("assets/plants/goldenlily/goldenlily_stage3/goldenlily-3-1.png")
                ).convert_alpha(),

                pygame.image.load(
                    resource_path("assets/plants/goldenlily/goldenlily_stage3/goldenlily-3-2.png")
                ).convert_alpha()
            ]
        },
        "Moon Blossom": {
            "slot": pygame.image.load(
                resource_path("assets/plants/moonblossom/moonblossom_slotview/moonblossom-slotview.png")
            ).convert_alpha(),

            1: [
                pygame.image.load(
                    resource_path("assets/plants/moonblossom/moonblossom_stage1/moonblossom-1-1.png")
                ).convert_alpha(),

                pygame.image.load(
                    resource_path("assets/plants/moonblossom/moonblossom_stage1/moonblossom-1-2.png")
                ).convert_alpha()
            ],

            2: [
                pygame.image.load(
                    resource_path("assets/plants/moonblossom/moonblossom_stage2/moonblossom-2-1.png")
                ).convert_alpha(),

                pygame.image.load(
                    resource_path("assets/plants/moonblossom/moonblossom_stage2/moonblossom-2-2.png")
                ).convert_alpha()
            ],

            3: [
                pygame.image.load(
                    resource_path("assets/plants/moonblossom/moonblossom_stage3/moonblossom-3-1.png")
                ).convert_alpha(),

                pygame.image.load(
                    resource_path("assets/plants/moonblossom/moonblossom_stage3/moonblossom-3-2.png")
                ).convert_alpha()
            ]
        }
    }
    sounds = {
        "buy_sound": pygame.mixer.Sound(
            resource_path("assets/sounds/buy.ogg")
        ),
        "earn_sound": pygame.mixer.Sound(
            resource_path("assets/sounds/earn.ogg")
        ),
        "harvest_sound": pygame.mixer.Sound(
            resource_path("assets/sounds/harvest.ogg")
        ),
        "plant_sound": pygame.mixer.Sound(
            resource_path("assets/sounds/plant.ogg")
        ),
        "shovel_sound": pygame.mixer.Sound(
            resource_path("assets/sounds/shovel.ogg")
        ),
    }

    background_music = pygame.mixer.music.load(
        resource_path("assets/sounds/background_music.ogg")
    )

    shovel_image = pygame.image.load(
        resource_path("assets/buyables/objects/shovel.png")
    ).convert_alpha()
    shovel_image = pygame.transform.scale(
        shovel_image,
        (40, 40)
    )

    assets = {'grass_tiles':grass_tiles, 'water_frames': water_frames, 'shovel_image': shovel_image, 'plant_images': plant_images, 'sounds': sounds, 'background_tiles': background_tiles, 'boosted_tiles': boosted_tiles, 'background_music': background_music}

    return assets