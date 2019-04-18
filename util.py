import os
import binascii
import pickle


class Util():
    @classmethod
    def generate_block_id(self):
        return binascii.hexlify(os.urandom(16)).decode('utf-8')

    @classmethod
    def dump(self, path, data):
        with open(path, "wb") as fout:
            pickle.dump(data, fout)

    @classmethod
    def load(self, path):
        with open(path, "rb") as fin:
            return pickle.load(fin)
