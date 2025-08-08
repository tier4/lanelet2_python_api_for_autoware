#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

#include <lanelet2_core/LaneletMap.h>
#include <lanelet2_core/primitives/Lanelet.h>
#include <lanelet2_core/primitives/Point.h>
#include <lanelet2_io/Io.h>
#include <lanelet2_routing/RoutingGraph.h>
#include <lanelet2_traffic_rules/TrafficRulesFactory.h>

namespace py = pybind11;

PYBIND11_MODULE(_lanelet2_python_api, m) {
    m.doc() = "Python bindings for Lanelet2 with Autoware extension";

    // Basic Point3d binding
    py::class_<lanelet::Point3d>(m, "Point3d")
        .def(py::init<lanelet::Id, double, double, double>())
        .def_property_readonly("id", &lanelet::Point3d::id)
        .def_property_readonly("x", &lanelet::Point3d::x)
        .def_property_readonly("y", &lanelet::Point3d::y)
        .def_property_readonly("z", &lanelet::Point3d::z);

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
        .def("add", py::overload_cast<const lanelet::Lanelet&>(&lanelet::LaneletMap::add))
        .def("add", py::overload_cast<const lanelet::Point3d&>(&lanelet::LaneletMap::add))
        .def("add", py::overload_cast<const lanelet::LineString3d&>(&lanelet::LaneletMap::add));

    // IO functions
    m.def("load", &lanelet::io::load, "Load lanelet map from file",
          py::arg("filename"), py::arg("projector"), py::arg("errors") = nullptr);

    m.def("write", &lanelet::io::write, "Write lanelet map to file",
          py::arg("filename"), py::arg("map"), py::arg("projector"));

    // Add version info
    m.attr("__version__") = "0.1.0";
}