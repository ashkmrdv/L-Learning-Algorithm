import pandas as pd
import numpy as np
import random as rd
import string as st
import math as mt

# Constants
 
# DFA to accept three consecutive 'a's

# ACTUALTRANSITION={0:{'':0,'a':1, 'b':0},
#      1:{'':1,'a':2, 'b':0},
#      2:{'':2,'a':3, 'b':0},
#      3:{'':3,'a':1,'b':3}}
# ACTUALINITIAL=0
# ACTUALSTATES=[0,1,2,3]
# ACTUALFINAL=[3]

# DFA to accept even number of 'a's and 'b's

ACTUALTRANSITION={0:{'':0,'a':1, 'b':2},
     1:{'':1,'a':0, 'b':3},
     2:{'':2,'a':3, 'b':0},
     3:{'':3,'a':2,'b':1}
}
ACTUALINITIAL=0
ACTUALSTATES=[0,1,2,3]
ACTUALFINAL=[0]

# DFA that accepts any string to check edge case 

# ACTUALTRANSITION={0:{'':0,'a':0, 'b':0}
# }
# ACTUALINITIAL=0
# ACTUALSTATES=[0]
# ACTUALFINAL=[0]

#4  DFA that starts with 'a' 

# ACTUALTRANSITION={0:{'':0,'a':1, 'b':2},
#      1:{'':1,'a':1, 'b':1},
#      2:{'':2,'a':2, 'b':2}
# }
# ACTUALINITIAL=0
# ACTUALSTATES=[0,1,2]
# ACTUALFINAL=[1]

# 5 DFA that accepts only the input a few inputs with dead states

# ACTUALTRANSITION={0:{'':0,'a':0, 'b':1},
#      1:{'':1,'a':2, 'b':1},
#      2:{'':2,'a':2, 'b':2}
# }
# ACTUALINITIAL=0
# ACTUALSTATES=[0,1,2]
# ACTUALFINAL=[0,1]

# DFA for the Rivest Schapire example

# ACTUALTRANSITION={0:{'':0,'a':1, 'b':1},
#      1:{'':1,'a':2, 'b':0},
#      2:{'':2,'a':2, 'b':3},
#      3:{'':3,'a':0,'b':2}}
# ACTUALINITIAL=0
# ACTUALSTATES=[0,1,2,3]
# ACTUALFINAL=[1,2]

# Constants

EPSILON=''
ALPHABET=[EPSILON,'a','b']
ACTUALDFA=[ACTUALTRANSITION,ACTUALINITIAL,ACTUALFINAL,ACTUALSTATES]
COUNTEREXAMPLE=['']
COUNT=0

# Equivalence query: To check whether two DFAs are equal

def EquivalenceQuery(Learned):
    
    if(Learned==ACTUALDFA):
        return True
    else:
        return False

# Membership query: To check whether an input string is a part of the DFA

def MembershipQuery(String):
    global COUNT
    COUNT+=1

    if (AlphabetCheck(String,ALPHABET)==True):

        CurrState = ACTUALDFA[1]
        FinalState=ACTUALDFA[2]
        dfa=ACTUALDFA[0]

        for Char in String:
            CurrState = dfa[CurrState][Char]

        return int(CurrState in FinalState)
    
    else: 
        return 0

# Alphabet check : To check whether an input string is a part of a particular alphabet

def AlphabetCheck(String,ALPHABET):
    Alpha=True

    for Char in String:
        if Char in ALPHABET:
            Alpha=True
            continue
        else:
            Alpha =False
            break
    
    return Alpha

# Initialise the Observation table 

def Initialize():
    Columns=[EPSILON]
    Index1=[EPSILON]
    Index2=['a','b']

    Table1 = pd.DataFrame(columns=Columns,index=Index1)
    Table2 = pd.DataFrame(columns=Columns,index=Index2)

    return BuildObservationTable(Table1,Table2)

# Filling up the entries of Observation table using membership queries 

def BuildObservationTable(Table1,Table2):
    Index1=list(Table1.index)
    Index2=list(Table2.index)
    Columns=list(Table1.columns)

    Array1=np.array(Table1)
    Array2=np.array(Table2)

    for i in range (len(Index1)):
        for j in range (len(Columns)):
            Array1[i][j]=MembershipQuery(Index1[i]+Columns[j])

            Array1[i][j]=MembershipQuery(Index1[i]+Columns[j])

    for i in range (len(Index2)):
        for j in range (len(Columns)):
            Array2[i][j]=MembershipQuery(Index2[i]+Columns[j])

            Array2[i][j]=MembershipQuery(Index2[i]+Columns[j])
    
    Table1_new = pd.DataFrame(Array1,columns=Columns,index=Index1)
    Table2_new = pd.DataFrame(Array2,columns=Columns,index=Index2)


    return Table1_new,Table2_new

# Check the closedness of the observation Table

def CheckClosedness(Table1,Table2):
    Array1=np.array(Table1)
    Array2=np.array(Table2)
    for i in range (len(Array1)):
        temp=''
        Array1[i]=temp.join(str(Array1[i]))
    
    for i in range (len(Array2)):
        temp=''
        Array2[i]=temp.join(str(Array2[i]))

    for i in range(len(Array2)):
        if Array2[i] not in Array1:
            return False
    
    return True

# Variable to be chosen for the next column

def ColumnVariable(Table1,Table2):
    Array1=np.array(Table1).tolist()
    Array2=np.array(Table2).tolist()
    Array=Array1+Array2
    Index1=list(Table1.index)
    Index2=list(Table2.index)
    Index=Index1+Index2
    Columns=list(Table1.columns)

    compare=[]

    for i in range (len(Array1)-1):
        j=i+1
        while(j<len(Array1)):
            if Array1[i]==Array1[j]:
                compare.append([i,j])
            j=j+1
    
    for i in range (len(compare)):
        for j in range (len(ALPHABET)):
            for k in range (len(Columns)):
                value1=MembershipQuery(Index1[compare[i][0]]+ALPHABET[j]+Columns[k])
                value2=MembershipQuery(Index1[compare[i][1]]+ALPHABET[j]+Columns[k])

                if value1!=value2:
                    value=ALPHABET[j]+Columns[k]
                    if value not in Columns:
                        return value
    
    return None
    
# Check the consistency of the table

def CheckConsistency(Table1,Table2):
    Array1=np.array(Table1).tolist()
    Array2=np.array(Table2).tolist()
    Array=Array1+Array2
    Index1=list(Table1.index)
    Index2=list(Table2.index)
    Index=Index1+Index2
    Columns=list(Table1.columns)

    compare=[]

    for i in range (len(Array1)-1):
        j=i+1
        while(j<len(Array1)):
            if Array1[i]==Array1[j]:
                compare.append([i,j])
            j=j+1
    
    for i in range (len(compare)):
        for j in range (len(ALPHABET)):
            for k in range (len(Columns)):
                value1=MembershipQuery(Index1[compare[i][0]]+ALPHABET[j]+Columns[k])
                value2=MembershipQuery(Index1[compare[i][1]]+ALPHABET[j]+Columns[k])

                if value1!=value2:
                    return False
    return True

# Add a row in the upper side of the table

def AddRow(Table1,Table2):

    Index1=list(Table1.index)
    Index2=list(Table2.index)
    Columns=list(Table1.columns)

    Array1=np.array(Table1).tolist()
    Array2=np.array(Table2).tolist()

    Array1.append(Array2[0])
    Array2.pop(0)

    Index1.append(Index2[0])
    Index2=PrefixClosed(Index1)

    Table1_new = pd.DataFrame(columns=Columns,index=Index1)
    Table2_new = pd.DataFrame(columns=Columns,index=Index2)

    T1,T2=BuildObservationTable(Table1_new,Table2_new)

    return T1,T2

# Add a column in the table

def AddColumn(Table1,Table2):
    Index1=list(Table1.index)
    Index2=list(Table2.index)
    Columns=list(Table1.columns)
    
    Append=ColumnVariable(Table1,Table2)

    if Append!=None:
        Columns.append(Append)
        
        Table1_new = pd.DataFrame(columns=Columns,index=Index1)
        Table2_new = pd.DataFrame(columns=Columns,index=Index2)
        T1,T2=BuildObservationTable(Table1_new,Table2_new)
        
        return T1,T2
    
    else: 
        return Table1,Table2

# Create a prefix closed set of strings from the given row headers

def PrefixClosed(label):
    Final=[]

    for i in range (len(label)):
        for j in range (len(ALPHABET)):
            temp=label[i]+ALPHABET[j]
            if (temp not in Final)&(temp not in label):
                Final.append(label[i]+ALPHABET[j])
    
    return Final

# Construct DFA from Dataframe 

def DataframetToDfa(Table1,Table2):
    Index1=list(Table1.index)
    Index2=list(Table2.index)
    Index=Index1+Index2
    Columns=list(Table1.columns)

    Array1=np.array(Table1).tolist()
    Array2=np.array(Table2).tolist()
    Array=Array1+Array2

    LearnedTransition_test={}
    LearnedInitial_test=0
    LearnedFinal_test=[]
    LearnedStates_test=[]

    LearnedRows_test=[]
    LearnedStrings_test=[]
    row=0
    for i in range (len(Index1)):
        if Array1[i] not in LearnedRows_test:
            LearnedStates_test.append(row)
            row=row+1
            LearnedRows_test.append(Array1[i])
            LearnedStrings_test.append(Index1[i])

    for i in range (len(LearnedStates_test)):
        temp={}
        for j in range (len(ALPHABET)):
            String=LearnedStrings_test[i]+ALPHABET[j]
            I=Index.index(String)
            Row=Array[I]
            Append=LearnedRows_test.index(Row)

            temp[ALPHABET[j]]=Append
        
        LearnedTransition_test[i]=temp
    
    for i in range (len(LearnedStates_test)):
        for j in range (len(ALPHABET)):
            String=LearnedStrings_test[i]+ALPHABET[j]
            I=Index.index(String)
            Row=Array[I]
            State=LearnedRows_test.index(Row)
            Append=LearnedStrings_test[State]
            if (MembershipQuery(Append)==1)&(State not in LearnedFinal_test)&(State in LearnedStates_test):
                LearnedFinal_test.append(State)


    LearnedDfa_test=[LearnedTransition_test,LearnedInitial_test,LearnedFinal_test,LearnedStates_test]

    return (LearnedDfa_test)

# Returns the Output sequence 

def OutputSequence(State,Sequence):
    Output=''

    if State in ACTUALFINAL:
        Output+='1'
    else:
        Output+='0'
    
    if Sequence==None or Sequence=='':
        return Output
    else:
        for i in range (len(Sequence)):
        
            temp=ACTUALTRANSITION[State]
            State=temp[Sequence[i]]

            if State in ACTUALFINAL:
                Output+='1'
            else:
                Output+='0'
    
        return Output

# Returns the Output state 

def OutputState(Dfa,State,Sequence):
    if Sequence=='' or Sequence ==None:
        return State
    
    Transition,Initial,Final,States=Dfa

    for i in range (len(Sequence)):
        
        temp=Transition[State]
        State=temp[Sequence[i]]
    
    return State

# Return the output value of the learne DFA from the initial state

def OutputValue(Dfa,Sequence):

    if (AlphabetCheck(Sequence,ALPHABET)==True):

        CurrState = Dfa[1]
        FinalState=Dfa[2]
        dfa=Dfa[0]

        for Char in Sequence:
            CurrState = dfa[CurrState][Char]

        return int(CurrState in FinalState)
    
    else: 
        return 0

# Generate Strings for counterexample

def GenerateCounterExample():
    
    for i in range (len(COUNTEREXAMPLE)):
        for j in range (len(ALPHABET)):
            value=COUNTEREXAMPLE[i]+ALPHABET[j]
            if value not in COUNTEREXAMPLE:
                COUNTEREXAMPLE.append(COUNTEREXAMPLE[i]+ALPHABET[j])

# Return the right Counterexample

def CounterExample(Dfa):
    while(1):
        for i in range (len(COUNTEREXAMPLE)):
            if (OutputValue(Dfa,COUNTEREXAMPLE[i])!=MembershipQuery(COUNTEREXAMPLE[i])):
                return COUNTEREXAMPLE[i]
        GenerateCounterExample()

# Return the Index of the string

def Alpha(Dfa,counter,index):
    
    state_1=OutputState(Dfa,0,counter[0:index])
    state_2=OutputState(ACTUALDFA,state_1,counter[index:len(counter)])

    if state_2 in ACTUALFINAL:
        return 1
    else:
        return 0

# Return the two components of the string

def BinarySearch(Dfa,counter):
    low_index=0
    high_index=len(counter)-1
    mid_index=0
    low_string=''
    State_1=Alpha(Dfa,counter,0)
    State_2=Alpha(Dfa,counter,len(counter))
    
    while low_index<=high_index:
        mid_index=((low_index+high_index)//2)
        low_string=counter[0:mid_index]

        if Alpha(Dfa,counter,mid_index)!= Alpha(Dfa,counter,mid_index+1):
            break
        elif (Alpha(Dfa,counter,mid_index)==State_1) and (Alpha(Dfa,counter,mid_index)==State_1):
            low_index=mid_index
        elif (Alpha(Dfa,counter,mid_index)==State_2) and (Alpha(Dfa,counter,mid_index)==State_2):
            high_index=mid_index

    high_string=counter[mid_index+1:len(counter)]
    B=counter[mid_index]
    low_string=counter[0:mid_index]

    return(low_string,B,high_string)

# Performing the Rivest Schapire improvement

def Rivest(Dfa,Table1,Table2):
    Value=CounterExample(Dfa)
    S,b,R=BinarySearch(Dfa,Value)
    
    Index1=list(Table1.index)
    Index2=list(Table2.index)
    Columns=list(Table1.columns)

    if (S+b) not in Index1 and len(S+b)!=0 and S!=None:
        Index1.append(S+b)
    if R not in Columns and len(R)!=0 and R!=None:
        Columns.append(R)
    
    Index1,Index2=PrefixclosedRivest(Index1)
    Columns=SuffixClosedRivest(Columns)

    Table1_new = pd.DataFrame(columns=Columns,index=Index1)
    Table2_new = pd.DataFrame(columns=Columns,index=Index2)


    T1,T2=BuildObservationTable(Table1_new,Table2_new)

    return T1,T2

# Return the prefix closed set of strings

def PrefixclosedRivest(List):
    Index1=List.copy()
    Index2=[]
    for i in range (len(List)):
        value=List[i][0:len(List)-1]

        if value not in Index1:
            Index1.append(value)
    
    for i in range (len(Index1)):
        for j in range (len(ALPHABET)):
            value=Index1[i]+ALPHABET[j]

            if value not in Index1:
                Index2.append(value)

    
    return Index1,Index2

# Return the suffix closed set of strings

def SuffixClosedRivest(List):
    for i in range (len(List)):
        value=List[i][:-1]
        if value not in List:
            List.append(value)

    return List

# main

Table1,Table2=Initialize()

while(1):
    while(CheckConsistency(Table1,Table2)!=True):
        Table1,Table2=AddColumn(Table1,Table2)
    
    while(CheckClosedness(Table1,Table2)!=True):
        Table1,Table2=AddRow(Table1,Table2)
    
    LearnedDfa=DataframetToDfa(Table1,Table2)

    if EquivalenceQuery(LearnedDfa)==1:
        break

    while(CheckClosedness(Table1,Table2)!=True):
        Table1,Table2=AddRow(Table1,Table2)
    
    while(CheckConsistency(Table1,Table2)!=True):
        Table1,Table2=AddColumn(Table1,Table2)
    
    LearnedDfa=DataframetToDfa(Table1,Table2)
    Table1,Table2=Rivest(LearnedDfa,Table1,Table2)

print("Learned DFA is as follows")
print(LearnedDfa)
print("The number of times the Membership Query is called")
print(COUNT)
print("The Upper half of the Observation table")
print(Table1)
print("The Lower half of the obsercation table")
print(Table2)