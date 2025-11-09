import pickle

class PickleDealer:

    @staticmethod
    def load_pfile(file):
        with open(file, 'rb') as pf:
            pfile = pickle.load(pf)
        return pfile

    @staticmethod
    def write_pfile(file, contents):
        with open(file, 'wb') as pf:
            pickle.dump(contents, pf)