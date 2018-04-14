"""writes a forged .wow file that turns on the UV for one hour and that's all.
Basically, it turns the Sparkmaker into a UV print curer.
WARNING : use at your own risks
WARNING : Be careful not to damage your eyes & skin! Put on the lid, and add another protective layer that blocks UVs (I use aluminium foil).
WARNING : this could cause early wear of the LCD screen (maybe?). If you fear that, remove the LCD..."""

import os

path = "CurerSlice"
cure_time_in_secs = 3600

s = b"""G21;
M17;
;W:480;
;H:854;
;L:1;
{{
"""
s+=b"\xFF"*(480*854//8)
s+=b"""
}}
M106 S255;
G4 S%d;
M106 S0;
M18;
"""%cure_time_in_secs

os.makedirs(path,exist_ok=True)
with open(path+"/print.wow","wb") as f:
    f.write(s)
