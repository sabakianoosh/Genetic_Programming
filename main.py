import random
import numpy as np
import math
import sys
sys.setrecursionlimit(1500)

def target_functionn(x):
    return 2*x + 10

    
class node:
    def __init__(self, data):
      self.data = data
      self.left = None
      self.right = None
      self.parent = None

    def replace_node(self,node):
        self.right = node.right
        self.left = node.left
        self.data = node.data
    

optr = ["+", "-", "*", "/", "^"]
Generations = []
inputs = [int(x) for x in np.random.uniform(1,20,10)]

class exp_tree:
    def __init__(self, postfix_exp): #[21x7*+*]
      self.exp = postfix_exp
      self.root = None
      self.parent = None
      self.createTree(self.exp)

    
    def __len__(self):
        return self.tree_len(self.root)

    def tree_len(self, node):
        if node is None:
            return 0
        else:
            return 1 + max(self.tree_len(node.right), self.tree_len(node.left))
        
    def isOperator(self, char):
      if char in optr: 
         return True 
      return False 
    def createTree(self, exp):
      s = []
      self.root = node(exp[-1])
     
      s.append(self.root)
   
      for i in range(len(exp)-2,-1,-1):
         curr_node = s[-1]
         if (curr_node.right==None):
            temp = node(exp[i])
            curr_node.right = temp
            curr_node.right.parent = curr_node

            if self.isOperator(exp[i]):
               s.append(temp)
         else:
            temp = node(exp[i])
            curr_node.left = temp
            curr_node.left.parent = curr_node
            
            s.pop() 
            if self.isOperator(exp[i]):
               s.append(temp)
  

def Generic_Select(n):
    if(len(Generations)>1):
        Last_Gen = Generations[-1]
        Last_Gen.sort(key=lambda x : x[1])
        Next_Gen = Last_Gen[:int(0.8*n)]
        Previous_Gen = Generations[-2]
        Previous_Gen.sort(key=lambda x : x[1])
        Next_Gen += Previous_Gen[:int(0.2*n)]
        Generations.append(Next_Gen)
    else:
        Last_Gen = Generations[-1]
        Last_Gen.sort(key=lambda x : x[1])
        Next_Gen = Last_Gen[:n]
        Generations.append(Next_Gen)

    

def Valid_Function(tree):
    errors = []
    for i in range(len(inputs)):
        mystack = []
        for x in tree:
            if(x not in optr):
                mystack.append(x)
            else:
                tmp1 = mystack.pop()
                tmp2 = mystack.pop()
                if(tmp1=='x'):
                    tmp1 = inputs[i]
                if(tmp2=='x'):
                    tmp2 = inputs[i]
                if(x == '+'):
                    mystack.append(tmp1+tmp2)
                if(x == '-'):
                    mystack.append(tmp1-tmp2)
                if(x == '^'):
                    if (tmp1>100):
                        tmp1 = 100
                    if (tmp2>5):
                        tmp2 = 5
                    if(tmp2<0):
                        tmp2 = abs(tmp2)
                    mystack.append(tmp1**tmp2)
                if(x == '*'):
                    if (tmp1 and tmp2 > 1000):
                        mystack.append(tmp1*tmp2)
                    else:
                        mystack.append(int((tmp1*tmp2)/1000))
                if(x == '/'):
                    if(tmp2==0):
                        tmp2 = 1
                    if (int(tmp1/tmp2)>0):
                        mystack.append(int(tmp1/tmp2))
                    else:
                        mystack.append(1)

        result = mystack.pop()
        error = (abs(result-target_functionn(inputs[i])))
        errors.append(error)
    return (sum(errors)/len(errors))



def exp_tree_input(n):
    trees = []
    treezzz = []
    for i in range(n):
        operators_num = np.random.randint(2,15)
        if(operators_num==0):
            trees.append([np.random.randint(1,10)])
        else:
            counter = 1
            length = operators_num*2 + 1 
            tree = []
            tree.append(np.random.randint(1,10))
            tree.append(np.random.randint(1,10))
            while(len(tree)!= length and ((length-len(tree))>counter)):
                to_select = np.random.randint(3)
                if(counter <=0 or to_select!=2):
                    if(to_select==0):
                        tree.append(np.random.randint(1,10))
                        counter += 1
                    elif(to_select==1):
                        tree.append('x')
                        counter += 1
                    else:
                        to_select = np.random.randint(2)
                        if(to_select==0):
                            tree.append(np.random.randint(1,10))
                            counter += 1
                        elif(to_select==1):
                            tree.append('x')
                            counter += 1
                else:
                    tree.append(np.random.choice(optr))
                    counter -= 1
            if not(length-len(tree)>counter):
                for i in range(counter):
                    tree.append(np.random.choice(optr))
            trees.append([tree,Valid_Function(tree)])
            et = exp_tree(tree)
            treezzz.append([et,Valid_Function(tree)])
        Generations.append(treezzz)

    return (trees)



def mutation():
    countTree2mutation = [int(x) for x in np.random.uniform(0,len(Generations[-1]),int(0.5*len(Generations[-1])))]
    for indtree in countTree2mutation:
        count2muation = np.random.randint(0,len(Generations[-1][indtree][0]))
        for i in range(count2muation):
            which2mutate = np.random.randint(1,math.log2(len(Generations[-1][0]))+1)
            tomutate = Generations[-1][indtree][0].root
            while(which2mutate>0):
                toselect = np.random.randint(2)
                if (toselect==0):
                    tomutate = tomutate.right
                    which2mutate -= 1
                else:
                    tomutate = tomutate.left
                    which2mutate -= 1

            if (tomutate.data in optr):
                tomutate.data = np.random.choice(optr)
            else:
                XorInt = np.random.randint(3)
                if (XorInt==1 or XorInt==1):
                    tomutate.data = np.random.randint(1,10)
                else:
                    tomutate.data = 'x'
    temp = Generations[-1][indtree][0]
    del Generations[-1][indtree]
    Generations[-1].append([temp,Valid_Function(temp.exp)])
    


def Crossover():
    tree2crossover = [int(x) for x in np.random.uniform(0,len(Generations[-1]),int(0.8*len(Generations[-1])))]
    while(len(tree2crossover)>1):
        indOftree1 = np.random.choice(tree2crossover)
        tree2crossover.remove(indOftree1)
        indOftree2 = np.random.choice(tree2crossover)
        tree2crossover.remove(indOftree2)

        rangetree1 = np.random.randint(0,math.log2(len(Generations[-1][indOftree1][0])))
        rangetree2 = np.random.randint(0,math.log2(len(Generations[-1][indOftree2][0])))

        node2crossover1 = Generations[-1][indOftree1][0].root
      
        while(rangetree1>0 ):
            toselect = np.random.randint(2)
            if (toselect == 0 and node2crossover1.right != None):
               
                node2crossover1 = node2crossover1.right
                rangetree1 -=1 
            if(toselect==1 and node2crossover1.left != None):
                
                node2crossover1 = node2crossover1.left
                rangetree1 -= 1
            else:
                rangetree1 -=1 
        node2crossover2 = Generations[-1][indOftree2][0].root
        while(rangetree2>0):
            toselect = np.random.randint(2)
            if (toselect == 0 and node2crossover2.right!=None):
                node2crossover2 = node2crossover2.right
                rangetree1 -=1 
            if( toselect == 1 and node2crossover2.left!=None):
                node2crossover2 = node2crossover2.left
                rangetree2 -= 1
            else:
                rangetree2 -= 1

        Generations[-1][indOftree1][0].root.right.replace_node(node2crossover2)
        Generations[-1][indOftree2][0].root.left.replace_node(node2crossover1)
        temp = Generations[-1][indOftree1][0]
        del Generations[-1][indOftree1]
        
        Generations[-1].append([temp,Valid_Function(temp.exp)])
        temp = Generations[-1][indOftree2][0]
        del Generations[-1][indOftree2]
        
        Generations[-1].append([temp,Valid_Function(temp.exp)])
    Generations[-1].sort(key=lambda x : x[1])        
    print(Generations[-1][1][1])






            
            


exp_tree_input(10)
Generic_Select(10)
mutation()
Crossover()



      


