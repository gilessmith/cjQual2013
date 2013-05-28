
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


class TicTacToeJam(CodeJamRunner):
    problem_name = 'A'
    problem_size = 'large'
    
    def get_case_data(self, f):
        board = [f.readline().strip() for x in range(4)]
        try:
            # ignore blank line.
            f.readline()
        except:
            pass
                
        return board

        
    def execute_case(self, board):

        for row in board:
            if not ('.' in row or 'X' in row):
                return 'O won'
            elif not ('.' in row or 'O' in row):
                return 'X won'

        for col_index in range(4):
            column = [row[col_index] for row in board]
            
            if not ('.' in column or 'X' in column):
                return 'O won'
            elif not ('.' in column or 'O' in column):
                return 'X won'

        forward_diagonal = [board[i][i] for i in range(4)]
        if not ('.' in forward_diagonal or 'X' in forward_diagonal):
            return 'O won'
        elif not ('.' in forward_diagonal or 'O' in forward_diagonal):
            return 'X won'
        
        reverse_diagonal = [board[i][3-i] for i in range(4)]
        if not ('.' in reverse_diagonal or 'X' in reverse_diagonal):
            return 'O won'
        elif not ('.' in reverse_diagonal or 'O' in reverse_diagonal):
            return 'X won'

        if '.' in ''.join(board):
            return  'Game has not completed'
        else:
            return 'Draw'

        

    def test(self):
       assert self.execute_case(['XXXT','....', 'OO..', '....']) == 'X won'
       assert self.execute_case(['XOXT','XXOO', 'OXOX', 'XXOO']) == 'Draw'
       assert self.execute_case(['XOX.','OX..', '....', '....']) == 'Game has not completed'
       assert self.execute_case(['OOXX','OXXX', 'OX.T', 'O..O']) == 'O won'
       assert self.execute_case(['XXXO','..O.', '.O..', 'T...']) == 'O won'
       assert self.execute_case(['OXXX','XO..', '..O.', '...O']) == 'O won'

if __name__ == '__main__':
    tdj = TicTacToeJam()
    tdj.test()
    tdj.execute()

