#include <iostream>
#include <vector>

using namespace std;

class Graph {

 private:

  vector <vector <float> > mat;


 public:
  Graph(int size);
  Graph(vector <vector <float> > &mat);

  // make the mat sysmetric by filling the half
  // below diagonal
  void fill_mat();

  // set edge cost
  void set_edge_cost(int s, int t, float v);

  float get_edge_cost(int s, int t);

  void print_mat();

  vector <int> get_all_vertexes();
};


class Route {
 public:
  vector <int> route;
  float cost;

  void print();
};


class Bruteforce_Solver {
  class Node {
  private:
    vector <int> cur_route;
    vector <int> avail_vertexes;
    float cur_route_cost;

  public:
    Node(vector <int> &vertexes);
    Node(Node *n);
    bool no_more_vertex();
    Route get_route();
    Node *copy_and_choose_next_vertex(int vertex, Graph &g);
    vector <int> get_avail_vertexes();

    // link last vertex of the route to first vertex to
    // cloe the loop, also update the cost
    void close_loop(Graph &g);
    void print();
  };

 public:
  // solve the TSP with brute force
  // Return cost of the route.
  Route solve(Graph &g);

};


