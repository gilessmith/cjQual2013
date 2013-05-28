
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
    problem_name = 'c'
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

        
    def execute_case(self, levels):
        pass

    def test(self):
       pass

if __name__ == '__main__':
    tdj = FairSquareJam()
    tdj.test()
    tdj.execute()

