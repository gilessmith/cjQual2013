
class CodeJamRunner(object):

    def execute(self):
        with open('%s-%s.in' % (self.problem_name,self.problem_size)) as f:
            case_count = int(f.readline())
            case =0
            results = []
            while case<case_count:
                results.append(self.execute_case(self.get_case_data(f)))

                case += 1

        with open('%s-%s.out' %
                           (self.problem_name,
                            self.problem_size), 'w') as output:
             for i, result in enumerate(results):
                 output.write('Case #%s: %s\n' % (i+1, result))


class FairAndSquareJam(CodeJamRunner):
    problem_name = 'C'
    problem_size = 'large-2'
    
    def get_case_data(self, f):
        level_size = [int(x) for x in f.readline().strip().split(' ')]
        return level_size

    def is_palendrome(self, num):
        st = str(num)
        return st == st[::-1]
    
    def enumer(self, l):
        a = ['0'] * l
        results =[''.join(a)]
        for m in range(1, min(4,l)+1):
            b = [i for i in range(m)]  #[0, 1, 2]
            while True:

                base = a[:]
                for index in b:
                    base[index] = '1'
                results.append(''.join(base))

                try:
                    # this needs generalising
                    if b[-1] < l-1:
                        b[-1] += 1
                    else:
                        if b[-2]<b[-1] -1:
                            b[-2]+=1
                            b[-1] = b[-2]+1
                        else:
                            if b[-3]<b[-2] -1:
                                b[-3]+=1
                                b[-2] = b[-3]+1
                                b[-1] = b[-2]+1
                            else:
                                if b[-4]<b[-3] -1:
                                    b[-4]+=1
                                    b[-3] = b[-4]+1
                                    b[-2] = b[-3]+1
                                    b[-1] = b[-2]+1
                                else:
                                    break
                except:
                    break
	
        return results

    
    
    def generate_l_options(self, length):
        pals = []
        l = int(length /2) -1
        odd = length %2
        
        for base in self.enumer(l):
            if odd:
                yield int('1%s0%s1' %(base, base[::-1]))
                yield int('1%s1%s1' %(base, base[::-1]))
                yield int('1%s2%s1' %(base, base[::-1]))
            else:
                yield int('1%s%s1' % (base, base[::-1]))
                
        if odd:

            yield int('2%s0%s2' %('0'*l, '0'*l))
            yield int('2%s1%s2' %('0'*l, '0'*l))
        else:
            yield int('2%s2' %('0'*l*2))
                
    def generate_palendromes(self, start, end):
        lower_lim = start
        start_string = str(start)
        
        index = 0
        pals = [1,2,3,11,22,101,111,121,202,212]
        while index< len(pals) and start > pals[index]:
            index += 1
            
        for pal in pals[index:]:
            start = pal
            if start <=end:
                yield pal

        length = 4

        while length <= len(str(end)):
            for option in self.generate_l_options(length):
                if option < end:
                    yield option
                else:
                    break

            length += 1

            
##        elif len(start_string) %2:
##            start = int(start_string[:len(start_string)/2])
##            omit_middle = False
##        else:
##            start = int(start_string[:(len(start_string)-1)/2 +1])
##            omit_middle = True
##
##        current_length = len(str(start))
##            
##        while True:
##            st = str(start)
##            if omit_middle:
##                val = int(st[:-1]+st[::-1])
##                if val <= end:
##                    yield val
##                else:
##                    break
##            else:
##                val = int(st+st[::-1])
##                if val <= end:
##                    yield val
##                else:
##                    break
##
##            start += 1
##            if len(str(start)) > current_length:
##                if omit_middle:
##                    start = start /10
##                    omit_middle = False
##                else:
##                    omit_middle = True
##                    current_length += 1
            
    
    def execute_case(self, level_size):
        count = 0
        pal_base_l_limit = int(level_size[0]**0.5)
        pal_base_u_limit = int(level_size[1]**0.5)
        
        for pal in self.generate_palendromes(pal_base_l_limit, pal_base_u_limit):
            if self.is_palendrome(pal **2) and pal** 2 >= level_size[0]:
                count += 1
                #print '%s --> %s' % (pal, pal **2)

        print 'count = %s' % count
        return count  

    def test(self):
       assert self.is_palendrome(123) == False
       assert self.is_palendrome(121) == True
       assert self.is_palendrome(12345) == False
       assert self.is_palendrome(12321) == True
        
       assert self.execute_case((1,4)) == 2
       assert self.execute_case((10,120)) == 0
       assert self.execute_case((100,1000)) == 2
       assert self.execute_case((1,1000000)) == 10
       assert self.execute_case((1,10000000000)) == 21
       assert self.execute_case((1000000000,100000000000)) == 5
       #assert self.execute_case((100000000000,10000000000000)) == 13
       #assert self.execute_case((1,10**100)) == 220794

if __name__ == '__main__':
    tdj = FairAndSquareJam()
    tdj.test()
    tdj.execute()

