import os
import time

import pdbparse
from pdbparse.peinfo import *



def net(pdb_file):
    p = pdbparse.parse(pdb_file, fast_load=True)
    pdb = p.streams[pdbparse.PDB_STREAM_PDB]
    pdb.load()
    # print(p.streams)
    guidstr = ('%08x%04x%04x%s' % (pdb.GUID.Data1, pdb.GUID.Data2, pdb.GUID.Data3, binascii.hexlify(
        pdb.GUID.Data4).decode('ascii'))).upper()

    print("PDB Guid : %s" % (guidstr))
    print
    print("时间戳 : %s" % pdb.TimeDateStamp)
    print("names : %s" % pdb.names)
    print("Age : %d" % pdb.Age)

    dbi = p.streams[pdbparse.PDB_STREAM_DBI]
    dbi.load()
    print(dbi.DBIExHeaders)
    for (i, fns) in enumerate(dbi.modules):
        module_name = dbi.DBIExHeaders[i].objName
        print("[%d] DBI Module : %s" % (i, module_name))
        for fn in fns:
            print(u'\t%s' % fn)
        print(u'-')
    streams_ = p.streams[193]
    print(streams_)
    dbi1 = p.streams[pdbparse.PDB_STREAM_TPI]
    dbi1.load()
    structures = str(dbi1.structures)
    name = "symbol_" + str(time.time()) + ".txt"
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), name)
    with open(filename, "w") as j:
        j.write(structures)
if __name__ == '__main__':
    net(sys.argv[1])