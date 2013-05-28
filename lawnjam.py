
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


class LawnJam(CodeJamRunner):
    problem_name = 'B'
    problem_size = 'large'
    
    def get_case_data(self, f):
        lawn_size = [int(x) for x in f.readline().split(' ')]
        row_count = lawn_size[0]
        rows = []
        while row_count >0:
            row_count -=1
            rows.append([int(x) for x in f.readline().split(' ')])
        return rows, lawn_size[0], lawn_size[1]

        
    def execute_case(self, lawn):
        lawn, lawn_length, lawn_width = lawn[0], lawn[1], lawn[2]
        r_maxes = []
        c_maxes = []
        for row in lawn:
            r_maxes.append(max(row))

        for column in range(lawn_width):
            c_maxes.append(max([lawn[i][column] for i in range(lawn_length)]))

        for row_i in range(lawn_length):
            for col_i in range(lawn_width):
                square_height = lawn[row_i][col_i]
                if (square_height < r_maxes[row_i] and
                    square_height < c_maxes[col_i]):
                        return 'NO'

        return 'YES'

    def test(self):
##        assert self.execute_case([[2,1,2], [1,1,1],[2,1,2]], 3, 3) == 'YES'
##        assert self.execute_case([[2,2,2,2,2], [2,1,1,1,2], [2,1,2,1,2],
##                                  [2,1,1,1,2],[2,2,2,2,2]], 5, 5) == 'NO'
##        assert self.execute_case([[1,2,1]], 1, 3) == 'YES'
        pass

if __name__ == '__main__':
    tdj = LawnJam()
    tdj.test()
    tdj.execute()

