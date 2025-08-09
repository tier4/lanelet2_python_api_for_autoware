#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

#include <lanelet2_core/LaneletMap.h>
#include <lanelet2_core/primitives/Lanelet.h>
#include <lanelet2_core/primitives/Point.h>
#include <lanelet2_io/Io.h>
#include <lanelet2_io/Configuration.h>
#include <lanelet2_projection/Mercator.h>
#include <lanelet2_routing/RoutingGraph.h>
#include <lanelet2_traffic_rules/TrafficRulesFactory.h>

namespace py = pybind11;

PYBIND11_MODULE(_lanelet2_python_api, m) {
    m.doc() = "Python bindings for Lanelet2 with Autoware extension";

    // Basic Point3d binding
    py::class_<lanelet::Point3d>(m, "Point3d")
        .def(py::init<lanelet::Id, double, double, double>())
        .def_property_readonly("id", &lanelet::Point3d::id)
        .def_property_readonly("x", [](const lanelet::Point3d& p) { return p.x(); })
        .def_property_readonly("y", [](const lanelet::Point3d& p) { return p.y(); })
        .def_property_readonly("z", [](const lanelet::Point3d& p) { return p.z(); });

    // Basic LineString3d binding
    py::class_<lanelet::LineString3d>(m, "LineString3d")
        .def(py::init<lanelet::Id, lanelet::Points3d>())
        .def_property_readonly("id", &lanelet::LineString3d::id);

    // Basic Lanelet binding
    py::class_<lanelet::Lanelet>(m, "Lanelet")
        .def(py::init<lanelet::Id, lanelet::LineString3d, lanelet::LineString3d>())
        .def_property_readonly("id", &lanelet::Lanelet::id);

    // LaneletMap binding
    py::class_<lanelet::LaneletMap>(m, "LaneletMap")
        .def(py::init<>())
        .def("add", static_cast<void (lanelet::LaneletMap::*)(lanelet::Lanelet)>(&lanelet::LaneletMap::add))
        .def("add", static_cast<void (lanelet::LaneletMap::*)(lanelet::Point3d)>(&lanelet::LaneletMap::add))
        .def("add", static_cast<void (lanelet::LaneletMap::*)(lanelet::LineString3d)>(&lanelet::LaneletMap::add));

    // IO functions (using static_cast to resolve overloads)
    m.def("load", static_cast<std::unique_ptr<lanelet::LaneletMap>(*)(const std::string&, const lanelet::Projector&, lanelet::ErrorMessages*, const lanelet::io::Configuration&)>(&lanelet::load), 
          "Load lanelet map from file",
          py::arg("filename"), py::arg("projector"), py::arg("errors") = nullptr, py::arg("params") = lanelet::io::Configuration(),
          py::return_value_policy::take_ownership);

    m.def("write", static_cast<void(*)(const std::string&, const lanelet::LaneletMap&, const lanelet::Projector&, lanelet::ErrorMessages*, const lanelet::io::Configuration&)>(&lanelet::write), 
          "Write lanelet map to file",
          py::arg("filename"), py::arg("map"), py::arg("projector"), py::arg("errors") = nullptr, py::arg("params") = lanelet::io::Configuration());

    // Add version info
    m.attr("__version__") = "0.1.0";
}