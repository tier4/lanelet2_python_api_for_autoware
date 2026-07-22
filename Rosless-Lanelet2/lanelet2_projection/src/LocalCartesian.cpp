#include "lanelet2_projection/LocalCartesian.h"

namespace lanelet {
namespace projection {

LocalCartesianProjector::LocalCartesianProjector(Origin origin)
    : Projector(origin),
      localCartesian_(origin.position.lat, origin.position.lon, origin.position.ele) {}

BasicPoint3d LocalCartesianProjector::forward(const GPSPoint& gps) const {
  double x = 0;
  double y = 0;
  double z = 0;
  try {
    localCartesian_.Forward(gps.lat, gps.lon, gps.ele, x, y, z);
  } catch (GeographicLib::GeographicErr& e) {
    throw ForwardProjectionError(e.what());
  }
  return BasicPoint3d{x, y, z};
}

GPSPoint LocalCartesianProjector::reverse(const BasicPoint3d& local) const {
  double lat = 0;
  double lon = 0;
  double h = 0;
  try {
    localCartesian_.Reverse(local.x(), local.y(), local.z(), lat, lon, h);
  } catch (GeographicLib::GeographicErr& e) {
    throw ReverseProjectionError(e.what());
  }
  return GPSPoint{lat, lon, h};
}

}  // namespace projection
}  // namespace lanelet
