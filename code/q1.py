#Inheritance: Wood, Iron, and Putter head "is a" Club Head
#Clubhead: Superclass
#WoodHead, IronHead, PutterHead: Subclasses
from abc import ABC, abstractmethod

#Question 1a
class ClubHead(ABC):
    '''models a clubhead 
    it is a superclass 
    it has 2 attributes: loft, and weight
    it has property methods: loft, weight
    it has abstract  method: getHeight() --> set a framework for its subclassess
    it has a __str__() method 
    '''
    def __init__(self, loft, weight):
        self._loft = float(loft) #type=float; loft of the clubhead in degrees.
        self._weight = int(weight) #type=int; weight of the clubhead in grams

    #property accessor methods
    @property
    def loft(self): return self._loft
    @property
    def weight(self): return self._weight

    @abstractmethod
    def getHeight(self):
        pass

    def __str__(self):
        return f"{self._loft},{self._weight}"

#Question 1b
class WoodHead(ClubHead):
    '''models a wood-head
    it has 3 attributes: loft, weight, size
    it has additional method: getHeight() returns size/400
    it has a __str__() method 
    '''
    def __init__(self, loft, weight, size):
        super().__init__(loft, weight) #inherit all the methods and properties from ClubHead
        self._size = float(size) #type=float

    #method: compute the height for a wood
    def getHeight(self):
        return self._size / 400

    def __str__(self):
        return f"Wood,{super().__str__()},{self._size}"

class IronHead(ClubHead):
    '''models a iron-head
    it has 3 attributes: loft, weight, material
    it has additional method: getHeight() returns 1
    it has a __str__() method
    '''

    def __init__(self, loft, weight, material):
        super().__init__(loft, weight) #inherit all the methods and properties from ClubHead
        self._material = material #"Cast" or "Forged"

    #method: compute the height for a iron 
    def getHeight(self):
        return 1

    def __str__(self):
        return f"Iron,{super().__str__()},{self._material}"

class PutterHead(ClubHead):
    '''models a putter-head
    it has 3 attributes: loft, weight, style
    it has additional method: getHeight() returns 1 if the putter's style is Blade, else 0,5
    it has a __str__() method 
    '''
    def __init__(self, loft, weight, style):
        super().__init__(loft, weight) #inherit all the methods and properties from ClubHead
        self._style = style #"Blade", "Half-Mallet", "Mallet"

    #method: compute the height for a putter
    def getHeight(self):
        if self._style == "Blade":
            return 1
        else:
            return .5

    def __str__(self):
        return f"Putter,{super().__str__()},{self._style}"

#Question 1c
def main():
    #Part i - Create objects for Putter, Iron, Wood
    putter = PutterHead(3.5,365,"Blade")
    iron = IronHead(37.5,285,"Forged")
    wood = WoodHead(9.5,206,450)

    #Part ii - Print the details of the clubheads: loft, weight, height
    print("Details:")
    print(f"{putter} Height: {putter.getHeight():.2f}in")
    print(f"{iron} Height: {iron.getHeight():.2f}in")
    print(f"{wood} Height: {wood.getHeight():.2f}in")

'''main()'''