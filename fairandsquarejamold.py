
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
    problem_name = 'c'
    problem_size = 'small-attempt0'
    
    def get_case_data(self, f):
        level_size = [int(x) for x in f.readline().strip()]
        return level_size

    def is_palendrome(self, num):
        st = str(num)
        return st == st[::-1]

    def generate_palendromes(self, start, end):
        lower_lim = start
        start_string = str(start)
        if len(start_string) == 1:
            start = start
            omit_middle = True
        elif len(start_string) %2:
            start = int(start_string[:len(start_string)/2])
            omit_middle = False
        else:
            start = int(start_string[:(len(start_string)-1)/2 +1])
            omit_middle = True

        current_length = len(str(start))
            
        while True:
            st = str(start)
            if omit_middle:
                val = int(st[:-1]+st[::-1])
                if val <= end:
                    yield val
                else:
                    break
            else:
                val = int(st+st[::-1])
                if val <= end:
                    yield val
                else:
                    break

            start += 1
            if len(str(start)) > current_length:
                if omit_middle:
                    start = start /10
                    omit_middle = False
                else:
                    omit_middle = True
                    current_length += 1
            
    
    def execute_case(self, level_size):
        count = 0
        pal_base_l_limit = int(level_size[0]**0.5)
        pal_base_u_limit = int(level_size[1]**0.5)
        
        for pal in self.generate_palendromes(pal_base_l_limit, pal_base_u_limit):
            if self.is_palendrome(pal **2) and pal** 2 >= level_size[0]:
                count += 1
                print '%s --> %s' % (pal, pal **2)

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
       assert self.execute_case((100000000000,10000000000000)) == 13
       #assert self.execute_case((1,10**30)) == 10

if __name__ == '__main__':
    tdj = FairAndSquareJam()
    tdj.test()
    tdj.execute()

