#!/usr/bin/env bash
set -euo pipefail

# Build Rosless-Lanelet2
current_directory=$PWD
cd Rosless-Lanelet2
rm -r build
mkdir -p build
cd build
cmake -DCMAKE_INSTALL_PREFIX=$current_directory/install ..
make
make install
cd ../..

## Patch and build autoware_lanelet2_extension
cd autoware_lanelet2_extension

if git apply --reverse --check ../patches/autoware_lanelet2_extension_full.patch 2>/dev/null; then
  git apply --reverse ../patches/autoware_lanelet2_extension_full.patch
fi
git apply ../patches/autoware_lanelet2_extension_full.patch
cd ..

## Build autoware_lanelet2_extension
cd autoware_lanelet2_extension/autoware_lanelet2_extension
rm -r build
mkdir -p build
cd build
cmake -DCMAKE_INSTALL_PREFIX="${current_directory}/install" ..
make
make install
cd ../../../

## Build autoware_lanelet2_extension_python
cd autoware_lanelet2_extension/autoware_lanelet2_extension_python
rm -r build
mkdir -p build
cd build
cmake -DCMAKE_INSTALL_PREFIX="${current_directory}/install" ..
make
make install
cd ../../../
