class Node:

    def __str__(self):
        return "{0},{1}".format(self.x, self.y)
    
    def __repr__(self) -> str:
        return f'({self.position[0]},{self.position[1]})'

    def __init__(self, position,father,profundidad=0):
        self.position = position
        self.father = father
        self.gas_nave_3 = 0
        self.gas_nave_4 = 0
        self.profundidad = profundidad
        self.id_nave = 0
        self.weight = 0
        if father and father.nave:
            self.nave = True
        else:
            self.nave = False  


    def get_id_nave(self):
        return self.id_nave    

    def set_id_nave(self,new_id):
        self.id_nave = new_id

    def admin_gaso(self):
        if self.nave == True:
            if self.id_nave == 3 and (self.gas_nave_3 == None or self.gas_nave_3 < 11) :
                self.gas_nave_3 += 1
                self.nave = True
            elif self.id_nave == 4 and (self.gas_nave_3 == None or self.gas_nave_3 < 21):
                self.gas_nave_4 += 1
                self.nave = True
            elif self.gas_nave_3 == 20 or self.gas_nave_4 == 20:
                self.nave = False
                self.gas_nave_3 = None
                self.gas_nave_4 = None
        else:
            self.gas_nave_3 = None
            self.gas_nave_4 = None



    def check_is_goal(self, world):
        if world[self.position[0]][self.position[1]] == 5:
            world[self.position[0]][self.position[1]] = 0
            print(self.position[0] , self.position[1])
            return True
        else:
            return False
        #return world[self.position[0]][self.position[1]] == 5
    
                                              
    def can_move(self, world, direction):
            if direction == 'up':
                if self.father and (self.position[0]-1, self.position[1]) == self.father.position:
                    return False
                return self.position[0] != 0 and world[self.position[0]-1][self.position[1]] != 1
            elif direction == 'down':
                if self.father and (self.position[0]+1, self.position[1]) == self.father.position:
                    return False
                return self.position[0] != 9 and world[self.position[0]+1][self.position[1]] != 1
            elif direction == 'left':
                if self.father and (self.position[0], self.position[1]-1) == self.father.position:
                    return False
                return self.position[1] != 0 and world[self.position[0]][self.position[1]-1] != 1
            elif direction == 'right':
                if self.father and (self.position[0], self.position[1]+1) == self.father.position:
                    return False
                return self.position[1] != 9 and world[self.position[0]][self.position[1]+1] != 1
            else:
                raise AttributeError

    def make_child_node(self, direction):
        if direction == 'up':
            node = Node((self.position[0]-1, self.position[1]), self,self.profundidad+1)
        elif direction == 'down':
            node = Node((self.position[0] + 1, self.position[1]), self,self.profundidad+1)
        elif direction == 'left':
            node = Node((self.position[0], self.position[1]-1), self,self.profundidad+1)
        elif direction == 'right':
            node = Node((self.position[0], self.position[1]+1), self,self.profundidad+1)
        else:
            raise AttributeError
        node.father = self
        return node

    def make_child_node_with_weight(self, direction, world):
        if direction == 'up':
            node = Node((self.position[0]-1, self.position[1]), self,self.profundidad+1)
        elif direction == 'down':
            node = Node((self.position[0] + 1, self.position[1]), self,self.profundidad+1)
        elif direction == 'left':
            node = Node((self.position[0], self.position[1]-1), self,self.profundidad+1)
        elif direction == 'right':
            node = Node((self.position[0], self.position[1]+1), self,self.profundidad+1)
        else:
            raise AttributeError

        if world[node.position[0]][node.position[1]] == 6 and not node.nave:
            peso = 4
        elif world[node.position[0]][node.position[1]] == 3:
            node.nave = True
            peso = 1
            node.set_id_nave(3)
        elif world[node.position[0]][node.position[1]] == 4:
            node.nave = True
            peso = 1
            node.set_id_nave(4)
        else:
            peso = 1
        node.weight = peso + node.father.weight
        return node
    


    def get_fathers(self):
        fathers = []
        actual_node = self
        fathers.insert(0, actual_node)
        while actual_node.father:
            fathers.insert(0, actual_node.father)
            actual_node = actual_node.father
        return fathers
    
    def get_fathers_positions(self):
        fathers = []
        actual_node = self
        fathers.insert(0, actual_node)
        while actual_node.father:
            fathers.insert(0, (actual_node.father.position[0],actual_node.father.position[1]) )  
            actual_node = actual_node.father
        return fathers

    '''
    Cambios añadidos
    '''
    def get_position(self):
        return self.position

    def check_node_equal(self,node):
        if self.position == node.get_position():
            return True
        else:
            return False

    def in_list(self, nodes):
        in_list = False
        for n in nodes:
            if self.check_node_equal(n):
                in_list = True
        return in_list 

    def get_father(self):
        return self.father

    #This a function avoid return in the branch
    #Take data object and compare data of grandfhater
    def is_grandfather(self,node)-> bool:
        abue = node.get_father()
        if self.position == abue.get_position():
            return True
        else:
            return False