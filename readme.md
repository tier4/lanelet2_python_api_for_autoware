# Standable Autoware Lanelet2 Extension


## Setup
This repository will build and install (first in the local directory) the Lanelet2 library and the autoware_lanelet2_extension.

```
## Common packages only not available in bare ubuntu container
sudo apt install git gcc cmake python3 python3-pip

## install addtional necessary packages
bash pre-install.sh 

## build the repositories and it will create an `install` folder locally
bash build.sh

## add environmental variables in the current terminal
source setup.bash
```

Then we can use `lanelet2` and `autoware_lanelet2_extension_python` as if normal python packages everywhere.

I have already tested that I can launch lanelet2 (and the sub-packages) package normally, (with the installation pipeline reproduced in ubuntu 22.04 container).

###
Thanks https://github.com/embedded-software-laboratory/Rosless-Lanelet2 for there developments.

## API Changes (under Test)

For now I am using Eigen vecstors instead of Geometric poses. I have not tested if they are correct.
