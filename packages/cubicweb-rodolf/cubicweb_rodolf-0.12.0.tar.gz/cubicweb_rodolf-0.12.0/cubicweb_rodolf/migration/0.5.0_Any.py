from functools import cache

add_entity_type("ProcessType")
add_relation_definition("ImportRecipe", "use_process", "ProcessType")

process_type_label_map = {
    "default": "Processus d'import standard",
    "default-dryrun": "Processus d'import standard sans publication",
}


@cache
def get_process(process_type):
    return cnx.create_entity(
        "ProcessType",
        name=process_type_label_map.get(process_type, process_type),
        regid=process_type,
        activated=False,
    )


for recipe in cnx.find("ImportRecipe").entities():
    # create a deactivated process
    # the process, if the corresponding code exists, will be activated on
    # startup
    process = get_process(recipe.process_type)
    recipe.cw_set(use_process=process)

drop_attribute("ImportRecipe", "process_type")
sync_schema_props_perms()
