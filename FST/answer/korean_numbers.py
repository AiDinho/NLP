from myfst import fst
import sys, re

class korean_FST(fst.FST):
    def constructFST(self):
        for i in range(1,16):    #there are 15 states
            self.add_state(str(i))
            
            self.initial_state = '1'
              
            self.add_arc('1', '2', ('a'), ('1'))
        
            self.set_final('14')  
        
    def korean_transduce(self, expr):
        print expr
        #expr = "a b a b b".split()
        return self.transduce(expr)
         
def get_inter_expr(number):
    result = '#'
    loop_counter = 1       #a counter for three repeating count
    mag_counter = 1
    number = number[::-1]  #reverse the number
    for digit in number:
        if loop_counter == 1:
            result = digit + result
        elif loop_counter == 2:
            if digit != '1':            
                result = digit + '[10]' + result
            else:
                result = '[10]' + result
        elif loop_counter == 3:
            if digit != '1':
                result = digit + '[10^2]' + result
            else:
                result = '[10^2]' + result
        else:               #loop_counter == 4
            if digit != '1':
                result = digit + '[10^3]' + result
            else:
                result = '[10^3]' + result     
            if mag_counter == 4:
                result = '[10^4]' + result
            elif mag_counter == 8:
                result = '[10^8]' + result 
        loop_counter = 1 + loop_counter % 4
        mag_counter = mag_counter + 1
    if (number[len(number)-1] == '1') and (len(number)%4 == 1):
        result = result[1:]  #get rid of 1 if it is a lead digit
    return result
    
    
def preprocess(rawNumber):
    return ''.join(re.split(r",",rawNumber))

if __name__ == '__main__':
    f = korean_FST('korean')
    f.constructFST()
    if len(sys.argv) > 1:
        f.korean_transduce((get_inter_expr(preprocess(sys.argv[1]))))
    else:
        print f.korean_transduce(get_inter_expr(preprocess('100,100,000')))        
        #print "Please input a number to transduce"        
    