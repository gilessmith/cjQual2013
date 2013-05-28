import math

class CodeJamRunner(object):

    def execute(self):
        with open('%s-%s.in' % (self.problem_name,self.problem_size)) as f:
            case_count = int(f.readline())
            case =0
            results = []
            while case<case_count:
                results.append(self.solve_case(self.get_case_data(f)))

                case += 1

        with open('%s-%s.out' %
                           (self.problem_name,
                            self.problem_size), 'w') as output:
             for i, result in enumerate(results):
                 output.write('Case #%s: %s\n' % (i+1, result))


class FairSquareJam(CodeJamRunner):
    problem_name = 'C'
    problem_size = 'large-practice-2'
    
    def get_case_data(self, f):
        case_range =[int(x) for x in f.readline().strip().split(' ')]

        return case_range

    def transpose_range(input_range):
        
        min_base = math.ceil(input_range[0] ** 0.5)
        max_base = math.floor(input_range[1] ** 0.5)

        return (min_base, max_base)

    def execute(self):

        self.cache_data()
        super(FairSquareJam, self).execute()

    def cache_data(self):
        pals = []
        for pal in self.generate_pals_optimum():
            pal_sq = pal**2
            if self.is_pal(pal_sq):
                pals.append(pal_sq)
                print '%s --> %s' % (pal, pal_sq)

        self.pals = pals

    def is_pal(self, num):
        str_num = str(num)
        rev_num = [l for l in str_num]
        rev_num.reverse()
        
        return str_num == ''.join(rev_num)
 
    def binary_opts(self, length, fill_count):

        if fill_count == 0:
            yield '0'* length
            return 

        start = length - fill_count
        while start >= 0:
            for stem in self.binary_opts(length - (start+1), fill_count -1):
                yield '0' * start + '1' + stem
            
            start -= 1

        

    def generate_pals_optimum(self):
        
        for pal in [1,2,3,4,5,6,7,8,9,11,22,33,44,55,66,77,88,99]:
            yield pal

        max_base = 10**50
        length = 2
        snip = 2

        while True:
            #import pdb;pdb.set_trace()
            pals = []
            for x in range(0,5):
                if x > length -1:
                    break
                opt_len = length - 1
                if snip:
                    opt_len -= 1

                for opt in self.binary_opts(opt_len, x):
                    rev_opt = [l for l in opt]
                    rev_opt.reverse()
                    if snip:
                        for mid in ['0', '1', '2']:
                            pals.append( '1' + opt + mid + ''.join(rev_opt) + '1')
                    else:
                        pals.append( '1' + opt + ''.join(rev_opt) + '1')

            
            pals.sort()
            
            #import pdb;pdb.set_trace()
            for pal in pals:
                pal = int(pal)
                if pal < max_base:
                    yield pal
                else:
                    return 
                        

            if snip:
                for center in ['0', '1', '2']:
                    pal = int('2%s%s%s2' % ('0'* (length-2), center, '0'* (length-2)))
                    if pal < max_base:
                        yield pal
                    else:
                        break
            else:
                pal = int('2%s2' % ('00'* (length-1)))
                if pal < max_base:
                    yield pal
                else:
                    return

            if snip:
                snip = False
            else:
                snip = True
                length += 1
 


    def generate_palendromes(self):
        snip = True
        start = 1
        start_length = 1
        max_base = math.floor(10** 15)

        while True:
            
            stub = str(start)
            rev_stub = [l for l in stub]
            if snip:
                rev_stub.pop()
            rev_stub.reverse()
            str_value = stub + ''.join(rev_stub)
            value = int(str_value)

            if value < max_base:
                yield value
            else:
                break   
    
            start+= 1         
            if start_length < len(str(start)):
                if snip:
                    snip = False
                    start = start / 10
                else:
                    snip = True
                    start_length += 1

    def solve_case(self, case_range):
        min_index = 0
        max_index = len(self.pals)        

        for i, pal in enumerate(self.pals):   
            if case_range[0] <= pal:
                min_index = i
                break
        for i, pal in enumerate(self.pals[::-1]):   
            if case_range[1] >= pal:
                max_index = len(self.pals) - i
                break

        #print max_index - min_index
        return max_index - min_index

    def test(self):
        #for pal in self.generate_pals_optimum():
        #    print pal
        

        print 'Tests complete'

if __name__ == '__main__':
    tdj = FairSquareJam()
    tdj.test()
    tdj.execute()

