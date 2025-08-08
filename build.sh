current_directory=$PWD
cd Rosless-Lanelet2
rm -r build
mkdir -p build
cd build
cmake -DCMAKE_INSTALL_PREFIX=$current_directory/install ..
make
make install
cd ../..

cd autoware_lanelet2_extension
rm -r build
mkdir -p build
cd build
cmake -DCMAKE_INSTALL_PREFIX=$current_directory/install ..
make
make install
cd ../..

cd autoware_lanelet2_extension_python
rm -r build
mkdir -p build
cd build
cmake -DCMAKE_INSTALL_PREFIX=$current_directory/install ..
make
make install
cd ../..
