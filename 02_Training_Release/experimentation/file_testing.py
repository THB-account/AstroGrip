from pathlib import Path
from yaml import dump

p = Path("./test/sehr_langer_pfad")

print(p.exists())

p.mkdir(parents=True)

print(p.exists())

with open(p / "test.yaml",'w') as file:
    d = {"uuid":"dada","time_of_creation":1}
    dump(d,file)
