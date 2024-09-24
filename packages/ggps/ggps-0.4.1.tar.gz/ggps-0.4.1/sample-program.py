import json

import ggps

# Use:
# python sample-program.py > tmp/sample-program.txt


if __name__ == "__main__":

    print("ggps version {}".format(ggps.VERSION))

    if True:
        infile = "data/twin_cities_marathon.tcx"
        print("")
        print("processing file {} with ggps.TcxHandler() ...".format(infile))
        handler = ggps.TcxHandler()
        handler.parse(infile)
        trackpoints = handler.trackpoints
        for t in trackpoints:
            print(repr(t))
        count = len(trackpoints)
        print("{} trackpoints loaded from file {}".format(count, infile))

    if True:
        infile = "data/twin_cities_marathon.gpx"
        print("==========")
        print("processing file {} with ggps.GpxHandler() ...".format(infile))
        handler = ggps.GpxHandler()
        handler.parse(infile)
        trackpoints = handler.trackpoints
        for t in trackpoints:
            print(repr(t))
        count = len(trackpoints)
        print("{} trackpoints loaded from file {}".format(count, infile))

    if True:
        infile = "data/activity_4564516081.tcx"
        print("==========")
        print("processing file {} with ggps.TcxHandler() ...".format(infile))
        handler = ggps.TcxHandler()
        handler.parse(infile)
        trackpoints = handler.trackpoints
        for t in trackpoints:
            print(repr(t))
        count = len(trackpoints)
        print("{} trackpoints loaded from file {}".format(count, infile))

    if True:
        infile = "data/twin_cities_marathon.tcx"
        print("==========")
        print("processing file {} with ggps.PathHandler() ...".format(infile))
        handler = ggps.PathHandler()
        handler.parse(infile)
        print(str(handler))
        obj = json.loads(str(handler))

    if True:
        infile = "data/activity_4564516081.gpx"
        print("==========")
        print("processing file {} with ggps.GpxHandler() ...".format(infile))
        handler = ggps.GpxHandler()
        handler.parse(infile)
        trackpoints = handler.trackpoints
        for t in trackpoints:
            print(repr(t))
        count = len(trackpoints)
        print("{} trackpoints loaded from file {}".format(count, infile))
