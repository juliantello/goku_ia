from ctypes import sizeof
import sys
from tkinter import N
from turtledemo import clock
import pygame
from pygame.locals import *
from node import Node

class Main:

    def __init__(self):

        pygame.init()

        ### se carga las propiedades de la ventana y las imagenes

        self.frame = pygame.display.set_mode((500, 500))

        pygame.display.set_caption("Smart Goku")
        
        self.CELL_SIZE = 50
        self.MARGIN = 0

        self.white = pygame.image.load("img/white.png")
        self.white = pygame.transform.scale(self.white, (self.CELL_SIZE, self.CELL_SIZE))
        self.imgMuro = pygame.image.load("img/muro.png")
        self.imgMuro = pygame.transform.scale(self.imgMuro, (self.CELL_SIZE, self.CELL_SIZE))
        self.imgGoku = pygame.image.load("img/goku.png")
        self.imgGoku = pygame.transform.scale(self.imgGoku, (self.CELL_SIZE, self.CELL_SIZE))
        self.imgFreezer = pygame.image.load("img/freezer.png")
        self.imgFreezer = pygame.transform.scale(self.imgFreezer, (self.CELL_SIZE, self.CELL_SIZE))
        self.imgCell = pygame.image.load("img/cell.png")
        self.imgCell = pygame.transform.scale(self.imgCell, (self.CELL_SIZE, self.CELL_SIZE))
        self.imgSemilla = pygame.image.load("img/semilla.png")
        self.imgSemilla = pygame.transform.scale(self.imgSemilla, (self.CELL_SIZE, self.CELL_SIZE))
        self.imgEsfera = pygame.image.load("img/esfera.png")
        self.imgEsfera = pygame.transform.scale(self.imgEsfera, (self.CELL_SIZE, self.CELL_SIZE))

        ### se abre el archivo txt y se lo carga en una matrix

        file = open("file.txt", "r")
        self.data = []
        for index, line in enumerate(file.readlines()):
            self.data.append([int(s) for s in line.split() if s.isdigit()])

        ### variables que nos ayudan a hacer el recorrido de las esferas

        self.expanded_nodes = []
        self.goal_position = [] #positions the goals
        self.goals = 0 #goals totals in world
        self.goals_adquired = {}

        # print(self.data)
        self.get_initial_positions()
        self.game_intro()

    def draw_matrix(self):
        matrix = self.data
        for i in range(10):
            for j in range(10):
                if matrix[i][j] == 1:
                    image = self.imgMuro
                elif matrix[i][j] == 2:
                    image = self.imgGoku
                elif matrix[i][j] == 3:
                    image = self.imgFreezer
                elif matrix[i][j] == 4:
                    image = self.imgCell
                elif matrix[i][j] == 5:
                    image = self.imgSemilla
                elif matrix[i][j] == 6:
                    image = self.imgEsfera
                else:
                    image = self.white
                rect = pygame.Rect(j * (self.CELL_SIZE + self.MARGIN) + self.MARGIN, i * (self.CELL_SIZE + self.MARGIN) + self.MARGIN, self.CELL_SIZE, self.CELL_SIZE)
                self.frame.blit(image, rect)

    def game_intro(self):
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
                            self.profundidad()
                        elif event.key == pygame.K_c:
                            print("Alg. Costo Uniforme ejecutado")
                            self.costoUniforme()
                        elif event.key == pygame.K_a:
                            print("Alg. Amplitud ejecutado")
                            self.amplitud()
                        elif event.key == pygame.K_v:
                            print("Alg. Avara ejecutado")
                            self.avara()    
                except:
                    print("end")    
                    

            self.frame.fill((0, 0, 0))
            self.draw_matrix()
            pygame.display.update()

    def get_initial_positions(self):
        for i in range(10):
            for j in range(10):
                if self.data[i][j] == 2:
                    self.robot_position = (i, j) 
                if self.data[i][j] == 6: # inicializo variables con las posiciones de las metas
                    self.goal_position.append((i, j)) 
                    for position in self.goal_position:
                        self.goals_adquired[str(position)] = False
                    self.goals += 1

    def costoUniforme(self):
        nodes = []
        initial_node = Node(self.robot_position, None)
        nodes.append(initial_node)
        solucionado = False
        
        while not solucionado and len(nodes) != 0:
            
            bandera = False
            """ valida si estamos en un nodo meta y ya pasamos por el otro... de la forma como esta solo funciona con dos metas"""
            if (nodes[0].position == self.goal_position[0] and self.goal_position[1] in nodes[0].get_fathers_positions()):
                bandera = True
            if (nodes[0].position == self.goal_position[1] and self.goal_position[0] in nodes[0].get_fathers_positions()):
                bandera = True
            
            if  bandera: 
                solucionado = True
                #print(self.goals_adquired,"father positions", n.get_fathers_positions())
                return self.show_route(nodes[0].get_fathers())
            
            else:
                self.expanded_nodes.append(nodes[0])
                if (nodes[0].can_move(self.data, 'right')):
                    nodes.append(nodes[0].make_child_node_with_weight('right',self.data))
                if (nodes[0].can_move(self.data, 'up')):
                    nodes.append(nodes[0].make_child_node_with_weight('up',self.data))
                if (nodes[0].can_move(self.data, 'left')):
                    nodes.append(nodes[0].make_child_node_with_weight('left',self.data))
                if (nodes[0].can_move(self.data, 'down')):
                    nodes.append(nodes[0].make_child_node_with_weight('down',self.data))
            nodes.pop(0)
            nodes.sort(key=lambda x: x.weight)
    
    def profundidad(self):
        nodes = []
        initial_node = Node(self.robot_position, None)
        #expanded_nodes = []
        nodes.append(initial_node) #Frontera nodes
        solucionado = False
        goals_adquired = 0
        while not solucionado and len(nodes) != 0:
            
            bandera = False
            """ valida si estamos en un nodo meta y ya pasamos por el otro... de la forma como esta solo funciona con dos metas"""
            if (nodes[0].position == self.goal_position[0] and self.goal_position[1] in nodes[0].get_fathers_positions()):
                bandera = True
            if (nodes[0].position == self.goal_position[1] and self.goal_position[0] in nodes[0].get_fathers_positions()):
                bandera = True
            self.expanded_nodes.append(nodes[0])
            if  bandera: 
                solucionado = True
                #print(self.goals_adquired,"father positions", n.get_fathers_positions())
                return self.show_route(nodes[0].get_fathers())
            else:
                if (nodes[0].can_move(self.data, 'right')):
                    node_child_r = nodes[0].make_child_node('right')
                    if not node_child_r in nodes[0].get_fathers_positions():
                        nodes.append(node_child_r)

                if (nodes[0].can_move(self.data, 'up')):
                    node_child_u = nodes[0].make_child_node('up')
                    if not node_child_u in nodes[0].get_fathers_positions():
                        nodes.append(node_child_u)

                if (nodes[0].can_move(self.data, 'left')):
                    node_child_l = nodes[0].make_child_node('left')
                    if not node_child_l in nodes[0].get_fathers_positions():
                        nodes.append(node_child_l)

                if (nodes[0].can_move(self.data, 'down')):
                    node_child_d = nodes[0].make_child_node('down')   
                    if not node_child_d in nodes[0].get_fathers_positions():
                        nodes.append(node_child_d)
            nodes.pop(0)

    def amplitud(self):
        nodes = []
        initial_node = Node(self.robot_position,None)
        nodes.append(initial_node)
        solucionado = False
        goals_adquired = 0
        while not solucionado:
            if not nodes:
                raise AttributeError #Fallo
            n = nodes.pop(0)
            bandera = False
            """ valida si estamos en un nodo meta y ya pasamos por el otro... de la forma como esta solo funciona con dos metas"""
            if( n.position == self.goal_position[0] and self.goal_position[1] in n.get_fathers_positions()  ):
                bandera = True
            if( n.position == self.goal_position[1] and self.goal_position[0] in n.get_fathers_positions()  ):
                bandera = True

            if  bandera: 
                solucionado = True
                #print(self.goals_adquired,"father positions", n.get_fathers_positions())
                return self.show_route(n.get_fathers())
            else:
                self.expanded_nodes.append(n)
                if (n.can_move(self.data, 'right')):
                    nodes.append(n.make_child_node('right'))
                if (n.can_move(self.data, 'up')):
                    nodes.append(n.make_child_node('up'))
                if (n.can_move(self.data, 'left')):
                    nodes.append(n.make_child_node('left'))
                if (n.can_move(self.data, 'down')):
                    nodes.append(n.make_child_node('down'))
    
    def avara(self):
        nodes = []
        initial_node = Node(self.robot_position, None)
        nodes.append(initial_node)
        solucionado = False

        while not solucionado:
            if not nodes:
                raise AttributeError  # Fallo
            n = nodes.pop(0)
            bandera = False
            """ valida si estamos en un nodo meta y ya pasamos por el otro... de la forma como esta solo funciona con dos metas"""
            if (n.position == self.goal_position[0] and self.goal_position[1] in n.get_fathers_positions()):
                bandera = True
            if (n.position == self.goal_position[1] and self.goal_position[0] in n.get_fathers_positions()):
                bandera = True

            if bandera:
                solucionado = True
                return self.show_route(n.get_fathers())
            else:
                self.expanded_nodes.append(n)
                if (n.can_move(self.data, 'right')):
                    nodes.append(n.make_child_node('right'))
                if (n.can_move(self.data, 'up')):
                    nodes.append(n.make_child_node('up'))
                if (n.can_move(self.data, 'left')):
                    nodes.append(n.make_child_node('left'))
                if (n.can_move(self.data, 'down')):
                    nodes.append(n.make_child_node('down'))

    def show_route(self, nodes):
        print([n.weight for n in nodes])
        print(f'Profundidad: {nodes[-1].profundidad}')
        print(f'Cantidad nodos expandidos: {len(self.expanded_nodes)}')
        print([n for n in nodes ])
        while True:
            self.frame.fill((255, 255, 255))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            for i in range(10):
                for j in range(10):
                    val = self.data[i][j]
                    if val == 1:
                        self.frame.blit(self.imgMuro, (50 * j, 50 * i))
                    elif val == 3:
                        self.frame.blit(self.imgFreezer, (50 * j, 50 * i))
                    elif val == 4:
                        self.frame.blit(self.imgCell, (50 * j, 50 * i))
                    elif val == 5:
                        self.frame.blit(self.imgSemilla, (50 * j, 50 * i))
                    elif val == 6:
                        self.frame.blit(self.imgEsfera, (50 * j, 50 * i))
            self.frame.blit(self.imgEsfera, (50*self.goal_position[0][1], 50*self.goal_position[0][0]))
            self.frame.blit(self.imgEsfera, (50*self.goal_position[1][1], 50*self.goal_position[1][0]))
            if nodes[0].nave:
                self.frame.blit(self.imgGoku, (50 * nodes[0].position[1], 50 * nodes[0].position[0])) 
            else:
                self.frame.blit(self.imgGoku, (50 * nodes[0].position[1], 50 * nodes[0].position[0]))
            pygame.display.update()
            pygame.time.delay(1000)
            nodes.pop(0)

Main()