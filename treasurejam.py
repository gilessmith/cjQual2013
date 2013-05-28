
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

class ChestList(object):
    """A class that tracks which chests we are yet to open.

    """
    def __init__(self):
        self.chests = []
    
    def add_chest(self, chest):
        self.chests.append(chest)

    def open_chest(self, chest):
        self.chests.remove(chest)

    def get_neutral_chests(self, key_types):
        neutral_chests = []
        for chest in self.chests:
            if chest.neutral and chest.lock_type in key_types:
                neutral_chests.append(chest)
        return neutral_chests
        
    def unopen_chests_count(self):
        return len(self.chests)
    
    def lock_counts(self, lock_type):
        return len(self.chests_of_type(lock_type))

    def chests_of_type(self, lock_type):
        return filter(lambda chest: chest.lock_type == lock_type, self.chests)

    def possible_chests(self, available_key_types):
        possible_c = []
        for chest in self.chests:
            if chest.lock_type in available_key_types:
                possible_c.append(chest)

        return sorted(possible_c, key=lambda chest: 400-chest.key_count())

    def remaining_keys(self):
        remaining_keys = []
        for chest in self.chests:
            remaining_keys += chest.keys

        return remaining_keys
        
class KeyRing(object):
    """ A class used to track the keys that we have access to.

    """
    def __init__(self, keys):
        self.keys = {}
        if keys:
            for key in [int(x) for x in keys.strip().split(' ')]:
                self.add_keys([key])

    def add_keys(self, keys):
        for key in keys:
            try:
                self.keys[key] += 1
            except KeyError:
                self.keys[key] = 1

    def use_key(self, key):
        if self.keys[key] >0:
            self.keys[key] -= 1

            # remove the key if need be
            if self.keys[key] == 0:
                del self.keys[key]
        else:
            raise Exception("key ring doesn't have a key of type %s" % key)

    def get_key_types(self):
        return self.keys.keys()

    def get_keys(self):
        keys = []
        for key in self.get_key_types():
            for i in range(self.keys[key]):
                keys.append(key)

        return keys
        
class Chest(object):
    """Class that represents a chest

    Includes the number of the chest, the lock type, the keys inside, and
    whether or not the chest is neutral. A neutral chest is where it contains
    at least one of the keys used to open it.
    """
    
    def __init__(self, number, data):
        self.number = number
        data = [int(x) for x in data.strip().split(' ')]
        self.lock_type = data[0]
        
        if data[1] >0:
            self.keys = data[2:]
        else:
            self.keys = []
            
        if self.lock_type in self.keys:
            self.neutral = True
        else:
            self.neutral = False

    def key_count(self):
        return len(self.keys)

    def __unicode__(self):
        return 'Chest: %s' % (self.number)

    def __str__(self):
        return self.__unicode__()

class PathFinder(object):
    """ a class that allows iterative calling of the find sequence method
    so that all possible paths are selected.

    """

    def open_chest(self, chest):

        self.chest_list.open_chest(chest)
        self.key_ring.use_key(chest.lock_type)
        self.key_ring.add_keys(chest.keys)
        self.sequence.append(chest.number)
        print self.sequence
        
    def find_sequence(self, unopen_chests, key_ring, sequence):
        self.sequence = sequence
        self.key_ring = key_ring
        self.chest_list = ChestList()
        self.chest_list.chests = unopen_chests

        return self.process_chests()

    def process_chests(self):
        
        while True:
            #import pdb;pdb.set_trace()
            count = 0
            if self.chest_list.unopen_chests_count() == 0:
                return ' '.join([str(x) for x in self.sequence])
            
            neutrals = self.chest_list.get_neutral_chests(self.key_ring.get_key_types())

            for neutral in neutrals:
                
                self.open_chest(neutral)
                count += 1

            if count >0:
                continue

            for key_type in self.key_ring.get_key_types():
                if self.key_ring.keys[key_type] >= self.chest_list.lock_counts(key_type):
                    for chest in self.chest_list.chests_of_type(key_type):
                        self.open_chest(chest)
                        count += 1

            if count >0:
                continue
            
            key_types = self.key_ring.get_key_types()
            for chest in self.chest_list.possible_chests(key_types):
                
                p = PathFinder()
                remaining_chests= self.chest_list.chests[:]
                remaining_chests.remove(chest)
                new_key_ring = KeyRing('')
                new_key_ring.add_keys(self.key_ring.get_keys())
                new_key_ring.use_key(chest.lock_type)
                new_key_ring.add_keys(chest.keys)

                #import pdb;pdb.set_trace()
                result = p.find_sequence(remaining_chests, new_key_ring, self.sequence + [chest.number])

                if result != 'fail':
                    return result

            if len(self.chest_list.remaining_keys()) ==0:
                return 'IMPOSSIBLE'
            
            return 'fail'

class TreasureJam(CodeJamRunner):
    problem_name = 'D'
    problem_size = 'small-attempt2'
    
    def get_case_data(self, f):
        self.sequence = []
        self.key_ring = KeyRing('')
        self.chest_list = ChestList()
        counts = f.readline()
        print counts
        key_count, chest_count = [int(x) for x in counts.strip().split(' ')]

        keys = f.readline()
        print keys
        self.key_ring.add_keys([int(x) for x in keys.strip().split(' ')])
        chest_limit = chest_count
        while chest_count >0:
            chest_count -=1
            chest = Chest(chest_limit - chest_count, f.readline())
            self.chest_list.add_chest(chest)
            
        return None
        
    def execute_case(self, unused):
        p = PathFinder()
        result =  p.find_sequence(self.chest_list.chests, self.key_ring, [])
        print 'result seq: %s ' % result
        if result == 'fail':
            return 'IMPOSSIBLE'
        return result
        
##        while True:
##            count = 0
##            if self.chest_list.unopen_chests_count() == 0:
##                return ' '.join([str(x) for x in self.sequence])
##            
##            neutrals = self.chest_list.get_neutral_chests(self.key_ring.get_key_types())
##
##            for neutral in neutrals:
##                self.open_chest(neutral)
##                count += 1
##
##            if count >0:
##                continue
##
##            for key_type in self.key_ring.get_key_types():
##                if self.key_ring.keys[key_type] >= self.chest_list.lock_counts(key_type):
##                    for chest in self.chest_list.chests_of_type(key_type):
##                        self.open_chest(chest)
##                        count += 1
##
##            if count >0:
##                continue
##
##            
##            
##        # try iteratively starting with the most abundant chest
##            return 'Impossible'

    def test(self):

       return None
       c = Chest(1, '1 1 1')
       assert c.number == 1
       assert c.key_count() == 1
       assert c.neutral == True
       assert c.lock_type == 1
       
       c = Chest(4, '3 2 1 5')
       assert c.number == 4
       assert c.key_count() == 2
       assert c.neutral == False
       assert c.lock_type == 3
       assert 1 in c.keys
       assert 5 in c.keys

       self.sequence = []
       self.chest_list = ChestList()
       self.key_ring = KeyRing('1')
       chest_data = ['1 0', '1 2 1 3', '2 0', '3 1 2']
       for i, chest in enumerate(chest_data):
           self.chest_list.add_chest(Chest(i+1, chest))
       result = self.execute_case(None)
       print result
       assert result == '2 1 4 3'

       self.sequence = []
       self.chest_list = ChestList()
       self.key_ring = KeyRing('1')
       chest_data = ['1 1 2', '1 1 2', '2 1 1', '2 1 1']
       for i, chest in enumerate(chest_data):
           self.chest_list.add_chest(Chest(i+1, chest))
       result = self.execute_case(None)
       print result
       assert result == '1 3 2 4'

       self.sequence = []
       self.chest_list = ChestList()
       self.key_ring = KeyRing('1')
       chest_data = ['1 1 2', '1 1 2', '1 1 2', '2 1 3', '2 1 3', '2 1 3', '3 1 1', '3 1 1', '3 1 5', '5 0']
       for i, chest in enumerate(chest_data):
           self.chest_list.add_chest(Chest(i+1, chest))
       result = self.execute_case(None)
       print result
       assert result == '1 4 7 2 5 8 3 6 9 10'

       
       print 'Tests passed'

if __name__ == '__main__':
    tdj = TreasureJam()
    tdj.test()
    tdj.execute()

