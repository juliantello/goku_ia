import pygame
from algorithms.depthAlgorithm import DepthAlgorithm
from algorithms.amplitudeAlgorithm import AmplitudeAlgorithm
from algorithms.costAlgorithm import CostAlgorithm
from algorithms.avaraAlgorithm import AvaraAlgorithm
from algorithms.optimalAlgorithm import OptimalAlgorithm
import sys

BLACK = (0, 0, 0)
YELLOW = (255, 205, 104)
WHITE = (255, 255, 255)  # FREE 0

WIDTHCELL = 45
HEIGHTCELL = 45
MARGIN = 5

algorithm = None

class Interface:

    def __init__(self, initWorld):
        self.__initWorld = initWorld
        self.__solutionWorlds = None
        self.__imgGoku = None
        self.__imgWall = None
        self.__imgFreezer = None
        self.__imgBall = None
        self.__imgCell = None
        self.__imgSeed = None

    def setSolutionWorld(self, newSolutionWorlds):
        self.__solutionWorlds = newSolutionWorlds

    def loadImages(self):
        self.__imgGoku = pygame.image.load("img/goku.png").convert()
        self.__imgWall = pygame.image.load("img/muro.png").convert()
        self.__imgFreezer = pygame.image.load("img/freezer.png").convert()
        self.__imgBall = pygame.image.load("img/esfera.png").convert()
        self.__imgCell = pygame.image.load("img/cell.png").convert()
        self.__imgSeed = pygame.image.load("img/semilla.png").convert()

    def showText(self, pantalla, fuente, texto, color, dimensiones, x, y):
        tipo_letra = pygame.font.Font(fuente, dimensiones)
        superficie = tipo_letra.render(texto, True, color)
        rectangulo = superficie.get_rect()
        rectangulo.center = (x, y)
        pantalla.blit(superficie, rectangulo)

    def showComputingTime(self, screen, algorithm):
        computingTime = algorithm.getComputingTime()
        self.showText(screen, pygame.font.match_font(
            'arial'), computingTime, WHITE, 35, 655, 230)

    def drawWorld(self, grid, screen):
        for i in range(10):
                for j in range(10):
                    if (grid[i, j] == 0):
                        color = WHITE
                        pygame.draw.rect(screen, color, [(MARGIN+WIDTHCELL) * j + MARGIN,
                                                         (MARGIN+HEIGHTCELL) * i + MARGIN,
                                                         WIDTHCELL, HEIGHTCELL])
                    if grid[i, j] == 1:
                        imagen_redimensionada = pygame.transform.scale(self.__imgWall, (45, 45))
                        screen.blit(imagen_redimensionada, [(MARGIN+WIDTHCELL) * j + MARGIN,
                                                            (MARGIN+HEIGHTCELL) * i + MARGIN,
                                                            WIDTHCELL, HEIGHTCELL])
                    if grid[i, j] == 2:
                        imagen_redimensionada = pygame.transform.scale(self.__imgGoku, (45, 45))
                        screen.blit(imagen_redimensionada, [(MARGIN+WIDTHCELL) * j + MARGIN,
                                                            (MARGIN+HEIGHTCELL) * i + MARGIN,
                                                            WIDTHCELL, HEIGHTCELL])
                    if grid[i, j] == 3:
                        imagen_redimensionada = pygame.transform.scale(self.__imgFreezer, (45, 45))
                        screen.blit(imagen_redimensionada, [(MARGIN+WIDTHCELL) * j + MARGIN,
                                                            (MARGIN+HEIGHTCELL) * i + MARGIN,
                                                            WIDTHCELL, HEIGHTCELL])
                    if grid[i, j] == 4:
                        imagen_redimensionada = pygame.transform.scale(self.__imgCell, (45, 45))
                        screen.blit(imagen_redimensionada, [(MARGIN+WIDTHCELL) * j + MARGIN,
                                                            (MARGIN+HEIGHTCELL) * i + MARGIN,
                                                            WIDTHCELL, HEIGHTCELL])
                    if grid[i, j] == 5:
                        imagen_redimensionada = pygame.transform.scale(self.__imgSeed, (45, 45))
                        screen.blit(imagen_redimensionada, [(MARGIN+WIDTHCELL) * j + MARGIN,
                                                            (MARGIN+HEIGHTCELL) * i + MARGIN,
                                                            WIDTHCELL, HEIGHTCELL])
                    if grid[i, j] == 6:
                        imagen_redimensionada = pygame.transform.scale( self.__imgBall, (45, 45))
                        screen.blit(imagen_redimensionada, [(MARGIN+WIDTHCELL) * j + MARGIN,
                                                            (MARGIN+HEIGHTCELL) * i + MARGIN,
                                                            WIDTHCELL, HEIGHTCELL])

    def interfaceSolution(self, press, grid, w, screen, clock):
        while not press:
            # prueba para boton
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # draw the grid
            self.drawWorld(grid, screen)

         # limit to 1 frames per second.
            clock.tick(1)

        # check that the length is not exceeded
            if (not (w >= len(self.__solutionWorlds))):
                # update world
                grid = self.__solutionWorlds[w]
                w += 1
            elif (w == len(self.__solutionWorlds)):
                sonido_fondo = pygame.mixer.Sound("music/dragon-ball.mp3")
                pygame.mixer.Sound.play(sonido_fondo)
                w += 1
                press = True

        # advance and update the screen with what we have drawn.
            pygame.display.flip()

        # Close
        # pygame.quit()

    def showInterface(self):
        # Initialize pygame
        pygame.init()

        # music
        pygame.mixer.init()

        # Set the length and width of the screen
        WINDOW_DIMENSION = [510, 510]  # 510,510
        screen = pygame.display.set_mode(WINDOW_DIMENSION)

        # iterate until the user presses the exit button.
        press = False

        # use it to set how fast the screen refreshes.
        clock = pygame.time.Clock()

        w = 1
        self.loadImages()
        #grid = self.__solutionWorlds[0]
        grid = self.__initWorld

        # Set the screen background.
        screen.fill(BLACK)

        pygame.display.set_caption("Goku smart")

        self.drawWorld(grid, screen)
        
        intro = True

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                try:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            print("Alg. Profundidad ejecutado")
                            screen.fill(BLACK)
                            # Set the title of the screen.
                            pygame.display.set_caption("Goku smart profundidad")
                            self.showText(screen, pygame.font.match_font(
                                'arial'), "Profundidad", YELLOW, 35, 655, 50)
                            
                            num_balls = 0
                            for i in range(10):
                                for j in range(10):
                                    if grid[i, j] == 6:
                                        num_balls += 1

                            nodeExpanded = 0
                            depth = 0
                            cost = 0
                            for i in range(num_balls):       
                                algorithm = DepthAlgorithm(grid)
                                solution = algorithm.start()
                                solutionWorld = solution[0]
                                nodeExpanded += solution[1]
                                depth += solution[2]
                                cost += solution[3]
                                self.setSolutionWorld(solutionWorld)
                                self.interfaceSolution(press, grid, w, screen, clock)
                                grid = solutionWorld[len(solutionWorld)-1]
                            grid = self.__initWorld

                            self.showComputingTime(screen, algorithm)
                            self.showText(screen, pygame.font.match_font(
                                'arial'), str(nodeExpanded), WHITE, 35, 655, 295)
                            self.showText(screen, pygame.font.match_font(
                                'arial'), str(depth), WHITE, 35, 655, 355)
                            
                            print("Nodos expandidos: ", nodeExpanded)  # Good
                            print("Profundidad: ", depth)
                            print("Costo solución: ", cost)
                        elif event.key == pygame.K_c:
                            print("Alg. Costo Uniforme ejecutado")
                            screen.fill(BLACK)
                            # Set the title of the screen.
                            pygame.display.set_caption("Goku smart costo")
                            self.showText(screen, pygame.font.match_font(
                                'arial'), "Costo", YELLOW, 35, 655, 80)
                            
                            num_balls = 0
                            for i in range(10):
                                for j in range(10):
                                    if grid[i, j] == 6:
                                        num_balls += 1

                            nodeExpanded = 0
                            depth = 0
                            cost = 0
                            for i in range(num_balls):     
                                algorithm = CostAlgorithm(grid)
                                solution = algorithm.start()
                                solutionWorld = solution[0]
                                nodeExpanded += solution[1]
                                depth += solution[2]
                                cost += solution[3]
                                self.setSolutionWorld(solutionWorld)
                                self.interfaceSolution(press, grid, w, screen, clock)
                                grid = solutionWorld[len(solutionWorld)-1]
                            grid = self.__initWorld    
                            
                            self.showComputingTime(screen, algorithm)
                            self.showText(screen, pygame.font.match_font(
                                'arial'), str(nodeExpanded), WHITE, 35, 655, 295)
                            self.showText(screen, pygame.font.match_font(
                                'arial'), str(depth), WHITE, 35, 655, 355)
                            
                            print("Nodos expandidos: ", nodeExpanded)  # Good
                            print("Profundidad: ", depth)
                            print("Costo solución: ", cost)
                        elif event.key == pygame.K_a:
                            print("Alg. Amplitud ejecutado")
                            screen.fill(BLACK)
                            # Set the title of the screen.
                            pygame.display.set_caption("Goku smart amplitud")
                            self.showText(screen, pygame.font.match_font(
                                'arial'), "Amplitud", YELLOW, 35, 655, 20)
                            
                            num_balls = 0
                            for i in range(10):
                                for j in range(10):
                                    if grid[i, j] == 6:
                                        num_balls += 1

                            nodeExpanded = 0
                            depth = 0
                            cost = 0
                            for i in range(num_balls):      
                                algorithm = AmplitudeAlgorithm(grid)
                                solution = algorithm.start()
                                solutionWorld = solution[0]
                                nodeExpanded += solution[1]
                                depth += solution[2]
                                cost += solution[3]
                                self.setSolutionWorld(solutionWorld)
                                self.interfaceSolution(press, grid, w, screen, clock)
                                grid = solutionWorld[len(solutionWorld)-1]
                            grid = self.__initWorld   

                            self.showComputingTime(screen, algorithm)
                            self.showText(screen, pygame.font.match_font(
                                'arial'), str(nodeExpanded), WHITE, 35, 655, 295)
                            self.showText(screen, pygame.font.match_font(
                                'arial'), str(depth), WHITE, 35, 655, 355)
                            
                            print("Nodos expandidos: ", nodeExpanded)  # Good
                            print("Profundidad: ", depth)
                            print("Costo solución: ", cost)
                        elif event.key == pygame.K_v:
                            print("Alg. Avara")
                            screen.fill(BLACK)
                            # Set the title of the screen.
                            pygame.display.set_caption("Goku smart avara")
                            self.showText(screen, pygame.font.match_font(
                                'arial'), "Avara", YELLOW, 35, 655, 20)
                            
                            num_balls = 0
                            for i in range(10):
                                for j in range(10):
                                    if grid[i, j] == 6:
                                        num_balls += 1

                            nodeExpanded = 0
                            depth = 0
                            cost = 0
                            for i in range(num_balls):      
                                algorithm = AvaraAlgorithm(grid)
                                solution = algorithm.start()
                                solutionWorld = solution[0]
                                nodeExpanded += solution[1]
                                depth += solution[2]
                                cost += solution[3]
                                self.setSolutionWorld(solutionWorld)
                                self.interfaceSolution(press, grid, w, screen, clock)
                                grid = solutionWorld[len(solutionWorld)-1]
                            grid = self.__initWorld   

                            self.showComputingTime(screen, algorithm)
                            self.showText(screen, pygame.font.match_font(
                                'arial'), str(nodeExpanded), WHITE, 35, 655, 295)
                            self.showText(screen, pygame.font.match_font(
                                'arial'), str(depth), WHITE, 35, 655, 355)
                            
                            print("Nodos expandidos: ", nodeExpanded)  # Good
                            print("Profundidad: ", depth)
                            print("Costo solución: ", cost)
                        elif event.key == pygame.K_o:
                            print("Alg. A*")
                            screen.fill(BLACK)
                            # Set the title of the screen.
                            pygame.display.set_caption("Goku smart A*")               
                            self.showText(screen, pygame.font.match_font(
                                'arial'), "A*", YELLOW, 35, 655, 140)
                            
                            num_balls = 0
                            for i in range(10):
                                for j in range(10):
                                    if grid[i, j] == 6:
                                        num_balls += 1

                            nodeExpanded = 0
                            depth = 0
                            cost = 0
                            for i in range(num_balls):      
                                algorithm = OptimalAlgorithm(grid)
                                solution = algorithm.start()
                                solutionWorld = solution[0]
                                nodeExpanded += solution[1]
                                depth += solution[2]
                                cost += solution[3]
                                self.setSolutionWorld(solutionWorld)
                                self.interfaceSolution(press, grid, w, screen, clock)
                                grid = solutionWorld[len(solutionWorld)-1]
                            grid = self.__initWorld   

                            self.showComputingTime(screen, algorithm)
                            self.showText(screen, pygame.font.match_font(
                                'arial'), str(nodeExpanded), WHITE, 35, 655, 295)
                            self.showText(screen, pygame.font.match_font(
                                'arial'), str(depth), WHITE, 35, 655, 355)
                            
                            print("Nodos expandidos: ", nodeExpanded)  # Good
                            print("Profundidad: ", depth)
                            print("Costo solución: ", cost)
                except:
                    print("END")  

            pygame.display.flip()
