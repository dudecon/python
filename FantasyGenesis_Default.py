# A Fantasy Genesis roller

# The Lists:
# Anima
Anim_1_Sea_Life = ["Mollusk",
                   "Crab, Lobster",
                   "Squid, Mudskipper",
                   "Fish: Deep sea",
                   "Jellyfish",
                   "Fish: Fresh water",
                   "Whale, Dolphin",
                   "Shell",
                   "Eel, Leech",
                   "Coral, Anemone",
                   "Shark, ray"]

Anim_2_Insect = ["Worm",
                 "Ant",
                 "Mosquito",
                 "Moth, Butterfly",
                 "Fly, dragonfly",
                 "Lotus, Mantis",
                 "Bee, Wasp",
                 "Caterpillar",
                 "Beetle, Scarab",
                 "Flea, Mite",
                 "Spider"]

Anim_3_Mammal = ["Sheep, cow",
                 "Mouse, Rabbit",
                 "Pig, Boar",
                 "Deer, Pronghorn",
                 "Ram, Bull, Buck",
                 "Elephant, Giraffe"]

Anim_4_Reptile = ["Crocodile, Gila",
                  "Frog, Newt",
                  "Lizard, Snake",
                  "Turtle"]

Anim_5_Bird = ["Wild Fowl, Duck",
               "Farm Fowl, Rooster",
               "Seabird, Penguin",
               "City bird: Raven, Sparrow",
               "Tropical bird: Parrot, Heron",
               "Bird of Prey: Hawk, Owl"]

Anim_6_Mammal = ["Bat",
                 "Bear",
                 "Lupine: Wild Dog",
                 "Horse, Zeebra",
                 "Feline: Wild Cat",
                 "Primate"]

Anima = [Anim_1_Sea_Life,
        Anim_2_Insect,
        Anim_3_Mammal,
        Anim_4_Reptile,
        Anim_5_Bird,
        Anim_6_Mammal]

# Veggie

Vegi_1_Plant = ["Seaweed",
                "Fern",
                "Desert Cacti",
                "Thick Leaf Plant, Jade",
                "Flower: Domestic",
                "Vine",
                "Poppy",
                "Grass, Dandelion",
                "Bamboo",
                "Flower: Wild",
                "Carnivorous Plant"]

Vegi_2_Fruit_Vegi = ["Asparagus",
                     "Pinecone",
                     "Berry, Grapes",
                     "Ginger",
                     "Tree fruit (apple, orange)",
                     "Bean",
                     "Pumpkin, Gourd",
                     "Broccoli, Artichoke",
                     "Corn",
                     "Grain, Wheat",
                     "Pineapple"]

Vegi_3_Fungi = ["Moss",
                "Slime Fungi: Ooze, Jelly",
                "Lichen",
                "Mushroom"]

Vegi_4_Tree = ["Willow",
               "Birch",
               "Maple, Oak",
               "Banyan",
               "Pine",
               "Palm"]

Veggie = [Vegi_1_Plant,
          Vegi_2_Fruit_Vegi,
          Vegi_3_Fungi,
          Vegi_4_Tree]

# Elemental & Mineral

Elem_1_Fire_Electric = ["Fire, Vapor",
                        "Electric Bolt",
                        "Ember, Hot Coal",
                        "Molten Lava"]

Elem_2_Liquid = ["Icicles",
                 "Fog, Vapor",
                 "Wave",
                 "Dew Drops",
                 "Ripple",
                 "Frost, Snow",
                 "Suds, Bubbles",
                 "Tar, Gum"]

Elem_3_Earth_Metal = ["Malachite",
                      "Mountain, Cliff Face",
                      "Brick, Cobblestone",
                      "Rust, Oxide",
                      "Cracked Clay",
                      "Stalactite, Stalagmite",
                      "Glass, Crystals",
                      "Powder, Sand",
                      "Slate, Shale",
                      "Cement, Sediment",
                      "Mercury, Chrome"]

Elem_4_Astral_Atmosphere = ["Moon Cycles",
                            "Starfield",
                            "Crater, Asteroid",
                            "Solar Flare",
                            "Galaxy form",
                            "Volcano",
                            "Planets, Saturn's Rings",
                            "Cloud, Cyclone"]

EleMineral = [Elem_1_Fire_Electric,
              Elem_2_Liquid,
              Elem_3_Earth_Metal,
              Elem_4_Astral_Atmosphere]

Tech_1_Transportation = ["Car, Truck, Bus",
                         "Aircraft",
                         "Rail, Train, Trolley",
                         "Cycle (motor or bi)",
                         "Sled, Ski",
                         "Boat, Ship",
                         "Spacecraft",
                         "Tank Tread"]

Tech_2_Architecture = ["Ornament, Gargoyle",
                       "Bridge, Framework",
                       "Castle, Dome",
                       "Ornament, Pillar",
                       "Modern Skyscraper",
                       "Place of Worship, Totem",
                       "Doorway, Archway",
                       "Old Village, Cottage"]

Tech_3_Tool = ["Drill",
               "Cup, Plate",
               "Umbrella",
               "Bundle, Bale",
               "Hammer, Axe",
               "Brush: Hair, Tooth",
               "Razor, Knife",
               "Spigot, Faucet",
               "Rope",
               "Silverware",
               "Lock, Key"]

Tech_4_Machine = ["Switch, Dial, Button",
                  "Turbine",
                  "Bulb, Lamp",
                  "Clock, Gears",
                  "Fan, Propeller",
                  "Saw"]

Tech_5_Tool = ["Adhesive, Bandage",
               "Shovel, Pick",
               "Capsule, Tablet",
               "Nuts, Bolts",
               "Chain",
               "Thread, Stitch",
               "Shears, Scissors",
               "Pen, Paintbrush",
               "Spring, Coil",
               "Syringe",
               "Tube, Plumbing"]

Tech_6_Machine = ["Reactor Core",
                  "Telephone",
                  "Solar Panel",
                  "Engine",
                  "Laser Beam",
                  "Microchip",
                  "Dish Antenna",
                  "Rocket"]

Techne = [Tech_1_Transportation,
          Tech_2_Architecture,
          Tech_3_Tool,
          Tech_4_Machine,
          Tech_5_Tool,
          Tech_6_Machine]

All = [Anima, Veggie, EleMineral, Techne]

from random import choice

def RecurseChoice(Root):
    if isinstance(Root,str):
        print(Root)
    else:
        Sub_Root = choice(Root)
        RecurseChoice(Sub_Root)

#Choose one from each category
for i in All:
    RecurseChoice(i)
