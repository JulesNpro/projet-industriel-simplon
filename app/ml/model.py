import pickle

with open('modeljose.pkl', 'rb') as file:
    model = pickle.load(file)
print(model)