import pygame

class Background(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        # load images
        self.crossroad_bg = pygame.image.load("map_img/Crossroad_1.png").convert_alpha()
        self.road_x1_bg = pygame.image.load("map_img/Road_X1.1.png").convert_alpha()
        self.road_x2_bg = pygame.image.load("map_img/Road_X1.2.png").convert_alpha()
        self.road_house_bg = pygame.image.load("map_img/Road_House.png").convert_alpha()
        self.road_y1_bg = pygame.image.load("map_img/Road_Y1.png").convert_alpha()
        self.road_y2_bg = pygame.image.load("map_img/Road_Y1.2.png").convert_alpha()
        self.house_bg = pygame.image.load("map_img/House.png").convert_alpha()
        self.home_bg = pygame.image.load("map_img/Home.png").convert_alpha()
        self.wall_bg = pygame.image.load("map_img/housewall.png").convert_alpha()
        self.sand_bg = pygame.image.load("map_img/sand.png").convert_alpha()


        # scale
        self.crossroad_bg = pygame.transform.scale(self.crossroad_bg, (800, 600))
        self.road_x1_bg = pygame.transform.scale(self.road_x1_bg, (800, 600))
        self.road_x2_bg = pygame.transform.scale(self.road_x2_bg, (800, 600))
        self.road_house_bg = pygame.transform.scale(self.road_house_bg, (800, 600))
        self.road_y1_bg = pygame.transform.scale(self.road_y1_bg, (800, 600))
        self.road_y2_bg = pygame.transform.scale(self.road_y2_bg, (800, 600))
        self.house_bg = pygame.transform.scale(self.house_bg, (800, 600))
        self.home_bg = pygame.transform.scale(self.home_bg, (800, 600))
        self.wall_bg = pygame.transform.scale(self.wall_bg, (800, 600))
        self.sand_bg = pygame.transform.scale(self.sand_bg, (800, 600))

        # default background
        self.background = self.home_bg
        self.image = self.home_bg

        # maps
        self.wall_bg1 = self.wall_bg.copy()
        self.wall_bg2 = self.wall_bg.copy()

        self.sand_bg1 = self.sand_bg.copy()
        self.sand_bg2 = self.sand_bg.copy()
        self.sand_bg3 = self.sand_bg.copy()
        self.sand_bg4 = self.sand_bg.copy()

        self.map_xr = [[self.wall_bg1, self.road_house_bg, self.wall_bg2],
                       [self.sand_bg1, self.road_y1_bg, self.sand_bg2],
                       [self.road_x1_bg, self.crossroad_bg, self.road_x2_bg],
                       [self.sand_bg3, self.road_y2_bg, self.sand_bg4]]
        self.map_xl = [[self.wall_bg2, self.road_house_bg, self.wall_bg1],
                       [self.sand_bg2, self.road_y1_bg, self.sand_bg1],
                       [self.road_x2_bg, self.crossroad_bg, self.road_x1_bg],
                       [self.sand_bg4, self.road_y2_bg, self.sand_bg3]]
        self.map_yu = [[self.sand_bg3, self.road_x1_bg, self.sand_bg1, self.wall_bg1],
                       [self.road_y2_bg, self.crossroad_bg, self.road_y1_bg, self.road_house_bg, self.home_bg],
                       [self.sand_bg4,self.road_x2_bg, self.sand_bg2, self.wall_bg2]]
        self.map_yd = [[self.wall_bg1, self.sand_bg1, self.road_x1_bg, self.sand_bg3],
                       [self.home_bg,self.road_house_bg, self.road_y1_bg, self.crossroad_bg, self.road_y2_bg],
                       [self.wall_bg2, self.sand_bg2, self.road_x2_bg, self.sand_bg4]]

        self.special_transitions = {
            self.home_bg: [
                {
                    "label": "house_door",
                    "rect": pygame.Rect(350, 550, 100, 50),  # door area
                    "target_bg": self.road_house_bg,
                    "target_pos": (400, 250),  # where player should appear
                }
            ],
            self.road_house_bg: [
                {
                    "label": "house_door",
                    "rect": pygame.Rect(350, 150, 100, 50),  # door area
                    "target_bg": self.home_bg,
                    "target_pos": (400, 550),  # where player should appear
                }
            ]
            
        }

        #Wall and boarder
        self.borders_by_bg = {
            self.home_bg: [
                pygame.Rect(0, 0, 800, 100),     # top wall
                pygame.Rect(0, 0, 50, 600),      # left wall
                pygame.Rect(750, 0, 50, 600),    # right wall
                pygame.Rect(0, 550, 300, 50),    # bottom-left wall
                pygame.Rect(500, 550, 300, 50),  # bottom-right wall
            ],
            self.road_house_bg: [
                pygame.Rect(0, 0, 330, 200), 
                pygame.Rect(470, 0, 800, 200),
            ],
            self.wall_bg1: [
                pygame.Rect(0, 0, 800, 200)
            ],
            self.wall_bg2: [
                pygame.Rect(0, 0, 800, 200)
            ]
}

    #trigger zones per background
        # Each entry is (label, rect)
        self.zones_by_bg = {
            self.crossroad_bg: [
                ("crossroad_zone1", pygame.Rect(0, -10, 800, 10)), # top edge
                ("crossroad_zone2", pygame.Rect(810, 0, 800, 600)), # right 
                ("crossroad_zone3", pygame.Rect(-10, 0, 10, 600)), # left
                ("crossroad_zone4", pygame.Rect(0, 600, 800, 610)), # bottm
            ],
            self.road_x1_bg: [
                ("road_x1_zone1", pygame.Rect(810, 0, 800, 600)), # right 
                ("road_x1_zone2", pygame.Rect(0, -10, 800, 10)), # top
                ("road_x1_zone3", pygame.Rect(0, 600, 800, 610)), # bottm
            ],
            self.road_x2_bg: [
                ("road_x2_zone1", pygame.Rect(-10, 0, 10, 600)), # left
                ("road_x2_zone2", pygame.Rect(0, -10, 800, 10)),  # top
                ("road_x2_zone3", pygame.Rect(0, 600, 800, 610)) # bottom
            ],
            self.road_y1_bg: [
                ("road_y1_zone1", pygame.Rect(0, -10, 800, 10)), # top
                ("road_y1_zone2", pygame.Rect(-10, 0, 10, 600)), # left
                ("road_y1_zone3", pygame.Rect(810, 0, 800, 600)), # right
                ("road_y1_zone4", pygame.Rect(0, 600, 800, 610)) # bottom
            ],
            self.road_y2_bg: [
                ("road_y2_zone1", pygame.Rect(0, -10, 800, 10)), # top
                ("road_y2_zone2", pygame.Rect(-10, 0, 10, 600)), # left
                ("road_y2_zone3", pygame.Rect(810, 0, 800, 600)) # right 
            ],
            self.sand_bg1: [
                ("sand1_zone1", pygame.Rect(810, 0, 800, 600)), # right 
                ("sand1_zone2", pygame.Rect(0, -10, 800, 10)), # top
                ("sand1_zone3", pygame.Rect(0, 600, 800, 610)), # bottm
            ],
            self.sand_bg2: [
                ("sand2_zone1", pygame.Rect(-10, 0, 10, 600)), # left
                ("sand2_zone2", pygame.Rect(0, -10, 800, 10)), # top
                ("sand2_zone3", pygame.Rect(0, 600, 800, 610)), # bottm
            ],
            self.sand_bg3: [
                ("sand3_zone1", pygame.Rect(810, 0, 800, 600)), # right 
                ("sand3_zone2", pygame.Rect(0, -10, 800, 10)), # top
            ],
            self.sand_bg4: [
                ("sand4_zone1", pygame.Rect(-10, 0, 10, 600)), # left
                ("sand4_zone2", pygame.Rect(0, -10, 800, 10)), # top
            ],
            self.home_bg: [
                ("bed_zone", pygame.Rect(600, 200, 80, 60))  
            ]
            

            
        }



    def trans_L(self):
        try:
            for row in self.map_xl:              # loop row
                for i in range(len(row)):        # loop column
                    if self.background == row[i]:
                        if i + 1 < len(row):     # check bounds
                            self.background = row[i + 1]
                            self.update_img()
                            return True
            return False
        except IndexError:
            return False

    def trans_R(self):
        try:
            for row in self.map_xr:
                for i in range(len(row)):
                    if self.background == row[i]:
                        if i + 1 < len(row):
                            self.background = row[i + 1]
                            self.update_img()
                            return True
            return False
        except IndexError:
            return False

    def trans_U(self):
        try:
            for row in self.map_yu:
                for i in range(len(row)):
                    if self.background == row[i]:
                        if i + 1 < len(row):
                            self.background = row[i + 1]
                            self.update_img()
                            return True
            return False
        except IndexError:
            return False

    def trans_D(self):
        try:
            for row in self.map_yd:
                for i in range(len(row)):
                    if self.background == row[i]:
                        if i + 1 < len(row):
                            self.background = row[i + 1]
                            self.update_img()
                            return True
            return False
        except IndexError:
            return False


    def update_img(self):
        self.image = self.background

    def check_bg(self):
        return self.background

    def get_zones(self):
        return self.zones_by_bg.get(self.background, [])
    
    def get_special_transitions(self):
        return self.special_transitions.get(self.background, [])

    def get_borders(self):
        return self.borders_by_bg.get(self.background, [])


