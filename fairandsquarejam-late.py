import math
import bisect

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
    problem_size = 'small-practice'
    
    def get_case_data(self, f):
        level_count = int(f.readline())
        levels = []
        while level_count >0:
            level_count -=1
            level = [int(x) for x in f.readline().split(' ')]
            level.append(0)
            levels.append(level)
        return levels

    def transpose_range(input_range)
        
        min_base = math.ceil(input_range[0] ** 0.5)
        max_base = math.floor(input_range[1] ** 0.5)

        return (min_base, max_base)
        
    def generate_palendromes():
        snip = True
        start = 1
        max_base = math.floor(1000** 0.5)

        while True:
            
            stub = str_start
            rev_stub = [l for l in stub]
            if snip:
                rev_stub.pop()
            rev_stub.reverse()
            str_value = stub + ''.join(rev_stub)
            value = int(str_value)

            if value < max_base:
                yield value


    def solve_case(self, set_range):
        pass


    def test(self):
       pass

if __name__ == '__main__':
    tdj = FairSquareJam()
    tdj.test()
    tdj.execute()

