import Genshin_Artifact
import random

# Upgrade artifacts for Diluc
# The main attribute must match.
TARGET_MAIN={"Flower":"HP","Feather":"ATK","Hourglass":"ATK%","Cup":"Pyro","Crown":["CRate","CDamage"]}
# Assming our upgradation target sub-attributes is crit rate and crit damage.
TARGET_SUB=["CRate","CDamage"]
TOLERANCE={"Flower":1,"Feather":1,"Hourglass":2,"Crown":3,"Cup":3}
# Every artifact (either 3 init or 4 init) has 5 chance to upgrade.
# Missed upgraded times, [upgraded_times - (CRate+CDamage)] should lower than our tolerance, 
# otherwise this artifact will be dropped.
# Through this, the actual tolerance of missed upgraded times 
# can be differently determined based on different position and different number of initial attributes.
# Hint: try to infer my expectation for each position of artifacts.

def print_result(artifact:Genshin_Artifact.Artifact):
    print(artifact.sub_attributes)


# This is my strategy to determine whether and how to upgrade an artifact or not
# The strategy may change after each upgradation
def upgrade_logic(artifact:Genshin_Artifact.Artifact,display=True):
    
    # drop_or_keep=random.choice(["Drop","Keep"])
    # if drop_or_keep=="Drop":
    #     return
    
    # Determine if main attribute is correct
    # If main attribute is useless, then directly dropped
    if artifact.main_attribute not in TARGET_MAIN[artifact.position]:
        if display:
            print("The main attribute is wrong!")
            print("Drop!")
        return False
        
    # If the artifact has 4 initial sub-attributes while doesn't have crit rate and crit damage, then drop.
    elif len(artifact.sub_attributes)==4 and all(i not in artifact.sub_attributes for i in TARGET_SUB):
        if display:
            print("No crit in sub-attributes.")
            print("Drop!")
        return False
    
    # This artifact is deserve to be upgraded
    # But it may still be dropped if it become a rubbish during upgradation
    else:
        # Every artifact (either 3 init or 4 init) has 5 chance to upgrade.
        while artifact.upgraded_times<5:
            artifact.Upgrade(display=display)
            # After upgrade once, a crown may have 4 useless sub-attributes from 3, the directly drop
            if all(i not in artifact.sub_attributes for i in TARGET_SUB):
                if display:
                    print("Useless crown")
                    print("Drop!")
                return False
            
            # Count the total number of crit rate and crit damage attributes after each upgradation
            c_num=artifact.sub_attributes.get("CRate",0)+artifact.sub_attributes.get("CDamage",0)
            # If it has no possibility to match our expectation for its position, then directly drop.
            if artifact.upgraded_times-c_num>=TOLERANCE[artifact.position]:
                if display:
                    print("歪麻了！")
                    print("Drop!")
                return False
        # The artifact achieves our expectation for its position
        else:
            if display:
                print("Graduation!") # The final result matches the graduation standards.
            return True

# Abandoned version
'''
    pos=artifact.position
    if pos=="Flower":
        upgrade_logic_flower(artifact)
        
    elif pos=="Feather":
        upgrade_logic_feather(artifact)
        
    elif pos=="Hourglass":
        upgrade_logic_hourglass(artifact)
        
    elif pos=="Cup":
        upgrade_logic_cup(artifact)
        
    else:
        upgrade_logic_crown(artifact)

def check_c(artifact:Genshin_Artifact.Artifact):
    if all(i in artifact.sub_attributes for i in ["CRate","CDamage"]):
        num=2
    elif any(i in artifact.sub_attributes for i in ["CRate","CDamage"]):
        num=1
    else:
        num=0
    return num

def upgrade_logic_flower(artifact:Genshin_Artifact.Artifact):
    pass

def upgrade_logic_feather(artifact:Genshin_Artifact.Artifact):
    pass

def upgrade_logic_hourglass(artifact:Genshin_Artifact.Artifact):
    pass

def upgrade_logic_cup(artifact:Genshin_Artifact.Artifact):
    pass

def upgrade_logic_crown(artifact:Genshin_Artifact.Artifact):
    pass
'''

# From 0 start, farming artifacts for one character 
# Simulate the real situation of farming artifacts in Genshin Impact
def Framing_Artifacts(target="Diluc",
                      suit="Mo nv",
                      display=True): # whether to display details or not
    if display:
        print(f"Start drawing artifacts for {target}")
    count=0 # Total number of farming times
    graduate_dict={} # Store number of artifacts in each position
    grad_list=[] # Store the best graduated artifact of each position
    while True:
        artifact=Genshin_Artifact.Artifact(suit=suit,display=display)
        count+=1
        if upgrade_logic(artifact=artifact,display=display):
            grad_list.append(artifact)
            position=artifact.position
            # counting number of graduated artifacts in different position
            if position in graduate_dict:
                graduate_dict[position]+=1
            else:
                graduate_dict[position]=1
            
            # If we graduate 4 positions, the suit of artifacts is graduated because we can use 1 piece from other suits.     
            if len(graduate_dict)>=4:
                
                # After graduation, some position may have multiple graduated artifacts
                # We can choose the best one for each position
                best_artifacts=pick_best(grad_list)
                
                if display:
                    print("4 positions are graduated!")
                    print(f"Count of graduated artifacts in each position: {graduate_dict}")
                    print()
                    print("The best artifacts in each position:")
                    for artifact in filter(None,best_artifacts):
                        print(f"{artifact.position}: {artifact.main_attribute}, {artifact.sub_attributes}")
                    print()
                    print(f"Total number of farming: {count}")
                farm_log=[graduate_dict,best_artifacts,count]
                return farm_log
        else:
            continue

# After all (4) postion is graduated, we may have multiple graduated artifacts in each position
# pick the best artifacts of each postion.
def pick_best(artifacts_list:list[Genshin_Artifact.Artifact]):
    artifact_slot={"Flower":0,"Feather":1,"Hourglass":2,"Cup":3,"Crown":4}
    best_artifacts=[None,None,None,None,None] # Each slot corresponding to flower, feather, hourglass, cup, crown.
    for ar in artifacts_list:
        index=artifact_slot[ar.position]
        if best_artifacts[index] is None:
            best_artifacts[index]=ar
        elif crit_num(ar)>=crit_num(best_artifacts[index]):
            best_artifacts[index]=ar
    best_artifacts:list[Genshin_Artifact.Artifact] # Notice the datatype

    return best_artifacts

# Check if an artifact's sub-attributes have either crit rate or crit damage
def check_crit(artifact:Genshin_Artifact.Artifact):
    sub_att=artifact.sub_attributes
    if any(i in sub_att for i in [TARGET_SUB]):
        return True
    else:
        return False  

# Calculate the crit score (sum of crit rate and crit damage) of an artifact
def crit_num(artifact:Genshin_Artifact.Artifact):
    sub_dict=artifact.sub_attributes
    crit_score=sub_dict.get("CRate",0)+sub_dict.get("CDamage",0)
    
    return crit_score

# Farming artifacts for 100 characters
def farm_for_characters(n=100):
    total_count=0
    for i in range(n):
        count=Framing_Artifacts(display=False)[2] # The count of a character's farming times
        total_count+=count
        # print(f"number of farming times in this graduation:{count}")        
        # print()
    avg=total_count//n
    print(f"Average farm times for every character: {avg}")
    

# Farming artifacts for Diluc
graduate_dict=Framing_Artifacts()
print()
n=100
print(f"Farm artifacts for {n} characters:")
farm_for_characters(n=n)
