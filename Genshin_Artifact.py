# Simulating the artifacts system
import random

# attriubtes_list=["ATK%","ATK","DEF%","DEF","HP%","HP","EMatster","ECharge","CRate","CDamage"]

# A simulator for generate an artifact
# Assuming the position only has Feather and Flower
class Artifact:
    def __init__(self,
                 suit="Default",
                 position=None, 
                 # Note: Don't use "position=random.choice(["Feather","Flower","Hourglass","Cup","Crown"])" here, 
                 # because the interpreter load the function definition only once!
                 display=True): # By default, display logs after create an instance
        # self.level=1
        self.suit=suit
        if position is None:
            self.position=random.choice(["Feather","Flower","Hourglass","Cup","Crown"])
        else:
            self.position=position
        self.main_attribute=self.Generate_main_attribute(self.position) # Generate main attribute for this artifact
        # self.star=random.choice([4,5]) if self.suit in ["Pyro"] else random.choice([1,2,3,4,5])
        self.star=5 # Assuming 5 stars only
        # The sub-attributes pool for all artifacts and their relative weight
        self.sub_attributes_pool={"ATK":150,
                                  "HP":150,
                                  "DEF":150,
                                  "CRate":75,
                                  "CDamage":75,
                                  "ATK%":100,
                                  "HP%":100,
                                  "DEF%":100,
                                  "ECharge:":100,
                                  "EMaster":100}
        self.sub_attributes=self.Generate_sub_attributes() # generate sub-attributes for this artifact
        self.upgraded_times=0
        self.value=None
        if display:
            self.print_attributes()
    
    # Generate a main attribute for a artifact in different position
    def Generate_main_attribute(self,position):
        # Different main attributes have different relative weights on each position
        position_main={"Flower":[["HP"],[1]],
                       "Feather":[["ATK"],[1]],
                       "Hourglass":[["ATK%","HP%","DEF%","ECharge","EMaster"],
                                    [26.66,26.66,26.66,10,10]],
                       "Cup":[["ATK%","HP%","DEF%","Pyro","Hydro","Electro","Cryo","Anemo","Dendro","Geo","Physical","EMaster"],
                              [19.25,19.25,19.25,5,5,5,5,5,5,5,5,2.5]],
                       "Crown":[["ATK%","HP%","DEF%","Heal","CRate","CDamage","EMaster"],
                                [22,22,22,10,10,10,4]]}
        
        # Draw a main attribute from pool of its position based on weights
        if position in position_main:
            att_pool=position_main[position][0]
            weights=position_main[position][1]
            attribute=random.choices(att_pool,weights=weights,k=1)[0]
            return attribute
        
        else:
            print("Invalid position.")
            return "Default"    

    # Generate sub-attributes for a artifact
    def Generate_sub_attributes(self):
        # The sub-attributes can't be duplicated with the main attribute
        att_pool=self.sub_attributes_pool
        if self.main_attribute in self.sub_attributes_pool:
            att_pool.pop(self.main_attribute)
        
        # An artifact has 80% chance to have 3 initial attributes and 20% chance to have 4.
        num_att=random.choices([3,4],weights=[0.8,0.2],k=1)[0]
        
        sub_att=[]
        for i in range(num_att):
            # Assuming the sub-attributes have relative weights in chance to appear
            att_pool_list=list(att_pool.keys()) 
            weights=list(att_pool.values()) # Generate relative weights list in each draw
            # print(att_pool_list,weights)
            attribute=random.choices(att_pool_list,weights=weights,k=1)[0]
            att_pool.pop(attribute) # Update the pool after each attribute is picked
            sub_att.append(attribute)
        sub_attributes={j:1 for j in sub_att}
        return sub_attributes
    
    # Upgrade the sub-attributes once 
    def Upgrade(self,display=True):
        # Complement the 4-th sub-attribute if it has slot
        if len(self.sub_attributes)<4:
            att_pool={key:value for key,value in self.sub_attributes_pool.items()
                      if key!=self.main_attribute and key not in self.sub_attributes}
            att_pool_list=list(att_pool.keys())
            weights=list(att_pool.values())
            attribute=random.choices(att_pool_list,weights=weights,k=1)[0]
            
            self.sub_attributes[attribute]=1
            self.upgraded_times+=1
                

        else:
            # Assuming each sub-attribute has equal chance to be upgraded
            upgrade=random.choice(list(self.sub_attributes.keys()))
            self.sub_attributes[upgrade]+=1
            self.upgraded_times+=1
        if display==True:
            print("Upgraded.",end=" ")
            self.print_sub_attributes()
        
    # Print some logs
    def print_attributes(self):
        print(f"Suit: {self.suit}")
        print(f"Position: {self.position}")
        print(f"Main attribute: {self.main_attribute}")
        # print(f"Star: {self.star}")
        print(f"Sub-Attribute: {self.sub_attributes}")
    
    # print sub-attributes
    def print_sub_attributes(self):
        print(f"Sub-Attribute: {self.sub_attributes}") 
        
# Get 1000 crowns and look for attributes counts
def get_crowns(number=1000):
    crowns={}
    for i in range(number):
        artifact=Artifact(position="Crown",display=False)
        if artifact.main_attribute in crowns:
            crowns[artifact.main_attribute]+=1
        else:
            crowns[artifact.main_attribute]=1
    crowns=dict(sorted(crowns.items())) # sort the dictionary by keys to display
    return crowns

if __name__=="__main__":
    # Get an artifact
    Artifact_1=Artifact(suit="Pyro")
    for i in range(Artifact_1.star):
        Artifact_1.Upgrade()
        
    # Get 1000 crown and count main attributes
    print("Get 1000 crown and count main attributes")
    aLotOfcrowns=get_crowns()
    print("Count main attributes of crowns:")
    print(aLotOfcrowns)
    


            
        