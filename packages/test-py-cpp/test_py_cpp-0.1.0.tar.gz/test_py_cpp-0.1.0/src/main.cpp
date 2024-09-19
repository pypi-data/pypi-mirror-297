#include <iostream> // for std::cout

#include <algorithm> // for std::for_each
#include <pybind11/pybind11.h>
#include <utility> // for std::pair

#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/graph_utility.hpp>

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

using namespace boost;

int add(int i, int j) { return i + j + 1; }

int gra() {
    // create a typedef for the Graph type
    typedef adjacency_list<vecS, vecS, bidirectionalS> Graph;

    // Make convenient labels for the vertices
    enum { A, B, C, D, E, N };
    const int num_vertices = N;
    const char *name = "ABCDE";

    // writing out the edges in the graph
    typedef std::pair<int, int> Edge;
    Edge edge_array[] = {Edge(A, B), Edge(A, D), Edge(C, A), Edge(D, C),
                         Edge(C, E), Edge(B, D), Edge(D, E)};
    const int num_edges = sizeof(edge_array) / sizeof(edge_array[0]);

    // declare a graph object
    Graph g(num_vertices);

    // add the edges to the graph object
    for (int i = 0; i < num_edges; ++i)
        add_edge(edge_array[i].first, edge_array[i].second, g);

    std::cout << "Graph size " << sizeof(g) << std::endl;

    return 5;
}

namespace py = pybind11;

PYBIND11_MODULE(_core, m) {
    m.doc() = R"pbdoc(
        Pybind11 example plugin
        -----------------------

        .. currentmodule:: scikit_build_example_ugrnn

        .. autosummary::
           :toctree: _generate

           add
           subtract
    )pbdoc";

    m.def("add", &add, R"pbdoc(
        Add two numbers

        Some other explanation about the add function.
    )pbdoc");

    m.def("gra", &gra, R"pbdoc(
        Test the graph function
    )pbdoc");

    m.def("subtract", [](int i, int j) { return i - j; }, R"pbdoc(
        Subtract two numbers

        Some other explanation about the subtract function.
    )pbdoc");

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}