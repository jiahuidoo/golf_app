from q1 import * 

#Quesion 2a
class Shaft:
    '''models a Shaft 
    it has 4 attributes: length, weight, material, and flex 
    it has property methods: length, weight, flex
    it has a __str__() method 
    '''
    def __init__(self, length, weight, material, flex):
        self._length = float(length) #type=float; length of the shaft in inches
        self._weight = int(weight) #type=int; weight of shaft in grams
        self._material = material.capitalize() #type=str; material of the shaft, graphite or steel

        #convert to abbr. otherwise take in as it is which may already be in abbr. when load from spec file
        self._flex = "SR" if flex == "Senior" else "R" if flex == "Regular" else "S" if flex == "Stiff" else "XS" if flex == "Extra-Stiff" else flex.upper() #type=str; SR, R, S, XS
    
    #property accessor methods
    @property
    def length(self): return self._length
    @property
    def weight(self): return self._weight
    @property
    def flex(self): return self._flex

    def __str__(self):
        return f"{self._length},{self._weight},{self._material},{self._flex}"

class Grip:
    '''models a Grip 
    it has 4 attributes: diameter, weight, and material
    it has property methods: 
    it has a __str__() method 
    '''
    def __init__(self, diameter, weight, material):
        self._diameter = float(diameter) #type=float; thickness of the grip in inches, 0.6 or 0.58
        self._weight = int(weight) #type=int; weight of the grip in grams
        self._material = material.capitalize() #type=str; material of the grip, rubber, leather or synthetic

    #property accessor methods
    @property
    def diameter(self): return self._diameter
    @property
    def weight(self): return self._weight

    def __str__(self):
        return f"{self._diameter:.3g},{self._weight},{self._material}"

#Question 2b
class EquipmentRuleException(Exception):
    '''subclass of Exception 
    use when runtime error happens in Club object(s)'''
    pass

#Question 2c
class Club:
    '''models a golf Club with attributes: label and the 3 parts: ClubHead, Grip and Shaft objects
    it has a property for label
    it has property for loft, flex, length, weight
    it has mutator method: changeGrip() - may raise Exception
    it has method getDetails()
    the constructor may also raise Exception'''

    '''may raise EquipmentRuleException'''
    def __init__(self, label, head, shaft, grip):
        self._label = label.upper() #club's label for the golfers to identify
        self._head = head #ClubHead object
        self._shaft = shaft #Shaft object
        self._grip = grip #Grip object

        #weight of the ClubHead must be more than the combined weight of the Shaft and Grip
        if self._head.weight <= self._shaft.weight + self._grip.weight:
            raise EquipmentRuleException(f"Clubhead must weight more than {self._shaft.weight + self._grip.weight:}g")

        #assembled club length must be between 18 to 48 inches
        #club length = height of ClubHead + length of Shaft
        clubLength = self._head.getHeight() + self._shaft.length
        if clubLength < 18:
            raise EquipmentRuleException(f"Club length {clubLength}in too short!")

        elif clubLength > 48:
            raise EquipmentRuleException(f"Club length {clubLength}in too long!")

    #property accessor methods
    @property
    def label(self): return self._label
    @property
    def head(self): return self._head
    @property
    def shaft(self): return self._shaft
    @property
    def grip(self): return self._grip
    @property
    def loft(self): return self._head.loft
    @property
    def flex(self): return self._shaft.flex

    @property
    def length(self): 
        #length of Shaft and height of the ClubHead
        return self._head.getHeight() + self._shaft.length

    @property
    def weight(self): 
        #total weight of ClubHead, Shaft and Grip
        return self._head.weight + self._shaft.weight + self._grip.weight 

    #mutator method
    '''may raise EquipmentRuleException'''
    def changeGrip(self, newGrip): #pass in new Grip object
        '''error: the weight of the head less than the 
        combined weight of the shaft and new grip (threshold)
        '''
        weightThresh = self._shaft.weight + newGrip.weight
        if self._head.weight <= weightThresh:
            raise EquipmentRuleException(f"Clubhead must weight more than {weightThresh}g")
        #change new Grip
        self._grip = newGrip
    
    def getDetails(self):
        return f"Club: {self._label:<10}Loft: {self.loft} Length: {self.length:.2f}in Flex: {self.flex} Weight: {self.weight}g"

    def __str__(self):
        #return formatted label and outputs of ClubHead, Shaft and Grip objects
        return f"{self._label},{self._head},{self._shaft},{self._grip}"

#Question 2d
def main():
    '''
    the creation of club and error handling repeat the same steps 
    for all golf clubs, so "for loop" is used.
    '''
    #add up total weight of clubs
    totalWeight = 0

    #list to store golf clubs
    golfClubs = []

    #dictionary
    #collections of golf clubs to be created
    #consists configuration of club head and shaft for each club
    golfConfig = {"Driver": [['Wood',10.5,203,450],[45,68,'Graphite','Stiff']], 
                "8-iron": [['Iron',34.5,268,'Cast'],[35.5,109,'Steel','Regular']], 
                "Sunset": [['Putter',3,380,'Mallet'],[33,120,'Steel','Stiff']], 
                "5-wood": [['Wood',17.5,150,280],[42.5,89,'Steel','Stiff']]
                }

    #all clubs use this grip
    g1 = Grip(0.6,62,"Rubber")

    #part i
    for label, value in golfConfig.items():
        '''eval() is used to dynamically call the 
        respective Clubhead subclass; WoodHead, PutterHead or IronHead
        with necessary parameters according to the club type/ catgeory'''
        h = eval(f'{value[0][0]}Head({value[0][1]},{value[0][2]},"{value[0][3]}")')
        s = Shaft(value[1][0], value[1][1], value[1][2], value[1][3])
        try:
            c = Club(label, h,s,g1) #construct Club object
            golfClubs.append(c) #add into created clubs
            totalWeight += c.weight #sum total weight
            print(c.getDetails())
        except EquipmentRuleException as e:
            print(f"Club: {label:<10}Error: {e}")
    
    print(f"Number of clubs created: {len(golfClubs)}\nTotal weight: {totalWeight:.2f}g")

    #part ii
    #new grip
    g2 = Grip(0.58,75,"Leather")

    #replace grip for all created golf clubs
    for gc in golfClubs:
        gc.changeGrip(g2)
        print(gc)

'''main()'''