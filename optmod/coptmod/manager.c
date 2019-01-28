/** @file manager.c
 * 
 * This file is part of OPTMOD
 *
 * Copyright (c) 2019, Tomas Tinoco De Rubira. 
 *
 * OPTMOD is released under the BSD 2-clause license.
 */

#include "manager.h"

struct Manager {

  int max_nodes;
  int num_nodes;
  Node* nodes;
  
  int num_inputs;
  Node** inputs;
  
  int num_outputs;
  double* outputs;
  
  Node* hash;
};

int MANAGER_get_max_nodes(Manager* m) {
  if (m)
    return m->max_nodes;
  else
    return 0;
}

int MANAGER_get_num_nodes(Manager* m) {
  if (m)
    return m->num_nodes;
  else
    return 0;
}

int MANAGER_get_num_inputs(Manager* m) {
  if (m)
    return m->num_inputs;
  else
    return 0;
}

int MANAGER_get_num_outputs(Manager* m) {
  if (m)
    return m->num_outputs;
  else
    return 0;
}

Manager* MANAGER_new(int num_inputs, int num_outputs) {
  int i;
  Manager* m = (Manager*)malloc(sizeof(Manager));  
  m->max_nodes = num_outputs;
  m->num_nodes = 0;
  m->nodes = NODE_array_new(m->max_nodes);
  m->num_inputs = num_inputs;
  m->num_outputs = num_outputs;
  m->inputs = (Node**)malloc(sizeof(Node*)*num_inputs);
  m->outputs = (double*)malloc(sizeof(double)*num_outputs);
  m->hash = NULL;
  for (i = 0; i < m->num_inputs; i++)
    m->inputs[i] = NULL;
  for (i = 0; i < m->num_outputs; i++)
    m->outputs[i] = 0.;
  return m;
}

void MANAGER_inc_num_nodes(Manager* m) {

  // Local vars
  int i;
  Node* n;
  Node* new_n;
  Node* new_nodes;
  Node* new_hash;
  int new_max_nodes;

  // Check
  if (!m)
    return;

  // Increment
  m->num_nodes += 1;

  // Dynamic resize
  if (m->num_nodes >= m->max_nodes) {

    // New nodes
    new_max_nodes = 2*m->max_nodes;
    new_nodes = NODE_array_new(new_max_nodes);

    // New hash
    new_hash = NULL;
    for (i = 0; i < m->num_nodes; i++) {
      n = NODE_array_get(m->nodes, i);
      new_n = NODE_array_get(new_nodes, i);
      NODE_set_id(new_n, NODE_get_id(n));
      new_hash = NODE_hash_add(new_hash, new_n);
    }

    // Copy old node data
    for (i = 0; i < m->num_nodes; i++) {
      n = NODE_array_get(m->nodes, i);
      new_n = NODE_array_get(new_nodes, i);
      NODE_copy_from_node(new_n, n, new_hash);
    }

    // Update hash
    NODE_hash_del(m->hash);
    m->hash = new_hash;

    // Update inputs
    for (i = 0; i < m->num_inputs; i++)
      m->inputs[i] = NODE_hash_find(m->hash, NODE_get_id(m->inputs[i]));

    // Update nodes
    NODE_array_del(m->nodes, m->num_nodes);
    m->nodes = new_nodes;
    m->max_nodes = new_max_nodes;
  }
}

void MANAGER_add_node(Manager* m, int type, long id, double value, long* arg_ids, int num_args) {

  int i;
  Node* n;
  Node* arg;
  Node** args;
  
  if (!m)
    return;
  
  // Root
  n = NODE_hash_find(m->hash, id);  
  if (!n) {
    n = NODE_array_get(m->nodes, m->num_nodes);
    NODE_set_id(n, id);
    m->hash = NODE_hash_add(m->hash, n);
    MANAGER_inc_num_nodes(m);
  }
  NODE_set_type(n, type);
  NODE_set_value(n, value);
  
  // args
  args = (Node**)malloc(sizeof(Node*)*num_args);
  for (i = 0; i < num_args; i++) {
    arg = NODE_hash_find(m->hash, arg_ids[i]);
    if (!arg) {
      arg = NODE_array_get(m->nodes, m->num_nodes);
      NODE_set_id(arg, arg_ids[i]);
      m->hash = NODE_hash_add(m->hash, arg);
      MANAGER_inc_num_nodes(m);
    }
    args[i] = arg;
  }
  
  if (num_args <= 2) {
    NODE_set_arg1(n, args[0]);
    if (num_args > 1)
      NODE_set_arg2(n, args[1]);
    free(args);
  }
  else
    NODE_set_args(n, args, num_args);
}

void MANAGER_del(Manager* m) {
  if (m) {
    NODE_hash_del(m->hash);
    NODE_array_del(m->nodes, m->num_nodes);
    free(m->inputs);
    free(m->outputs);
    free(m);
  }
}

void MANAGER_set_output_node(Manager* m, int index, long id) {

  Node* n;
  
  if (!m)
    return;

  n = NODE_hash_find(m->hash, id);
  if (0 <= index && 0 < m->num_outputs)
    NODE_set_output_index(n, index);
}

void MANAGER_set_input_var(Manager* m, int index, long id) {
  
  Node* n;

  if (!m)
    return;

  n = NODE_hash_find(m->hash, id);
  if (0 <= index && index < m->num_inputs && NODE_get_type(n) == NODE_TYPE_VARIABLE)
    m->inputs[index] = n;
}

void MANAGER_show(Manager* m) {

  int i;

  if (!m)
    return;

  printf("\n");
  printf("Manager\n");
  printf("num_inputs: %d\n", m->num_inputs);
  printf("num_outputs: %d\n", m->num_outputs);
  printf("max_nodes: %d\n", m->max_nodes);
  printf("num_nodes: %d\n\n", m->num_nodes);

  printf("inputs:\n");
  for (i = 0; i < m->num_inputs; i++)
    printf("%ld, ", NODE_get_id(m->inputs[i]));
  printf("\n\n");

  printf("outputs:\n");
  for (i = 0; i < m->num_outputs; i++)
    printf("%.2e, ", m->outputs[i]);
  printf("\n\n");
  
  printf("nodes:\n\n");
  for (i = 0; i < m->num_nodes; i++) {
    NODE_show(NODE_array_get(m->nodes, i));
    printf("\n");
  }
}
