from libc.stdint cimport uintptr_t
cdef extern from "evaluator.h":

    ctypedef struct Evaluator

    void EVALUATOR_add_node(Evaluator* e, int type, uintptr_t id, double value, uintptr_t* arg_ids, int num_args)
    void EVALUATOR_del(Evaluator* e)
    void EVALUATOR_eval(Evaluator* e, double* var_values)
    int EVALUATOR_get_max_nodes(Evaluator* e)
    int EVALUATOR_get_num_nodes(Evaluator* e)
    int EVALUATOR_get_num_inputs(Evaluator* e)
    int EVALUATOR_get_num_outputs(Evaluator* e)
    double* EVALUATOR_get_values(Evaluator* e)
    Evaluator* EVALUATOR_new(int num_inputs, int num_outputs)
    void EVALUATOR_set_output_node(Evaluator* e, int index, uintptr_t id)
    void EVALUATOR_set_input_var(Evaluator* e, int index, uintptr_t id)
    void EVALUATOR_show(Evaluator* e)
