import json
import os

for root, dirs, files in os.walk("."):
    for file in filter(lambda f: f.endswith('.json'), files):
        path = os.path.join(root, file)
        print(path)
        with open(path) as f:
            json.load(f)
