from pathlib import Path
try: 
    import git
except:
    print("\nNeed to have GitPython installed for this to function. Please run 'pip install GitPython', then try again.")
    exit 
import os
import shutil
import random
import re
import json
import time
import datetime
import argparse

# Shamelessly stolen from https://medium.com/@nutanbhogendrasharma/searching-text-in-multiple-files-in-python-5b40196b2d10, and then 
# tweaked so it works properly for my purposes. Yes, it's ugly, but it works, and it doesn't cause python to error out as the original
def searchText(path, text):
    folderList = []
    files = os.listdir(path)
    for file_name in files:
        abs_path = path + file_name
        if os.path.isdir(abs_path):
            folderList.append(abs_path)
           
        if os.path.isfile(abs_path) and abs_path.endswith('cs'):
            with open(abs_path, 'r') as f:
                if text in f.read():
                    final_path = abs_path
                    if type(final_path) != None:
                        return final_path
                    else:
                        continue
                else:
                    continue

        for dirName in folderList:
            dfiles = os.listdir(dirName)
            for dfn in dfiles:
                abs_path = dirName + '/' + dfn
                with open(abs_path, 'r') as f:
                    if abs_path.endswith('cs'):
                        pass
                    else:
                        continue

                    if text in f.read():
                        final_path = abs_path
                        if type(final_path) != None:
                            return final_path
                        else:
                            continue
                    else:
                        continue
    pass


#Set up early variables
repoUrl = "https://github.com/FiendsOfTheElements/FF1Randomizer.git"

# Set variables from arguments
args = argparse.ArgumentParser()
# Option 1: you want blind seed? you get blind seed.
args.add_argument('-b', '--blind', help="Make it a blind seed", action="store_true")
# Option 2: if deep dungeon is to be possibly enabled
args.add_argument('-d', '--deepdungeon', help="Enable the possibility of Deep Dungeon", action="store_true")
# Option 3: if experimental tab should be enabled
args.add_argument('-e', '--experimental', help="Enable the experimental tab", action="store_true")
# Option 4: If you want to mess with Max and Starting levels
args.add_argument('-l', '--levels', help="Enable the Max Level Slider and Starting level dropdown", action="store_true")
# Option 5: if max mp randomization is wanted
args.add_argument('-m', '--mp', help="Enable max MP randomization", action="store_true")
# Option 6: Output file path.
args.add_argument('-o', '--outfile', help="Path where you want the output file dropped. Default is current working directory")
# Option 7: Allow for Shops to be killed
args.add_argument('-s', '--shopkill', help="Enable shop kill chances", action="store_true")
# Option 8: if transmooglifier is wanted as a possibility
args.add_argument('-t', '--transmoog', help="Enable possible transmooglifier", action="store_true")
# Option 9: Add XP per class variance
args.add_argument('-x', '--xp', help="Allow per class XP randomization", action="store_true")

parseArgs = args.parse_args()

# Get the repo 
homeDir = Path.home()
workingDir = str(homeDir) + '/FF1FRtmp'
try:
    repo = git.Repo.clone_from(repoUrl, workingDir)
except:
#    print("Working Directory already found at " + workingDir + ", or you're offline. Would you like to continue, assuming that directory is populated properly?")
#    rec = input("If you would like to continue, enter 'Y': ")
#    if rec.lower() == 'y':
#        pass
#    else:
#        print("Please clean up/remove " + workingDir + " and try again")
#        exit
    pass

# Initialize variables
flagDict = {}
lineCont = 0
lineConcat = ""
lastLine = ""
rolledValue = ''
outputDict = {}
timeStamp = datetime.datetime.now()
uTime = str(datetime.datetime.timestamp(timeStamp))[0:10]
fsName = "FF1Rando Rando Generated Flagset " + uTime
if type(parseArgs.outfile) != None:
    try:
        if parseArgs.outfile[-1] != "/":
            parseArgs.outfile += "/"
        ofName = parseArgs.outfile + "FF1RR." + uTime + ".json"
    except:
        ofName = "FF1RR." + uTime + ".json"
else:
    ofName = "FF1RR." + uTime + ".json"
guardOpen = open('guardRails.json')
guardJson = json.load(guardOpen)

if parseArgs.deepdungeon == True:
    del guardJson["DeepDungeonGenerator"]
if parseArgs.mp == True:
    mplist = ["RedMageMaxMP","WhiteMageMaxMP","BlackMageMaxMP","KnightMaxMP","NinjaMaxMP"]
    for m in mplist:
        del guardJson[m]
if parseArgs.transmoog == True:
    del guardJson["Transmooglifier"]
if parseArgs.shopkill == True:
    sklist = ["ShopKillMode_Weapons","ShopKillMode_Armor","ShopKillMode_Item","ShopKillMode_Black","ShopKillMode_White","ShopKillFactor_Weapons","ShopKillFactor_Armor","ShopKillFactor_Item","ShopKillFactor_Black","ShopKillFactor_White"]
    for s in sklist:
        del guardJson[s]
if parseArgs.xp == True:
    xplist = ["ExpMultiplierFighter","ExpMultiplierThief","ExpMultiplierBlackBelt","ExpMultiplierRedMage","ExpMultiplierWhiteMage","ExpMultiplierBlackMage"]
    for x in xplist:
        del guardJson[x]
if parseArgs.blind == True:
    guardJson['BlindSeed'] = True
if parseArgs.levels == True:
    levelsList = ["StartingLevel","MaxLevelLow","MaxLevelHigh"]
    for l in levelsList:
        del guardJson[l]

# Get file list
btPath = workingDir + '/FF1Blazorizer/Tabs/'
libPath = workingDir + '/FF1Lib/'
fileList = os.listdir(btPath)
ignoreFiles = ['FunTab.razor','PresetsTab.razor', 'FileTab.razor', 'BlindSeedTab.razor', 'ExperimentalTab.razor', 'QoLTab.razor']
if parseArgs.experimental == True:
    ignoreFiles.remove('ExperimentalTab.razor')
flagTypes = ['CheckBox', 'TriStateCheckBox', 'EnumDropDown', 'DoubleSlider', 'Slider', 'IntSlider']
# Open Files one at a time, and begin building the flag dictionary
for razorFiles in fileList:
    if razorFiles in ignoreFiles:
        continue

    file = open(btPath + razorFiles, 'r')
    fline = file.readlines()
    
    for f in fline:
        if lineCont != 0:
            lineConcat = lastLine + f
            f = lineConcat

        lastLine = f
        
        # Strip out the extra cruft
        f = re.sub('\s+',' ',f)
        
        # If it's the PartyTab.razor file, gotta change it up a bit, since they're in tables.
        if razorFiles == 'PartyTab.razor':
            f = re.sub('<td class=*.*ty">','',f)

        # Get the first word after the first <
        fcs = f.find("<") + 1
        fce = f.find(" ", fcs) 
        ctype = f[fcs:fce]


        # If the line's not a flag, nor the continuation of a flag, skip it
        if ctype not in flagTypes and lineCont == 0:
            lineConcat = ""
            continue
         
        # Check to see if the line has the flag terminus in it
        endCheck = f.find(ctype, fce)
        if endCheck != -1:
            lineCont = 0
            lineConcat = ""
        else:
            lineCont = 1
            continue

        # Get the flag's name
        bvs = f.find("@bind-Value")
        if ctype == 'DoubleSlider':
            # Double Sliders are ...different.
            nos = f.find("(", bvs) + 7 # Offset by seven for the "(Flags." part before the name
            noe = f.find(",", bvs)
            flagName = f[nos:noe]
        else:
            fns = f.find('"', bvs) + 7
            fne = f.find('"', fns)
            flagName = f[fns:fne]
        flagName = flagName.replace('.', '')
        # Oh boy, let's fix some names that don't match. 
        match flagName:
            case "BetterTrapTreasure":
                flagName = "BetterTrapChests"
            case "FiendRefights":
                flagName = "PreserveFiendRefights"
                ctype = "TriStateCheckBox"
        # If it's a slider, get the min, max, and step value
        if ctype == "Slider" or ctype == "DoubleSlider" or ctype == "IntSlider":
            mif = f.find(" Min")
            mis = f.find('=', mif) + 2
            mie = f.find('"', mis + 1)
            maf = f.find(" Max")
            mas = f.find('=', maf) + 2
            mae = f.find('"', mas + 1)
            stf = f.find(" Step", mae)
            sts = f.find('=', stf) + 2
            ste = f.find('"', sts + 1)
            minv = int(f[mis:mie])
            maxv = int(f[mas:mae])
            stev = int(f[sts:ste])
            # Set the options for the dictionary
            flagOpts = [minv, maxv, stev]
        
        # If it's a drop down, get the number of options available
        elif ctype == "EnumDropDown":
            # Step 1: ensure that the count is cleared
            edcount = 0
            edi = 0
            # Step 2: Find the TItem for lib it belongs to
            tifs = f.find("TItem") + 7
            tife = f.find('"', tifs)
            titem = f[tifs:tife]
            findText = "public enum " + titem
            if titem == "SpoilerBatHints": # Hardcoding this until I can figure out why it's getting so many extra items returned
                edcount = 4
                continue
            libFile = searchText(libPath, findText)
            # Step 3: step through the file until you find the class.
            edfo = open(libFile, 'r')
            edfl = edfo.readlines()
            for el in edfl:
                edlc = el.find(findText)
                if edlc == -1 and edi == 0:
                    continue
                else:
                    edi = 1

                # Clean up Tabs and extra spaces
                el = el.strip(re.sub('\s',' ',el))

                # Skip empty lines
                if len(re.findall('\S',el)) < 1:
                    continue

                # Count all the pertinent lines only.

                dcount = el.find('[Description') + el.find('public enum') + el.find('{') + el.find('}') + el.find('==')

                if dcount == -5:
                    edcount += 1
                else:
                    pass

                ecount = el.find('}')
                if ecount != -1:
                    edi = 0
                    break

            # Close the file, because it's the right thing to do.
            edfo.close()

            # Set option value for the dictionary
            flagOpts = edcount 
        else:
            flagOpts = ctype


        # Determine any dependencies
        dcheck = f.find("IsEnabled")
        if dcheck != -1:
            # Find the dependency name
            dns = f.find('"', dcheck) + 1
            dne = f.find('"', dns)
            dname = f[dns:dne]
        else:
            dname = None

        # Add the entry to the dictionary
        flagDict[flagName] = [ctype, flagOpts, dname]
        # Add in the second checkbox for the fiend refights tickybox
        if flagName == "PreserveFiendRefights":
            flagDict["PreserveAllFiendRefights"] = [ctype, flagOpts, dname]

# Remove some unused flags that will cause error messages
deadFlags = ["KeyItemPlacementMode","LoosePlacementMode","ExpChestConversionHigh","ExpChestMinRewHigh","FiendsRefights","AllFighters","AllThiefs","AllBlackBelts","AllRedMages","AllWhiteMages","AllBlackMages","AllKnights","AllNinjas","AllMasters","AllRedWizards","AllWhiteWizards","AllBlackWizards","AllForced","AllNones"]
for d in deadFlags:
    try:
        del flagDict[d]
    except:
        pass

# Iterate through the dictionary and roll the value
for n, v in flagDict.items():
    ftype = v[0]

    match ftype:
        case "CheckBox":
            if random.randint(1,2) == 1:
                fvalue = False
            else:
                fvalue = True
            outputDict[n] = fvalue
        case "TriStateCheckBox":
            d3 = random.randint(1,3)
            if d3 == 1:
                fvalue = True
            elif d3 == 2:
                fvalue = False
            else:
                fvalue = None
            outputDict[n] = fvalue
        case "DoubleSlider":
            # The output name will be only the low value, need to get truncated name for max value
            # Except for some oddities. grump.
            tnl = len(n) - 3
            trueName = n[0:tnl]
            mn = trueName + "High"
            # Get the lowest common denominator to feed to the randint
            stepv = v[1][2]
            minval = v[1][0] / stepv
            maxval = v[1][1] / stepv
            minroll = random.randint(minval, maxval - 1)
            maxroll = random.randint(minroll, maxval)
            mirv = minroll * stepv
            marv = maxroll * stepv
            match n:
                case "ExpChestMinReward":
                    mn = "ExpChestMaxReward"
                case "ExpChestConversionMin":
                    mn = "ExpChestConversionMax"
            outputDict[n] = mirv
            outputDict[mn] = marv
        case "Slider" | "IntSlider":
            stepv = v[1][2]
            minval = v[1][0] / stepv
            maxval = v[1][1] / stepv
            rollv = random.randint(minval, maxval) * stepv
            # Exp Multiplier is odd in its calculations, have to step it down to a tenth
            match n:
                case "ExpMultiplier" | "ExpMultiplierFighter" | "ExpMultiplierThief" | "ExpMultiplierBlackBelt" | "ExpMultiplierRedMage" | "ExpMultiplierWhiteMage" | "ExpMultiplierBlackMage":
                    rollv = rollv / 10
            outputDict[n] = rollv
        case "EnumDropDown":
            maxv = v[1] - 1 # Reduce Volume by 1, as the dropdown are 0 indexed
            rollv = random.randint(0,maxv)
            # If deep dungone isn't disabled, make sure it doesn't roll
            if parseArgs.deepdungeon != True:
                if n == "GameMode":
                    while rollv == 1:
                        rollv = random.randint(0,maxv)
                
            outputDict[n] = rollv
        case _:
            print("Something's wrong, flag name: " + n + ", flag type: " + ftype)

# Set up the guard rails
for k, v in guardJson.items():
    outputDict[k] = v

# Make sure there's at least *some* way to save
if outputDict['DisableTentSaving'] == True and outputDict['DisableInnSaving'] == True and outputDict['SaveGameWhenGameOver'] == False:
    match random.randint(1,3):
        case 1:
            outputDict['DisableTentSaving'] = False
        case 2:
            outputDict['DisableInnSaving'] = False
        case 3:
            outputDict['SaveWhenGameOver'] = True

# If procgen overworld is turned on, use pregenerated map
    if outputDict['OwMapExchange'] == 1:
        outputDict['OwRandomPregen'] = True

ofDict = {"Name": fsName,
"Flags": outputDict}

ofJson = json.dumps(ofDict, indent=4)

outfile = open(ofName, 'w')
outfile.write(ofJson)
outfile.close()

#clean up after yourself
# Only if user directory is not specified
shutil.rmtree(workingDir)
