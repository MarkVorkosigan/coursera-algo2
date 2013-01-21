#include "tsp.h"
#include <list>
#include <assert.h>
#include <stdlib.h>

Graph::Graph(int size)
{
  this->mat.clear();
  for(int i = 0; i < size; i ++) {
    vector <float> row(size);
    this->mat.push_back(row);
    for(int j = 0; j < size; j ++) {
      this->mat[i][j] = 0;
    }
    mat[i][i] = 0;
  }
}

Graph::Graph(vector <vector <float> > &mat) {

  this->mat = mat;
}

void Graph::fill_mat() {

  for(int i = 0; i < this->mat.size(); i ++){
    for(int j = i + 1; j < this->mat.size(); j ++) {
      this->mat[j][i] = this->mat[i][j];
    }
  }
}

void Graph::set_edge_cost(int s, int t, float v) {

  mat[s][t] = v;
  mat[t][s] = v;
}

float Graph::get_edge_cost(int s, int t){
  return this->mat[s][t];
}

void Graph::print_mat(){
  for(int i = 0; i < this->mat.size(); i++) {
    for(int j = 0; j < this->mat.size(); j++) {
      cout << mat[i][j] << " ";
    }
    cout << endl;
  }
}

vector <int> Graph::get_all_vertexes() {
  vector <int> v;
  for( int i = 0; i < this->mat.size(); i ++) {
    v.push_back(i);
  }
  return v;
}

void Route::print() {

  cout << "Route: ";
  for(int i = 0; i < this->route.size(); i ++)
    cout << this->route[i] << "->";
  cout << endl;
  cout << "Cost: " << this->cost << endl;
}

Bruteforce_Solver::Node::Node(vector <int> &vertexes){
  this->avail_vertexes = vertexes;
  this->cur_route_cost = 0;
}

bool Bruteforce_Solver::Node::no_more_vertex() {

  return this->avail_vertexes.size() == 0;
}

Route Bruteforce_Solver::Node::get_route() {
  Route r = Route();
  r.route = this->cur_route;
  r.cost = this->cur_route_cost;
  return r;
}

Bruteforce_Solver::Node::Node(Node *n) {
  this->cur_route = n->cur_route;
  this->cur_route_cost = n->cur_route_cost;
  this->avail_vertexes = n->avail_vertexes;
}

void Bruteforce_Solver::Node::print() {
  
  if (this->cur_route.size() == 0) {
    cout << "Empty route" << endl;
  } else {
    cout << "Route: ";
    for(int i = 0; i < this->cur_route.size(); i ++ ){
      cout << this->cur_route[i] << " ";
    }
    cout << endl;
  }

  if (this->avail_vertexes.size() == 0) {
    cout << "No more vertexs" << endl;
  } else {
    cout << "Vertexes: ";
    for(int i = 0; i < this->avail_vertexes.size(); i ++) {
      cout << this->avail_vertexes[i] << " ";
    }
    cout << endl;
  }

  cout << "Cost: " << this->cur_route_cost << endl;
}

Bruteforce_Solver::Node *Bruteforce_Solver::Node::copy_and_choose_next_vertex(int vertex, Graph &g) {

  Bruteforce_Solver::Node *new_node = new Node(this);

  // Remove vertex from avaiable list
  vector <int> new_vertexes;
  for (int i = 0; i < this->avail_vertexes.size(); i ++) {
    if (this->avail_vertexes[i] != vertex)
      new_vertexes.push_back(this->avail_vertexes[i]);
  }
  new_node->avail_vertexes = new_vertexes;

  // Add vertex as new node's last leg
  if (this->cur_route.size() > 0) {
    int last_v = this->cur_route[this->cur_route.size()-1];
    new_node->cur_route.push_back(vertex);
    new_node->cur_route_cost += g.get_edge_cost(last_v, vertex);
  } else {
    new_node->cur_route.push_back(vertex);
    new_node->cur_route_cost = 0;
  }

  return new_node;
}

vector <int> Bruteforce_Solver::Node::get_avail_vertexes() {
  return this->avail_vertexes;
}

// link last vertex of the route to first vertex to
// cloe the loop, also update the cost
void Bruteforce_Solver::Node::close_loop(Graph &g) {

  int last_vertex = this->cur_route[this->cur_route.size()-1];
  int first_vertex = this->cur_route[0];
  this->cur_route.push_back(first_vertex);
  this->cur_route_cost += g.get_edge_cost(last_vertex, first_vertex);
}

Route Bruteforce_Solver::solve(Graph &g)
{
  list <Node*> stack;

  vector <int> all_vertexes = g.get_all_vertexes();
  Node *init_node = new Node(all_vertexes);
  stack.push_front(init_node);

  Route best_result;
  best_result.cost = 10000000000.0;

  while (!stack.empty())
  {

    Bruteforce_Solver::Node *cur_node = stack.front();
    stack.pop_front();

    if (cur_node->no_more_vertex())
    {
      cur_node->close_loop(g);
      Route cur_route = cur_node->get_route();
      if (cur_route.cost < best_result.cost)
      {
	best_result = cur_route;
      }
      delete(cur_node);
      continue;
    }

    vector <int> avail_vertexes = cur_node->get_avail_vertexes();
    vector <int>::iterator it;
    for(it = avail_vertexes.begin(); it != avail_vertexes.end(); it ++)
    {
      int v = (*it);
      Node *next_node = cur_node->copy_and_choose_next_vertex(v, g);
      stack.push_front(next_node);
    }
    delete(cur_node);
  }

  return best_result;
}

// Generate a random problem
Graph gen_problem(int prob_size, int edge_cost_lb=1, int edge_cost_ub=20) {
  Graph g(prob_size);

  for(int i = 0; i < prob_size; i ++) {

    for(int j = i + 1; j < prob_size; j ++) {
      int edge_cost = rand() % (edge_cost_ub - edge_cost_lb + 1) + edge_cost_lb;
      g.set_edge_cost(i, j, edge_cost);
    }
  }
  return g;
}

void test_case_1() {

  Graph g(3);

  g.set_edge_cost(0, 1, 1);
  g.set_edge_cost(1, 2, 2);
  g.set_edge_cost(2, 0, 3);

  g.print_mat();

  Bruteforce_Solver bf;
  Route r = bf.solve(g);

  r.print();
  assert(r.cost == 6);

}

void test_case_2() {

  Graph g(4);
  g.set_edge_cost(0, 1, 1);
  g.set_edge_cost(0, 2, 2);
  g.set_edge_cost(0, 3, 4);
  g.set_edge_cost(1, 2, 2);
  g.set_edge_cost(1, 3, 3);
  g.set_edge_cost(2, 3, 3);

  g.print_mat();

  Bruteforce_Solver bf;
  Route r = bf.solve(g);

  r.print();
  assert(r.cost == 9);

}

void rand_tests() {

  for(int i = 0; i < 200; i ++) {

    int prob_size = 1 + rand() % 10;
    Graph g = gen_problem(prob_size);
    cout << "Problem size: " << prob_size << endl;
    g.print_mat();
    Bruteforce_Solver bf;
    Route r = bf.solve(g);
    r.print();
  }
}

int main() {
  test_case_1();
  test_case_2();
  rand_tests();
}

