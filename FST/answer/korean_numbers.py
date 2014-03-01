from myfst import fst
import sys, re

class korean_FST(fst.FST):
    def constructFST(self):
        for i in range(0,7):    #there are 7 states
            self.add_state(str(i))
        self.initial_state = '1'
        
        self.add_arc('1', '0', ('0'), (''))
        self.add_arc('0', '0', ('['), (''))
        self.add_arc('0', '0', ('1'), (''))
        self.add_arc('0', '0', ('0'), (''))
        self.add_arc('0', '0', ('^'), (''))
        self.add_arc('0', '0', ('2'), (''))
        self.add_arc('0', '0', ('3'), (''))
        self.add_arc('0', '0', ('4'), ('man '))
        self.add_arc('0', '1', (']'), (''))
        self.add_arc('0', '4', ('#'), (''))
        
        self.add_arc('1', '1', ('1'), ('il '))
        self.add_arc('1', '1', ('2'), ('i '))
        self.add_arc('1', '1', ('3'), ('sam '))
        self.add_arc('1', '1', ('4'), ('sa '))
        self.add_arc('1', '1', ('5'), ('o '))
        self.add_arc('1', '1', ('6'), ('yuk'))
        self.add_arc('1', '1', ('7'), ('chil '))
        self.add_arc('1', '1', ('8'), ('pal '))
        self.add_arc('1', '1', ('9'), ('gu '))
        
        self.add_arc('1', '2', ('['), (''))
        self.add_arc('2', '2', ('1'), (''))
        self.add_arc('2', '2', ('0'), (''))
        self.add_arc('2', '3', ('^'), (''))
        self.add_arc('3', '3', ('2'), ('baek '))
        self.add_arc('3', '3', ('3'), ('cheon '))
        self.add_arc('3', '3', ('4'), ('man '))
        self.add_arc('3', '5', ('8'), ('eok '))
        self.add_arc('3', '1', (']'), (''))
        self.add_arc('2', '1', (']'), ('sib '))   # ']' appears without '^'
        
        self.add_arc('1', '4', ('#'), (''))
        
        #5,6 are used to handle 1,0000,0000; once a non-zero number occurs, go back to 1        
        self.add_arc('5', '6', ('0'), (''))        
        self.add_arc('5', '1', ('1'), ('il '))
        self.add_arc('5', '1', ('2'), ('i '))
        self.add_arc('5', '1', ('3'), ('sam '))
        self.add_arc('5', '1', ('4'), ('sa '))
        self.add_arc('5', '1', ('5'), ('o '))
        self.add_arc('5', '1', ('6'), ('yuk'))
        self.add_arc('5', '1', ('7'), ('chil '))
        self.add_arc('5', '1', ('8'), ('pal '))
        self.add_arc('5', '1', ('9'), ('gu '))
        self.add_arc('5', '2', ('['), (''))
        self.add_arc('5', '5', (']'), (''))
         
        self.add_arc('6', '6', ('['), (''))
        self.add_arc('6', '6', ('1'), (''))
        self.add_arc('6', '6', ('0'), (''))
        self.add_arc('6', '6', ('^'), (''))
        self.add_arc('6', '6', ('2'), (''))
        self.add_arc('6', '6', ('3'), (''))
        self.add_arc('6', '6', ('4'), (''))
        self.add_arc('6', '5', (']'), (''))
        self.add_arc('6', '4', ('#'), (''))
        
        self.add_arc('5', '4', ('#'), (''))
        
        self.set_final('4')  
        
    def korean_transduce(self, expr):
        return ("".join(self.transduce(expr.split()))).rstrip()
         
def get_inter_expr(number):
    result = '#'
    loop_counter = 1       #a counter for three repeating count
    number = number[::-1]  #reverse the number
    for i in range(len(number)):
        digit = number[i]
        if loop_counter == 1:     # '1' is not ruled out for this position
            result = digit +' '+ result
        elif loop_counter == 2:
            if digit != '1':            
                result = digit +' '+'[ 1 0 ]'+' '+ result
            else:
                result = '[ 1 0 ]'+' '+ result
        elif loop_counter == 3:
            if digit != '1':
                result = digit +' '+ '[ 1 0 ^ 2 ]'+' '+ result
            else:
                result = '[ 1 0 ^ 2 ]'+' '+ result
        else:               #loop_counter == 4
            if digit != '1':
                result = digit +' '+'[ 1 0 ^ 3 ]'+' '+ result
            else:
                result = '[ 1 0 ^ 3 ]' +' '+ result     
            if (i+1 == 4) and (i+1 != len(number)): #when there is no more digit, don't add it
                result = '[ 1 0 ^ 4 ]' +' '+ result
            elif (i+1 == 8) and (i+1 != len(number)):
                result = '[ 1 0 ^ 8 ]' +' '+ result 
        loop_counter = 1 + loop_counter % 4
    if (number[len(number)-1] == '1') and (len(number)%4 == 1):
        result = result[2:]  #get rid of 1 if it is a lead digit
    return result
    
    
def preprocess(rawNumber):
    return ''.join(re.split(r",",rawNumber))

if __name__ == '__main__':
    f = korean_FST('korean')
    f.constructFST()
    print f.korean_transduce((get_inter_expr(preprocess('100001001'))))  
    #for line in sys.stdin:
     #   line = line[:-1]
      #  print f.korean_transduce((get_inter_expr(preprocess(line))))    
    