import math
import pandas #Pandas is a python library that handles excel file import

class ID3:
    def __init__(self):
        self._tree = {}
        self._totalstep = 1
        pass
    
    def train(self, rawData):
        #Set up a dictionary to keep track of splits
        splitDict = {'outlook':True, 'temperature':True, 'humidity':True, 'wind':True, 'play':True}
        self.buildTree('play', rawData, splitDict)
        
    def findEntropy(self, item, data, target='no'):
        labels = ['Outlook','Temperature','Humidity','Windy']
        p = 0
        q = len(data.index)
        total = 0
        for i in range(len(data.index)):
            if target == 'play':
                if data.iloc[i]['Play'] == "Yes": 
                    p = p + 1
                    q = q - 1
                    total = len(data.index)
            else:
                for j in labels:
                    if data.iloc[i][j] == item:
                        total = total + 1
                        if data.iloc[i]['Play'] == "Yes": 
                            p = p+1
                            total = total-1
        #Entropy calc breakdown by N. Wouda
        if target == 'play':
            x = (p/(total))
            y = (q/(total))
        else:
            if p == 0:
                return 0
            x = (p/(p+total))
            y = (total/(p+total))
        if x == 0 or x == 1:
            return 0
        else:
            return(-(x*math.log2(x))+ -(y*math.log2(y)))
    
    def buildTree(self, category, data, splitDict, entropyCat = '0'):
        #Remove category from splits as it no longer factors in
        splitDict[category] = False            
        
        #Then determine entropy of the values
        if splitDict['outlook']:
            sunnyEntropy = self.findEntropy("Sunny", data)
            overcastEntropy = self.findEntropy("Overcast", data)
            rainyEntropy = self.findEntropy("Rainy", data)
        if splitDict['temperature']:
            hotEntropy = self.findEntropy("Hot", data)
            mildEntropy = self.findEntropy("Mild", data)
            coldEntropy = self.findEntropy("Cold", data)
        if splitDict['humidity']:
            highEntropy = self.findEntropy("High", data)
            normalEntropy = self.findEntropy("Normal", data)
        if splitDict['wind']:
            windtEntropy = self.findEntropy("Yes", data)
            windfEntropy = self.findEntropy("No", data)

        if category == 'play':
            entropyCat = self.findEntropy("Yes", data, 'play')
        
        #Count all instances of values:
        sunny = 0
        overcast = 0
        rainy = 0
        hot = 0
        mild = 0
        cold = 0
        high = 0
        normal = 0
        windt = 0
        windf = 0
        total = 0
        
        sunnyP = 0
        overcastP = 0
        rainyP = 0
        hotP = 0
        mildP = 0
        coldP = 0
        highP = 0
        normalP = 0
        windtP = 0
        windfP = 0
        
        for i in range(len(data.index)):
            if data.iloc[i]['Outlook']== 'Sunny':
                sunny = sunny+1
                if data.iloc[i]['Play']== 'Yes':
                    sunnyP = sunnyP+1
            if data.iloc[i]['Outlook'] == 'Overcast':
                overcast = overcast+1
                if data.iloc[i]['Play']== 'Yes':
                    overcastP = overcastP+1
            if data.iloc[i]['Outlook'] == 'Rainy':
                rainy = rainy+1
                if data.iloc[i]['Play']== 'Yes':
                    rainyP = rainyP+1
            if data.iloc[i]['Temperature'] == 'Hot':
                hot = hot+1
                if data.iloc[i]['Play']== 'Yes':
                    hotP = hotP+1
            if data.iloc[i]['Temperature'] == 'Mild':
                mild = mild+1
                if data.iloc[i]['Play']== 'Yes':
                    mildP = mildP+1
            if data.iloc[i]['Temperature'] == 'Cold':
                cold = cold+1
                if data.iloc[i]['Play']== 'Yes':
                    coldP = coldP+1
            if data.iloc[i]['Humidity'] == 'High':
                high = high+1
                if data.iloc[i]['Play']== 'Yes':
                    highP = highP+1
            if data.iloc[i]['Humidity'] == 'Normal':
                normal = normal+1
                if data.iloc[i]['Play']== 'Yes':
                    normalP = normalP+1
            if data.iloc[i]['Windy'] == 'Yes':
                windt = windt+1
                if data.iloc[i]['Play']== 'Yes':
                    windtP = windtP+1
            if data.iloc[i]['Windy'] == 'No':
                windf = windf+1
                if data.iloc[i]['Play']== 'Yes':
                    windfP = windfP+1
            total = total + 1
        
        #Then determine the information gain for each
        if splitDict['outlook']:
            outlookGain = entropyCat - (((sunny/total)*sunnyEntropy)+((overcast/total)*overcastEntropy)+((rainy/total)*rainyEntropy))
        else:
            outlookGain = 0
        if splitDict['temperature']:
            tempGain = entropyCat - (((hot/total)*hotEntropy)+((mild/total)*mildEntropy)+((cold/total)*coldEntropy))
        else: tempGain = 0
        if splitDict['humidity']:
            humidGain = entropyCat - (((high/total)*highEntropy)+((normal/total)*normalEntropy))
        else: humidGain = 0
        if splitDict['wind']:
            windGain = entropyCat - (((windt/total)*windtEntropy)+((windf/total)*windfEntropy))
        else: windGain = 0
            
        #Append all values to a list as tuples
        valueList = [('outlook',outlookGain),('temperature',tempGain),('humidity',humidGain),('wind',windGain)]
        
        #Find highest gain, keep duplicates
        num = 0
        for i in valueList:
            if num < i[1]:
                num = i[1]
        for i in valueList:
            if i[1] == num:
                highestGain = i
        if splitDict['outlook'] == False and splitDict['humidity'] == False and splitDict['temperature'] == False and splitDict['wind'] == False:
            for i in valueList:
                if i[0] == category.lower():
                    highestGain = i
                    
                
        #Add decision to tree
        treeNode = {}
        split1 = "y"
        split2 = "y"
        split3 = "y"

        #Outlook
        if highestGain[0] == 'outlook':
            #Sunny
            if sunnyEntropy == 0:
                if sunnyP != 0:
                    treeNode['Sunny'] = 'T'
                else:
                    treeNode['Sunny'] = 'F'
                split1 = 'N'
            else:
                if splitDict['humidity'] == False and splitDict['temperature'] == False and splitDict['wind'] == False:
                    treeNode['Sunny'] = str(sunnyP) + "/" + str(sunny)
                    split1 = 'N'
                else:
                    treeNode['Sunny'] = self._totalstep + 1
                    self._totalstep = self._totalstep + 1
            #Overcast
            if overcastEntropy == 0:
                if overcastP != 0:
                    treeNode['Overcast'] = 'T'
                else:
                    treeNode['Overcast'] = 'F'
                split2 = 'N'
            else:
                if splitDict['humidity'] == False and splitDict['temperature'] == False and splitDict['wind'] == False:
                    treeNode['Overcast'] = str(overcastP) + "/" + str(overcast)
                    split2 = 'N'
                else:
                    treeNode['Overcast'] = self._totalstep + 1
                    self._totalstep = self._totalstep + 1
            #Rainy
            if rainyEntropy == 0:
                if rainyP != 0:
                    treeNode['Rainy'] = 'T'
                else:
                    treeNode['Rainy'] = 'F'
                split3 = 'N'
            else:
                if splitDict['humidity'] == False and splitDict['temperature'] == False and splitDict['wind'] == False:
                    treeNode['Rainy'] = str(rainyP) + "/" + str(rainy)
                    split3 = 'N'
                else:
                    treeNode['Rainy'] = self._totalstep + 1
                    self._totalstep = self._totalstep + 1
        #Temperature
        if highestGain[0] == 'temperature':
            #Hot
            if hotEntropy == 0:
                if hotP != 0:
                    treeNode['Hot'] = 'T'
                else:
                    treeNode['Hot'] = 'F'
                split1 = 'N'
            else:
                if splitDict['outlook'] == False and splitDict['humidity'] == False and splitDict['wind'] == False:
                    treeNode['Hot'] = str(hotP) + "/" + str(hot)
                    split1 = 'N'
                else:
                    treeNode['Hot'] = self._totalstep + 1
                    self._totalstep = self._totalstep + 1
            #Mild
            if mildEntropy == 0:
                if mildP != 0:
                    treeNode['Mild'] = 'T'
                else:
                    treeNode['Mild'] = 'F'
                split2 = 'N'
            else:
                if splitDict['outlook'] == False and splitDict['humidity'] == False and splitDict['wind'] == False:
                    treeNode['Mild'] = str(mildP) + "/" + str(mild)
                    split2 = 'N'
                else:
                    treeNode['Mild']: self._totalstep + 1
                    self._totalstep = self._totalstep + 1
            #Cold
            if coldEntropy == 0:
                if rainyP != 0:
                    treeNode['Cold'] = 'T'
                else:
                    treeNode['Cold'] = 'F'
                split3 = 'N'
            else:
                if splitDict['outlook'] == False and splitDict['humidity'] == False and splitDict['wind'] == False:
                    treeNode['Cold'] = str(coldP) + "/" + str(cold)
                    split3 = 'N'
                else:
                    treeNode['Cold'] = self._totalstep + 1
                    self._totalstep = self._totalstep + 1
        
        #Humidity            
        if highestGain[0] == 'humidity':
            #High
            if highEntropy == 0:
                if highP != 0:
                    treeNode['High'] = 'T'
                else:
                    treeNode['High'] = 'F'
                split1 = 'N'
            else:
                if splitDict['outlook'] == False and splitDict['temperature'] == False and splitDict['wind'] == False:
                    treeNode['High'] = str(highP) + "/" + str(high)
                    split1 = 'N'
                else:
                    treeNode['High'] = self._totalstep + 1
                    self._totalstep = self._totalstep + 1
            #Normal
            if normalEntropy == 0:
                if normalP != 0:
                    treeNode['Normal'] = 'T'
                else:
                    treeNode['Normal'] = 'F'
                split2 = 'N'
            else:
                if splitDict['outlook'] == False and splitDict['temperature'] == False and splitDict['wind'] == False:
                    treeNode['Normal'] = str(normalP) + "/" + str(normal)
                    split2 = 'N'
                else:
                    treeNode['Normal'] = self._totalstep + 1
                    self._totalstep = self._totalstep + 1
        
        #Windy
        if highestGain[0] == 'wind':
            #Yes
            if windtEntropy == 0:
                if windtP != 0:
                    treeNode['Yes'] = 'T'
                else:
                    treeNode['Yes'] = 'F'
                split1 = 'N'
            else:
                if splitDict['outlook'] == False and splitDict['humidity'] == False and splitDict['temperature'] == False:
                    treeNode['Yes'] = str(windtP) + "/" + str(windt)
                    split1 = 'N'
                else:
                    treeNode['Yes'] = self._totalstep + 1
                    self._totalstep = self._totalstep + 1
            #No
            if windfEntropy == 0:
                if windfP != 0:
                    treeNode['No'] = 'T'
                else:
                    treeNode['No'] = 'F'
                split2 = 'N'
            else:
                if splitDict['outlook'] == False and splitDict['humidity'] == False and splitDict['temperature'] == False:
                    treeNode['No'] = str(windfP) + "/" + str(windf)
                    split2 = 'N'
                else:
                    treeNode['No'] = self._totalstep + 1
                    self._totalstep = self._totalstep + 1
        step = 1
        while step in self._tree:
            step = step + 1
        self._tree[step]= treeNode
        
        #Split recursively until tree is fully constructed. Tree is represented as an array of dictionaries.
        if highestGain[0] == 'humidity':
            if split1 != 'N':
                highData = data[data['Humidity'] == 'High']
                self.buildTree(highestGain[0], highData, splitDict, highEntropy)                
            if split2 != 'N':
                normalData = data[data['Humidity'] == 'Normal']
                self.buildTree(highestGain[0], normalData, splitDict, normalEntropy)
                
        if highestGain[0] == 'wind':
            if split1!= 'N':
                windtData = data[data['Windy'] == 'Yes']
                self.buildTree(highestGain[0], windtData, splitDict, windtEntropy)  
            if split2 != 'N':
                windfData = data[data['Windy'] == 'No']
                self.buildTree(highestGain[0], windfData, splitDict, windfEntropy)
                
        if highestGain[0] == 'outlook':
            if split1 != 'N':
                sunnyData = data[data['Outlook'] == 'Sunny']
                self.buildTree(highestGain[0], sunnyData, splitDict, sunnyEntropy)
            if split2 != 'N':
                overcastData = data[data['Outlook'] == 'Overcast']
                self.buildTree(highestGain[0], overcastData, splitDict, overcastEntropy)
            if split3 != 'N':
                rainyData = data[data['Outlook'] == 'Rainy']
                self.buildTree(highestGain[0], rainyData, splitDict, rainyEntropy)
            
        if highestGain[0] == 'temperature':
            if split1 != 'N':
                hotData = data[data['Temperature'] == 'Hot']
                self.buildTree(highestGain[0], hotData, splitDict, hotEntropy)
            if split2 != 'N':
                mildData = data[data['Temperature'] == 'Mild']
                self.buildTree(highestGain[0], mildData, splitDict, mildEntropy)
            if split3 != 'N':
                coldData = data[data['Temperature'] == 'Cold']
                self.buildTree(highestGain[0], coldData, splitDict, coldEntropy)
            

    def classify(self, record, step = 1):
        #Records should be formatted as a list object.
        #Navigate the decision tree based on these values      
        for i in record:                                                    #Iterate through the record
            for x in self._tree[step]:                                      #Find the node at the given step of the tree and iterate
                if i == x:                                                  #Check if the node is equal to the value
                    if self._tree[step][x] == 'T':                          
                        return('Yes')                                       #Play is true
                    elif self._tree[step][x] == 'F':
                        return('No')                                        #Play is false
                    elif type(self._tree[step][x]) is int:
                        return(self.classify(record, self._tree[step][x]))  #Recursively check the next step of the tree.
                    else:
                        prob = int(self._tree[step][x][0]) / int(self._tree[step][x][2])
                        if prob < 0.5:
                            return("No")
                        else:
                            return("Yes")
                        return(self._tree[step][x])                         #Return unsure values
                        
    def displayTree(self):
        print()
        print("Tree Reading: ")
        print("Index: {'Item': [Next Index, T, F, Play Chance]}")
        print("T means the user will play, F means they will not play.")
        print("Fractions are represented like so: number of days they played / total number of days")
        print("Fractions are evaluated to true or false based on their probability.")
        print()
        for i in self._tree:
            print(str(i) + ": " + str(self._tree[i]))
        return(self._tree)
        
#Testing Data
data = pandas.read_excel(r'TestingData.xlsx', sheet_name='Sheet')
example = ID3()
example.train(data)
newitem = ['Sunny', 'Hot', 'High', 'Normal']
print(example.classify(newitem))
example.displayTree()

#Runs training algorithm and outputs a result
data = pandas.read_excel(r'LabData.xlsx', sheet_name='Sheet')
example = ID3()
example.train(data)

print(example.classify(['Sunny', 'Mild', 'Normal', 'No']))

print(example.classify(['Overcast', 'Hot', 'Normal', 'Yes']))

print(example.classify(['Rainy', 'Hot', 'High', 'Yes']))

example.displayTree()
