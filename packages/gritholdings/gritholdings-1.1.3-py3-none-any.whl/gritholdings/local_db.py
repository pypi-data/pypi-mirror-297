"""Local Database Module"""
import pickle


class LocalDB:
    def save_to_pickle(data, filename):
        try:
            with open(filename, 'wb') as f:
                pickle.dump(data, f)
        except Exception as e:
            print(f"An error occurred while saving to {filename}: {e}")


    def load_from_pickle(filename):
        try:
            with open(filename, 'rb') as f:
                return pickle.load(f)
        except EOFError:
            return {}