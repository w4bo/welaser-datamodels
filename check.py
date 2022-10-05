import json
import os
import geojson

for root, dirs, files in os.walk("."):
    for file in sorted(filter(lambda f: f.endswith('.json'), files)):
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
                if "location" in entity:
                    assert geojson.loads(json.dumps(entity["location"])).is_valid
