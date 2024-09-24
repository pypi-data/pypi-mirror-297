# ggps

ggps - gps file parsing utilities for garmin connect and garmin devices


## Urls

- GitHub: https://github.com/cjoakim/ggps-py
- PyPi: https://pypi.org/project/ggps/

## Features

- Parse **gpx** and **tcx** files downloaded from Garmin Connect (https://connect.garmin.com)
- The GPX parsed Trackpoint data includes additional/augmented values, including as "seq" and "elapsedtime".
- The TCX parsed Trackpoint data additionally includes additional/augmented values, such as "altitudefeet", "distancemiles", "distancekilometers", and "runcadencex2".


## Quick start


### Installation

```
$ pip install ggps
```

### Use


#### Sample Program

See the following sample-program.py in the GitHub repo.

See the **data/** directory in the GitHub repo for the sample gpx and tcx files
processed by this sample program.

```
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

```

#### Executing the Sample Program

```
$ mkdir tmp

$ python sample-program.py > tmp/sample-program.txt
```

#### Sample Program Output

```
ggps version 0.4.0

processing file data/twin_cities_marathon.tcx with ggps.TcxHandler() ...
{
  "altitudefeet": "850.3937408367167",
  "altitudemeters": "259.20001220703125",
  "cadence": "89",
  "cadencex2": "178",
  "distancekilometers": "0.0",
  "distancemeters": "0.0",
  "distancemiles": "0.0",
  "elapsedtime": "00:00:00",
  "heartratebpm": "85",
  "latitudedegrees": "44.97431952506304",
  "longitudedegrees": "-93.26310088858008",
  "seq": "1",
  "speed": "0.0",
  "time": "2014-10-05T13:07:53.000Z",
  "type": "Trackpoint"
}

...

{
  "altitudefeet": "864.8294163501167",
  "altitudemeters": "263.6000061035156",
  "cadence": "77",
  "cadencex2": "154",
  "distancekilometers": "42.63544921875",
  "distancemeters": "42635.44921875",
  "distancemiles": "26.492439912628992",
  "elapsedtime": "04:14:24",
  "heartratebpm": "161",
  "latitudedegrees": "44.95180849917233",
  "longitudedegrees": "-93.10493202880025",
  "seq": "2256",
  "speed": "3.5460000038146977",
  "time": "2014-10-05T17:22:17.000Z",
  "type": "Trackpoint"
}
2256 trackpoints loaded from file data/twin_cities_marathon.tcx

==========

processing file data/activity_4564516081.tcx with ggps.TcxHandler() ...
{
  "altitudefeet": "796.587936521515",
  "altitudemeters": "242.8000030517578",
  "cadence": "0",
  "distancekilometers": "5.9999998658895494e-05",
  "distancemeters": "0.05999999865889549",
  "distancemiles": "3.728227070091633e-05",
  "elapsedtime": "00:00:00",
  "heartratebpm": "98",
  "latitudedegrees": "35.50809354521334",
  "longitudedegrees": "-80.8350570872426",
  "seq": "1",
  "speed": "0.0",
  "time": "2020-02-17T17:15:02.000Z",
  "type": "Trackpoint"
}

...

{
  "altitudefeet": "804.4619322448889",
  "altitudemeters": "245.1999969482422",
  "cadence": "86",
  "cadencex2": "172",
  "distancekilometers": "23.387580078125",
  "distancemeters": "23387.580078125",
  "distancemiles": "14.532368516690651",
  "elapsedtime": "02:51:26",
  "heartratebpm": "171",
  "latitudedegrees": "35.508142998442054",
  "longitudedegrees": "-80.83528247661889",
  "seq": "2209",
  "speed": "2.3889999389648438",
  "time": "2020-02-17T20:06:28.000Z",
  "type": "Trackpoint"
}
2209 trackpoints loaded from file data/activity_4564516081.tcx

==========

processing file data/twin_cities_marathon.tcx with ggps.PathHandler() ...
{
  "TrainingCenterDatabase": 1,
  "TrainingCenterDatabase@xmlns": 1,
  "TrainingCenterDatabase@xmlns:ns2": 1,
  "TrainingCenterDatabase@xmlns:ns3": 1,
  "TrainingCenterDatabase@xmlns:ns4": 1,
  "TrainingCenterDatabase@xmlns:ns5": 1,
  "TrainingCenterDatabase@xmlns:xsi": 1,
  "TrainingCenterDatabase@xsi:schemaLocation": 1,
  "TrainingCenterDatabase|Activities": 1,
  "TrainingCenterDatabase|Activities|Activity": 1,
  "TrainingCenterDatabase|Activities|Activity@Sport": 1,
  "TrainingCenterDatabase|Activities|Activity|Creator": 1,
  "TrainingCenterDatabase|Activities|Activity|Creator@xsi:type": 1,
  "TrainingCenterDatabase|Activities|Activity|Creator|Name": 1,
  "TrainingCenterDatabase|Activities|Activity|Creator|ProductID": 1,
  "TrainingCenterDatabase|Activities|Activity|Creator|UnitId": 1,
  "TrainingCenterDatabase|Activities|Activity|Creator|Version": 1,
  "TrainingCenterDatabase|Activities|Activity|Creator|Version|BuildMajor": 1,
  "TrainingCenterDatabase|Activities|Activity|Creator|Version|BuildMinor": 1,
  "TrainingCenterDatabase|Activities|Activity|Creator|Version|VersionMajor": 1,
  "TrainingCenterDatabase|Activities|Activity|Creator|Version|VersionMinor": 1,
  "TrainingCenterDatabase|Activities|Activity|Id": 1,
  "TrainingCenterDatabase|Activities|Activity|Lap": 27,
  "TrainingCenterDatabase|Activities|Activity|Lap@StartTime": 27,
  "TrainingCenterDatabase|Activities|Activity|Lap|AverageHeartRateBpm": 27,
  "TrainingCenterDatabase|Activities|Activity|Lap|AverageHeartRateBpm|Value": 27,
  "TrainingCenterDatabase|Activities|Activity|Lap|Calories": 27,
  "TrainingCenterDatabase|Activities|Activity|Lap|DistanceMeters": 27,
  "TrainingCenterDatabase|Activities|Activity|Lap|Extensions": 27,
  "TrainingCenterDatabase|Activities|Activity|Lap|Extensions|LX": 108,
  "TrainingCenterDatabase|Activities|Activity|Lap|Extensions|LX@xmlns": 108,
  "TrainingCenterDatabase|Activities|Activity|Lap|Extensions|LX|AvgRunCadence": 27,
  "TrainingCenterDatabase|Activities|Activity|Lap|Extensions|LX|AvgSpeed": 27,
  "TrainingCenterDatabase|Activities|Activity|Lap|Extensions|LX|MaxRunCadence": 27,
  "TrainingCenterDatabase|Activities|Activity|Lap|Extensions|LX|Steps": 27,
  "TrainingCenterDatabase|Activities|Activity|Lap|Intensity": 27,
  "TrainingCenterDatabase|Activities|Activity|Lap|MaximumHeartRateBpm": 27,
  "TrainingCenterDatabase|Activities|Activity|Lap|MaximumHeartRateBpm|Value": 27,
  "TrainingCenterDatabase|Activities|Activity|Lap|MaximumSpeed": 27,
  "TrainingCenterDatabase|Activities|Activity|Lap|TotalTimeSeconds": 27,
  "TrainingCenterDatabase|Activities|Activity|Lap|Track": 27,
  "TrainingCenterDatabase|Activities|Activity|Lap|Track|Trackpoint": 2256,
  "TrainingCenterDatabase|Activities|Activity|Lap|Track|Trackpoint|AltitudeMeters": 2256,
  "TrainingCenterDatabase|Activities|Activity|Lap|Track|Trackpoint|DistanceMeters": 2256,
  "TrainingCenterDatabase|Activities|Activity|Lap|Track|Trackpoint|Extensions": 2256,
  "TrainingCenterDatabase|Activities|Activity|Lap|Track|Trackpoint|Extensions|TPX": 2256,
  "TrainingCenterDatabase|Activities|Activity|Lap|Track|Trackpoint|Extensions|TPX@xmlns": 2256,
  "TrainingCenterDatabase|Activities|Activity|Lap|Track|Trackpoint|Extensions|TPX|RunCadence": 2256,
  "TrainingCenterDatabase|Activities|Activity|Lap|Track|Trackpoint|Extensions|TPX|Speed": 2256,
  "TrainingCenterDatabase|Activities|Activity|Lap|Track|Trackpoint|HeartRateBpm": 2256,
  "TrainingCenterDatabase|Activities|Activity|Lap|Track|Trackpoint|HeartRateBpm|Value": 2256,
  "TrainingCenterDatabase|Activities|Activity|Lap|Track|Trackpoint|Position": 2256,
  "TrainingCenterDatabase|Activities|Activity|Lap|Track|Trackpoint|Position|LatitudeDegrees": 2256,
  "TrainingCenterDatabase|Activities|Activity|Lap|Track|Trackpoint|Position|LongitudeDegrees": 2256,
  "TrainingCenterDatabase|Activities|Activity|Lap|Track|Trackpoint|Time": 2256,
  "TrainingCenterDatabase|Activities|Activity|Lap|TriggerMethod": 27,
  "TrainingCenterDatabase|Author": 1,
  "TrainingCenterDatabase|Author@xsi:type": 1,
  "TrainingCenterDatabase|Author|Build": 1,
  "TrainingCenterDatabase|Author|Build|Version": 1,
  "TrainingCenterDatabase|Author|Build|Version|BuildMajor": 1,
  "TrainingCenterDatabase|Author|Build|Version|BuildMinor": 1,
  "TrainingCenterDatabase|Author|Build|Version|VersionMajor": 1,
  "TrainingCenterDatabase|Author|Build|Version|VersionMinor": 1,
  "TrainingCenterDatabase|Author|LangID": 1,
  "TrainingCenterDatabase|Author|Name": 1,
  "TrainingCenterDatabase|Author|PartNumber": 1
}

...

```

---

## Changelog

Current version: 0.4.1

-  2024/09/23, version 0.4.1,  Fix pyproject.toml project description
-  2024/09/23, version 0.4.0,  Upgraded to python 3.12, pyproject.toml build mechanism, latest m26 >=0.3.1
-  2020/02/22, version 0.3.0,  Parsing improvements, normalize 'cadence' and 'heartratebpm' attribute names
-  2020/02/19, version 0.2.1,  Upgraded the m26 and Jinga2 libraries
-  2017/09/27, version 0.2.0,  Converted to the pytest testing framework
-  2017/09/26, version 0.1.13, packagin.
-  2016/11/07, version 0.1.12, updated packaging
-  2016/11/07, version 0.1.11, updated packaging
-  2016/11/07, version 0.1.10, updated packaging
-  2016/11/07, version 0.1.9,  updated packaging
-  2016/11/07, version 0.1.8,  updated packaging
-  2016/11/06, version 0.1.7,  updated description
-  2016/11/06, version 0.1.6,  republished
-  2016/11/06, version 0.1.5,  refactored ggps/ dir
-  2016/11/06, version 0.1.4,  refactored ggps/ dir. nose2 for tests
-  2015/11/07, version 0.1.3,  Added README.rst
-  2015/11/07, version 0.1.1   Initial release
