"""Original low-volume mechanical/arc effects for Create: Industrial.
Deterministically synthesizes clean mono PCM; ffmpeg encodes Vorbis OGG.
No generated speech, sampled commercial/game audio, or external assets.
"""
from pathlib import Path
import math, wave, subprocess, tempfile
import numpy as np

OUT=Path(__file__).resolve().parents[1]/'src/main/resources/assets/createindustrial/sounds/welder'
OUT.mkdir(parents=True,exist_ok=True)
RATE=32000
rng=np.random.default_rng(1907)

def smooth(x, width):
    # Small zero-phase smoothing kernel for natural nonharsh sizzling.
    k=np.ones(width)/width
    return np.convolve(x,k,'same')

def save(name, y):
    fade=min(len(y)//8, int(.018*RATE))
    y[:fade]*=np.linspace(0,1,fade)
    y[-fade:]*=np.linspace(1,0,fade)
    y=np.tanh(y * 1.1)
    y=(y / max(1.0,np.max(np.abs(y)) / 0.67) * 28000).astype(np.int16)
    with tempfile.TemporaryDirectory() as t:
        inp=Path(t)/'source.wav'
        with wave.open(str(inp),'wb') as wf:
            wf.setnchannels(1);wf.setsampwidth(2);wf.setframerate(RATE);wf.writeframes(y.tobytes())
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(inp),'-c:a','libvorbis','-qscale:a','5',str(OUT/(name+'.ogg'))],check=True)
    print(name,round(len(y)/RATE,3),'s', (OUT/(name+'.ogg')).stat().st_size,'bytes')

def make_select():
    n=int(.14*RATE);t=np.arange(n)/RATE
    tap=np.sin(2*np.pi*(460*t+500*t*t))*np.exp(-32*t)
    chime=np.sin(2*np.pi*890*t)*np.exp(-53*t)
    click=(rng.normal(size=n)-smooth(rng.normal(size=n),14))*np.exp(-70*t)
    return .29*tap + .10*chime + .07*click

def make_weld():
    n=int(.49*RATE);t=np.arange(n)/RATE
    white=rng.normal(size=n)
    grit=white-smooth(white,25)
    mid=smooth(white,4)-smooth(white,35)
    arc=np.sin(2*np.pi*(960*t+120*t*t)) + .27*np.sin(2*np.pi*1640*t)
    micro=(.65+.35*np.sin(2*np.pi*33*t)**2)
    fade=np.minimum(1,np.minimum(t/.04,(.49-t)/.12).clip(0,1))
    noise=(.22*grit+.17*mid)*micro
    pulses=np.zeros(n)
    for center in (.067,.137,.211,.293,.362):
        tt=(t-center)
        pulses+=.14*np.exp(-(tt/.013)**2)*(rng.normal(size=n)*.23+np.sin(2*np.pi*1180*tt))
    finish=.13*np.exp(-np.maximum(0,t-.34)*22)*np.sin(2*np.pi*(590*t+100*t*t))
    return fade*(noise+.055*arc+pulses+finish)

def make_release():
    n=int(.24*RATE);t=np.arange(n)/RATE
    hiss=(rng.normal(size=n)-smooth(rng.normal(size=n),20))*.09*np.exp(-13*t)
    decay=np.sin(2*np.pi*(600*t-460*t*t))*.14*np.exp(-16*t)
    tap=np.sin(2*np.pi*170*t)*.13*np.exp(-28*t)
    return hiss+decay+tap

def make_invalid():
    # 120ms soft brass/mechanical 'tick' rather than a harsh error noise.
    n=int(.12*RATE); t=np.arange(n)/RATE
    tap=np.sin(2*np.pi*(380*t-90*t*t))*np.exp(-45*t)
    texture=(rng.normal(size=n)-smooth(rng.normal(size=n),9))*np.exp(-55*t)
    return .17*tap+.023*texture

save('select',make_select())
save('weld',make_weld())
save('release',make_release())
save('invalid',make_invalid())
