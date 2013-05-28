
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


def find_sequence(chests, keys):
    
    if not slow_impossibility_check(chests[:], keys[:])	:
        return False

    for chest in chests:
        
        if chest[0] in keys:
            if len(chests) == 1:
                return [chest[1]]

            remaining_chests = chests[:]
            remaining_chests.remove(chest)
            remaining_keys = keys[:]
            remaining_keys.remove(chest[0])
            remaining_keys += chest[2]

            sequence = find_sequence(remaining_chests, remaining_keys)
            if sequence:
                return [chest[1]] + sequence
            elif chest[0] in chest[2]:
                # if the chest contains a key that is required to open it, then 
                # it is a neutral chest, and it cannot be wrong to open it.
                return None
                

    # no successful sequence found - FAIL
    return None
                
def slow_impossibility_check(chests, keys):    

    while True:
        new_keys = []
        for chest in [chest for chest in chests]:
        
            if chest[0] in keys:
                for key in chest[2]:
                    if not key in keys:
                        new_keys.append(key)
                
                chests.remove(chest)
        
        if len(new_keys) == 0:
            break
        keys += new_keys

    if len(chests) == 0:
        return True

    print chests
    print keys
    return False
             

def quick_impossibility_check(chests, keys):
    lock_counts = {}
    key_counts = {}
    for key in keys:
        try:
            key_counts[key] += 1
        except KeyError:
            key_counts[key] = 1

    for chest in chests:
        try:
            lock_counts[chest[0]] += 1
        except KeyError:
            lock_counts[chest[0]] = 1

        for key in chest[2]:
            try:
                key_counts[key] += 1
            except KeyError:
                key_counts[key] = 1

    for key in lock_counts.keys():
        if lock_counts[key] > key_counts[key]:
            return False

    return True
    

class TreasureJam(CodeJamRunner):
    problem_name = 'D'
    problem_size = 'large-practice'
    
    def get_case_data(self, f):
        chests = []
        counts = f.readline()
        key_count, chest_count = [int(x) for x in counts.strip().split(' ')]

        keys = [int(x) for x in f.readline().strip().split(' ')]
        chest_limit = chest_count
        while chest_count > 0:
            chest_count -=1
            chest_data = [int(x) for x in f.readline().strip().split(' ')]
            # Chest: [lock_type, chest_number, chest_keys]
            chest = [chest_data[0], chest_limit - chest_count, chest_data[2:]]
            chests.append(chest)
        print chests
        print keys
        #import pdb;pdb.set_trace()
        return {'keys':keys, 'chests':chests}
                    
    def execute_case(self,data):
        sequence = None
        if quick_impossibility_check(data['chests'], data['keys']):
            sequence = find_sequence(data['chests'], data['keys'])
        
        if sequence:
            printable_sequence = ' '.join([str(n) for n in sequence])
            print printable_sequence
            return printable_sequence
        else:
            print 'IMPOSSIBLE'
            return 'IMPOSSIBLE'

    def test(self):
       
       chest_data = [[1, 1, [2]], [1, 2, [2]], [2, 3, [1]], [2, 4, [1]]]
       result = self.execute_case({'keys':[1], 'chests':chest_data})
       print result
       assert result == '1 3 2 4'

       chest_data = [[1, 1, [2]], [1, 2, [2]], [1, 3, [2]], [2, 4, [3]], [2, 5, [3]], [2, 6, [3]], [3, 7, [1]], [3, 8, [1]], [3, 9, [5]], [5, 10, []]]
       result = self.execute_case({'keys':[1], 'chests':chest_data})
       print result
       assert result == '1 4 7 2 5 8 3 6 9 10'
       
       print 'Tests passed'

if __name__ == '__main__':
    tdj = TreasureJam()
    tdj.test()
    tdj.execute()

