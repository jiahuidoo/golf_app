from q1 import * 
from q2 import * 

#Quesion 3a
class GolfSet:
    '''has a class variable _CLUBTYPE
    models an GolfSet with owner id, owner name and a collection golf clubs 
    using dictionary as the collection: key: clubtype category, value: list of club objects
    '''
    #class variable
    _CLUBTYPE = ["Wood", "Iron", "Putter"] #categories of golf clubs
    _MAXCLUBS = 14 #maximum number of clubs in a golf set

    '''may raise EquipmentRuleException'''
    def __init__(self, oId, oName, newSet):
        self._ownerID = oId
        self._owner = oName
        self._clubs = {}
        for cTy in type(self)._CLUBTYPE:
            self._clubs[cTy] = [] #create an empty list for each clubtype category
        
        '''load current golf set specification from file
        construct Club objects into _clubs by reading lines from the file
        '''
        self._filename = f"{oId}-{oName}.txt"

        if newSet == False:
            try:
                with open(self._filename, "r") as f:
                    for line in f:
                        lbl, cTy, hInfo, sInfo, gInfo = self.splitSpecInfo(line)
                        self.create(lbl, cTy, hInfo, sInfo, gInfo)
            #if file not found, raise EquipmentRuleException
            except FileNotFoundError:
                raise EquipmentRuleException(f"{self._filename} not found!")

    #property accessor methods
    @property
    def owner(self): return self._owner
    @property
    def numberOfClubs(self): return sum([len(i) for i in self._clubs.values()]) #sum of all clubs in the 3 categories of golf clubs 

    #class method 
    @classmethod
    def getClubType(cls): return cls._CLUBTYPE #return list of clubtype categories

    #mutator methods 
    def sortByLoft(self):
        '''
        function to mutate the order of the dict values (list)
        sort the list of club objects by loft within each clubtype category (dict key)
        '''
        for cType in self._clubs.keys():
            self._clubs[cType].sort(key=lambda x: x.loft, reverse=False)

    '''may raise EquipmentRuleException'''
    def add(self, clubType, newClub):
        '''function takes in 2 parameters: clubType and newClub (Club object)
        add into the matching clubtype category of _clubs
        need meet 6 quality checks, otherwise raise EquipmentRuleException
        '''
        #Check 1:
        #if number of clubs in the golf set is alr the max, cannot add anymore
        if self.numberOfClubs == type(self)._MAXCLUBS:
            raise EquipmentRuleException(f"Should not have more than {type(self)._MAXCLUBS} golf clubs in the set")

        #Check 2:
        #if the new club label alr exist, cannot add

        #flatten existing golf clubs in a list
        golfClubs = [c for clubs in self._clubs.values() for c in clubs]

        if newClub.label in [c.label for c in golfClubs]:
            raise EquipmentRuleException(f"Should not have same club label {newClub.label} within the set")

        #Check 3:
        #if the club's shaft flex different from those alr created in the same clubType category, cannot add
        if len(self._clubs[clubType]) > 0 and newClub.flex not in set([c.flex for c in self._clubs[clubType]]):
            raise EquipmentRuleException(f"Not advisable to have different shaft flex within the {clubType}")

        #Check 4:
        #if there is club having the same loft in the clubType category, cannot add
        if newClub.loft in [c.loft for c in self._clubs[clubType]]:
            raise EquipmentRuleException(f"Should not have same club loft {newClub.loft} within the {clubType}")

        #Check 5:
        #if new club with higher loft is longer than the next club in clubType category, cannot add
        #Check 6:
        #if new club with lower loft is shorter than the next club in clubType category, cannot add
        
        tmp = [[c.label, c.loft, c.length] for c in self._clubs[clubType]]
        for t in tmp:
            if newClub.loft > t[1] and newClub.length > t[2]:
                #logic: club with higher loft, should be shorter in length
                raise EquipmentRuleException(f"New club's length must not be shorter than next higher loft")

            if newClub.loft < t[1] and newClub.length < t[2]:
                #logic: club with lower loft, should be longer in length
                raise EquipmentRuleException(f"New club's length must not be longer than next lower loft")

        '''end of quality checks'''

        #add club
        self._clubs[clubType].append(newClub)

        #BONUS: sort by loft in ascending order
        self.sortByLoft()

    '''may raiseEquipmentRuleException'''
    def splitSpecInfo(self, line):
        '''function takes into 1 parameter: line
        split each line of specification for a Club into label, clubtype category, 
        headInfo (a list), shaftInfo (a list), gripInfo (a list)
        raise EquipmentRuleException if line does not correctly contain info
        of the club, label, clubtype, clubhead, shaft and grip.
        '''
        splits = line.replace("\n","").split(",")

        if len(splits) != 12:
            raise EquipmentRuleException(f"File line does not correctly contains required information:\n{line}")

        label = splits[0]
        #clubtype category: Wood, Putter, Rron
        clubType = splits[1]
        
        #parameters for ClubHead object: loft, weight, others (material, style, size)
        headInfo = splits[2:5]
        
        #parameters for Shaft object: length, weight, material, flex
        shaftInfo = splits[5:9]
        
        #paramters for Grip object: diameter, weight, material
        gripInfo = splits[9:]

        return label, clubType, headInfo, shaftInfo, gripInfo

    def create(self, label, clubType, headInfo, shaftInfo, gripInfo):
        '''
        function takes in 5 parameters: label, clubType, 
        headInfo (a list), shaftInfo (a list), gripInfo (a list)
        to create the club components; ClubHead, Shaft and Grip, and constuct into a Club
        to add created club into golf set
        Error Handling for EquipmentRuleException: may arise when create or add club
        '''
        #construct ClubHead object, call ClubHead subclass
        #e.g. WoodHead(10.5,203,450)
        head = eval(f'{clubType}Head({headInfo[0]},{headInfo[1]},"{headInfo[2]}")')
        #construct Shaft object
        #e.g. Shaft(length, weight, material, flex)
        shaft = Shaft(shaftInfo[0], shaftInfo[1], shaftInfo[2], shaftInfo[3])
        #construct Grip object
        #e.g. Shaft(diamater, weight, material)
        grip = Grip(gripInfo[0],gripInfo[1],gripInfo[2])

        #create Club with ClubHead, Shaft and Grip
        club = Club(label, head, shaft, grip)
        #add created Club into Golf Set
        self.add(clubType, club)

    '''may raise EquipmentRuleException'''
    def remove(self, label):
        '''function takes in 1 parameter: label
        match label and remove club from the golf set
        otherwise, raise EquipmentRuleException if unable to match label
        '''
        found = False
        for cTy, clubs in self._clubs.items():
            for c in clubs:
                if c.label == label.upper():
                    found = True
                    self._clubs[cTy].remove(c)
        
        if not found:
            raise EquipmentRuleException(f"Cannot remove as {label} is not in set")

    #other methods 
    def saveToFile(self):
        tmp=[f"{c}" for clubs in self._clubs.values() for c in clubs]
        
        f = open(self._filename, "w")
        f.write("\n".join(tmp))
        f.close()
    
    def getGolfSetDetails(self):
        tmp=""
        for clubs in self._clubs.values():
            for c in clubs:
                tmp+=f"{c.getDetails()}\n"
        tmp+=f"No of clubs: {self.numberOfClubs}\n"
        return tmp

    def __str__(self):
        tmp=""
        for clubs in self._clubs.values():
            for c in clubs:
                tmp+=f"{c}\n"
        return tmp

#Question 3b
def menu():
    print("Golfit Main Menu")
    print("==========================")
    print("1. Build a golf set")
    print("2. Load a golf set")
    print("0. Quit")
    opt = input ("Enter option: ")
    return opt

def subMenu(name):
    print(f"Club Fitting for {name}")
    print("==========================")
    print("1. Add a club")
    print("2. Remove a club")
    print("0. Back to Main Menu")
    choice = input ("Enter choice: ")
    return choice

def main():
    while True:
        opt = menu()
        if opt not in ["0", "1", "2"]:
            print("Sorry, please enter within range(0-2)\n")

        else:
            if opt == "0":
                break 

            elif opt == "1":
                golferId = input("Enter Golfer ID: ")
                golferName = input("Enter Golfer name: ")
                
                #One-time message
                print(f'''{"*"*45}\nRecommendation:\n- Build the set from longest to shortest club\n- i.e., from Driver to Putter\n{"*"*45}''')
                try:
                    golfSet = GolfSet(golferId, golferName, True)
                except EquipmentRuleException as e:
                    print(e)
                    continue

            elif opt == "2":
                golferId = input("Enter Golfer ID: ")
                golferName = input("Enter Golfer name: ")
                try:
                    golfSet = GolfSet(golferId, golferName, False)
                except EquipmentRuleException as e:
                    print(e)
                    continue
            
            #display id, name and golf set details
            print(golferId, golferName)
            print(golfSet.getGolfSetDetails())

            while True: 
                choice = subMenu(golferName)
                if choice not in ["0", "1", "2"]:
                    print("Sorry, please enter within range(0-2)\n")

                else:
                    if choice == "0":
                        #save to file before exiting sub menu
                        golfSet.saveToFile()
                        print("Save spec file.")
                        break

                    elif choice == "1":
                        '''Create new club and add into golf set
                        '''

                        #valid clubtype has to be selected
                        while True:
                            clubType = input("Which club type to add: ").capitalize()
                            if clubType in golfSet._CLUBTYPE:
                                break
                            
                            print(f"Sorry, please select from {golfSet._CLUBTYPE}")
                        #end of while loop

                        #prompt user to enter club's label
                        label = input("Enter the new club label: ")

                        #prompt user to enter head info: loft, weight, other (size, material or style)
                        hLoft = input("Enter clubhead loft: ")
                        hWeight = input("Enter clubhead weight: ")
                        if clubType == "Wood":
                            hOther = input("Enter wood size: ")
                        
                        elif clubType == "Iron":
                            hOther = input("Enter iron material: ")

                        else: #Putter
                            hOther = input("Enter putter style: ")
                        
                        headInfo = [hLoft, hWeight, hOther]

                        #prompt user to enter shaft info: length, weight, material, flex
                        sLength = input("Enter length of shaft: ")
                        sWeight = input("Enter weight of shaft: ")
                        sMaterial = input("Enter shaft material: ")
                        sFlex = input("Enter shaft flex: ")

                        shaftInfo = [sLength, sWeight, sMaterial, sFlex]

                        #prompt user to enter grip info:
                        gDiameter = input("Enter diameter of grip: ")
                        gWeight = input("Enter weight of grip: ")
                        gMaterial = input("Enter grip material: ")

                        gripInfo = [gDiameter, gWeight, gMaterial]

                        #create and add into golf set
                        try:
                            golfSet.create(label, clubType, headInfo, shaftInfo, gripInfo)
                            print("New club added")
                        except EquipmentRuleException as e:
                            print(e)
                        print()
                        #display id, name and golf set details
                        print(golferId, golferName)
                        print(golfSet.getGolfSetDetails())

                    elif choice == "2":
                        #remove
                        #prompt user to enter club's label (to be removed)
                        label = input("Enter the club label to remove: ")

                        try:
                            golfSet.remove(label)
                            print("Removal done...")
                        except EquipmentRuleException as e:
                            print(e)
                        print()
                        #display id, name and golf set details
                        print(golferId, golferName)
                        print(golfSet.getGolfSetDetails())
            #end of while loop
    #end of while loop

'''main()'''