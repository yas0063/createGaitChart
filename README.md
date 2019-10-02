# createGaitChart & createFig


## Overview

This python script may help people who create a gait chart manually from videos

## Requirements

It probably works on anaconda environment. However, if numpy and tkinter are installed, anaconda env is not required.

## createGaitChart

### Usage

#### booting up

```
$ python createGaitChart.py 
```

The default number of legs is six (L1, L2, L3, R1, R2, R3). By using '-l' option, the number of legs can be chaged.

If the target is a spider,
```
$ python createGaitChart.py -l 8
```
If the target is a cat,
```
$ python createGaitChart.py -l 4
```
If the target is a crow
```
$ python createGaitChart.py -l 2
```

The chart area can be secured at boot up with '-f' option.
```
$ python createGaitChart.py -f 1000
```

Of course, options can be used together.
```
$ python createGaitChart.py -f 1000 -l 8
```


#### input data

1. toggle each leg state based on leg state
2. input time
3. push set/chage button


Shortcut keys will help input work.
  - a: toggle L1
  - s: toggle L2
  - d: toggle L3
  - q: toggle R1
  - w: toggle R2
  - e: toggle R3
  - g: set/chage (append current state to result) and move next frame
  - f: set/chage (append current state to result) and move previous frame
  - n: next button (move next frame)
  - b: prev button (move previous frame)
  - A: fill L1 with black until last black cell
  - S: fill L2 with black until last black cell
  - D: fill L3 with black until last black cell
  - Q: fill R1 with black until last black cell
  - W: fill R2 with black until last black cell
  - E: fill R3 with black until last black cell
  - Ctrl-A: fill L1 with white until last black cell
  - Ctrl-S: fill L2 with white until last black cell
  - Ctrl-D: fill L3 with white until last black cell
  - Ctrl-Q: fill R1 with white until last black cell
  - Ctrl-W: fill R2 with white until last black cell
  - Ctrl-E: fill R3 with white until last black cell


## createFig

Create figure of gait chart from data file that created with createGaitChart.py. Current version only supports movie frame number although output csv file from createGaitChart can include data of time.

### Usage
```
createFig.py [-h] [-o OUTPUTFILENAME] datafilename
```

#### optional arguments
- -h, --help            show help message and exit
- -o OUTPUTFILENAME, --outputfilename OUTPUTFILENAME,  default output filename is ./output.pdf


## NOTE

- By loading the saved csv file, interrupted work can be resumed. However, the number of legs is fixed at booting up.
Therefore, if you want to read data files other than the default 6 legs (ex. 8 legs), 
you need to load the file after booting up in 8 legs mode.
- The number of legs is assumed to be even. If the number of legs is odd, this may work well or may not work.


## TODO 
- remove magic numbers 
- display gait chart based on time. 
