"""A roomy all-air GameTest fixture; the old 8-high room sealed the large flue with its barrier roof."""
from pathlib import Path
import gzip, struct
ROOT=Path(__file__).resolve().parents[1]
def text(value):
    raw=value.encode();return struct.pack('>H',len(raw))+raw
def tag(kind,name,payload):return bytes([kind])+text(name)+payload
def ints(values):return bytes([3])+struct.pack('>i',len(values))+b''.join(struct.pack('>i',v) for v in values)
size=16
blocks=[]
for y in range(size):
    for z in range(size):
        for x in range(size):
            blocks.append(tag(9,'pos',ints([x,y,z]))+tag(3,'state',struct.pack('>i',0))+b'\0')
data=tag(10,'',tag(3,'DataVersion',struct.pack('>i',3955))+tag(9,'size',ints([size]*3))
         +tag(9,'palette',bytes([10])+struct.pack('>i',1)+tag(8,'Name',text('minecraft:air'))+b'\0')
         +tag(9,'blocks',bytes([10])+struct.pack('>i',len(blocks))+b''.join(blocks))
         +tag(9,'entities',bytes([10])+struct.pack('>i',0))+b'\0')
path=ROOT/'src/main/resources/data/createindustrial/structure/empty.nbt'
path.write_bytes(gzip.compress(data,mtime=0))
print('Generated 16x16x16 all-air GameTest room; full large-furnace chimney clearance is inside the test bounds.')
