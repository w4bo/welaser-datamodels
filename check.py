import json
import os

for root, dirs, files in os.walk("."):
    for file in filter(lambda f: f.endswith('.json'), files):
        path = os.path.join(root, file)
        if "package" not in path and "renovate" not in path:
            print(path)
            with open(path) as f:
                entity = json.load(f)
                # all entities should have a type and an id
                assert "id" in entity
                assert "type" in entity
                if "Task" in path:
                    assert "actualLocation" in entity

