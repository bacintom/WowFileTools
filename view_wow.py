import datetime
import re
import struct
import sys

import numpy as np
import pyqtgraph.opengl as gl
from pyqtgraph.Qt import QtCore, QtGui


class WOWParseError(Exception):
    pass

def match_code(code:str, raw_line:bytes)->bool:
    """returns True if code is met at the beginning of the line."""
    line = raw_line.decode("ascii")
    return line.startswith(code + " ") or line.startswith(code + ";")

def extract_code_value(code_expr:str, raw_line:bytes)->float:
    """extracts a floating-point value specified after the prefix code-expr (which could be a regex). Returns None if not found."""
    line = raw_line.decode("ascii")
    zmotion_match = re.findall(r"%s([\d.-]+)[;\s]" % code_expr, line)
    if zmotion_match:
        return float(zmotion_match[0])
    return None  #not found

def run(wow_file_path):
    W, H, L = None, None, None
    maxL = 0
    layers = []
    layer_thickness = None
    z = 0.0
    ptime = 0
    zspeed = None
    power = 0
    prev_layer_z = None
    with open(wow_file_path, "rb") as wow_f:
        while True:
            line = wow_f.readline()
            if line == b"":  #EOF
                break
            elif match_code("G4", line):  #wait
                secs = extract_code_value("S", line)
                ptime += secs
            elif match_code("G91", line):  #relative coordinate mode
                pass
            elif match_code("M17", line):  #turn on steppers
                pass
            elif match_code("M18", line):  #turn off steppers
                pass
            elif match_code("G21", line):  #go millimeters mode
                pass
            elif match_code("G28", line):  #move to origin
                z = extract_code_value("Z", line)
            elif match_code("M106", line):  #set UV lamps power?
                power = extract_code_value("S", line)
            elif match_code("G1", line):  #move platform
                zmotion = extract_code_value("Z", line)
                if not zmotion:
                    print("WARNING motion not defined in line : ", line)
                new_zspeed = extract_code_value("F", line)
                zspeed = new_zspeed or zspeed
                if not new_zspeed:
                    print("WARNING speed not defined for travel in line : ",
                          line)
                secs = abs(zmotion / zspeed) * 60  #min->sec
                ptime += secs
                z += zmotion
            elif line.startswith(b";W"):  #define screen width in pixels
                W = int(line[3:-2].decode("ascii"))
            elif line.startswith(b";H"):  #define screen height in pixels
                H = int(line[3:-2].decode("ascii"))
            elif line.startswith(b";L"):  #define layer index?
                L = int(line[3:-2].decode("ascii"))
                maxL = max(L, maxL)
            elif line.startswith(
                    b"{{"
            ):  #layer pixels, encoded in binary (1 bit = 1 pixel), probably to save space and load time.
                if W is None:
                    raise WOWParseError(
                        "Layer contents defined without layer width.")
                if H is None:
                    raise WOWParseError(
                        "Layer contents defined without layer height.")
                if L is None:
                    raise WOWParseError(
                        "Layer contents defined without layer index.")

                l = wow_f.read(W * H // 8 + 1)
                layers.append(
                    np.unpackbits(np.fromstring(
                        l[:-1], dtype=np.uint8)).reshape((H, W)))
                #print("bitmap[%d]: "%(len(l)-1,),l[:10]," ... ",l[-10:])
            elif line.startswith(b"}}"):  #end of pixel data
                pass
            else:
                print("not understood:", line)

        print("PRINT TIME ESTIMATE:", str(datetime.timedelta(seconds=ptime)))
        app = QtGui.QApplication([])
        QtGui.QMessageBox.about(None,"Estimate","Print time estimate: %s" % str(datetime.timedelta(seconds=ptime)))

        layers = np.array(layers)[:]
        layers = layers.reshape(len(layers), H, W // 8,
                                8)[:, :, :, ::-1]  #big/little-endian flip
        layers = layers.reshape(len(layers), H, W, 1)
        layers = layers[:, :, ::-1, :]
        layers_rgba = np.concatenate(
            [layers, layers, layers, layers], axis=3) * 255
        layers_rgba[:, :, :, 3] //= 32
        #for voxel in layers_rgba.reshape((50*H*W,4)):
        #    if voxel[3] != 0:
        #        print("voxel:",voxel)

        w = gl.GLViewWidget()
        w.opts['distance'] = 200
        w.show()
        w.setWindowTitle("Print 3D Display")

        g = gl.GLGridItem()
        g.scale(10, 10, 1)
        w.addItem(g)

        data = layers_rgba.transpose(1, 2, 0, 3)

        v = gl.GLVolumeItem(data)
        v.scale(.1, .1, .05)
        w.addItem(v)

        ax = gl.GLAxisItem()
        w.addItem(ax)

        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage : python[3] %s path/to/file.wow" % sys.argv[0])
    else:
        wow_file_path = sys.argv[1]
        run(wow_file_path)
