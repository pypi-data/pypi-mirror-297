def _define_workflow(workflow):
    waiting = workflow.add_state("waiting", initial=True)
    ongoing = workflow.add_state("ongoing")
    error = workflow.add_state("error")
    successful = workflow.add_state("successful")

    workflow.add_transition("starts", (waiting,), ongoing)
    workflow.add_transition("fails", (ongoing,), error)
    workflow.add_transition("success", (ongoing,), successful)
    return workflow


def create_import_process_workflow(add_workflow):
    workflow = add_workflow("import process workflow", "ImportProcess")
    return _define_workflow(workflow)


def create_task_process_workflow(add_workflow):
    workflow = add_workflow("task process workflow", "TaskProcess")
    return _define_workflow(workflow)
