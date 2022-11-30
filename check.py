import geojson
import json
import os
import re

names = {}
ids = {}

for root, dirs, files in os.walk("."):
    for file in sorted(filter(lambda f: f.endswith('.json'), files)):
        path = os.path.join(root, file)
        if "package" not in path and "renovate.json" not in path and "settings.json" not in path:
            print(path)
            with open(path) as f:
                # The entity must be a valid JSON file
                entity = json.load(f)
                # All entities should have a type and an id, and they cannot include spaces
                assert "id" in entity, "The entity does not contain the id: " + str(entity)
                assert " " not in entity["id"], {"id": entity["id"]}
                assert "type" in entity, "The entity does not contain the type: " + str(entity)
                assert " " not in entity["type"], {"id": entity["id"], "type": entity["type"]}
                regexp = re.compile(r'\(|\)')
                for key, value in entity.items():
                    # Check for empty spaces at the begin/end of the key/attribute
                    assert not key.startswith(" ") and not key.endswith(" "), {"id": entity["id"], key: value}
                    assert not str(value).startswith(" ") and not str(value).endswith(" "), {"id": entity["id"], key: value}
                    # Attributes cannot contain brackets
                    assert not regexp.search(str(value)), {"id": entity["id"], key: value}
                    # Any location attribute must be a valid GeoJSON
                    if "location" in key.lower():
                        assert geojson.loads(json.dumps(entity[key])).is_valid, {"id": entity["id"], key: value}

                # Entities cannot have names
                if "name" in entity:
                    assert entity["name"] not in names, "Entities with duplicated names " + names[entity["name"]] + " and " + path
                    names[entity["name"]] = path

                # Entities cannot have duplicated ids
                assert entity["id"] not in ids, "Entities with duplicated ids " + ids[entity["id"]] + " and " + path + "\n" + str(ids)
                ids[entity["id"]] = path

                # It is not mandatory for a Task to have an actual location
                if entity["type"] == "Task" and entity["taskType"] == "Mission":
                    assert "plannedLocation" in entity
                    # assert "actualLocation" in entity

                # This are valid controlled properties for devices
                if "controlledProperty" in entity:
                    known_properties = set(["heartbeat", "temperature", "humidity", "image", "timestamp"])
                    difference = set(entity["controlledProperty"]).difference(known_properties)
                    assert (len(difference) == 0), "Unknown properties: " + str(difference)
