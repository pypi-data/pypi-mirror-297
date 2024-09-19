from cubicweb_rodolf.workflows import create_task_process_workflow


add_entity_type("TaskType")
add_entity_type("TaskProcess")
add_entity_type("ProjectTask")
add_relation_definition("ImportProcedure", "tasks", "ProjectTask")
sync_schema_props_perms()
commit()
create_task_process_workflow(add_workflow)
