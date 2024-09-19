add_attribute("ImportProcedure", "shacl_file")
for procedure in cnx.find("ImportProcedure").entities():
    if procedure.shacl_files:
        last_shacl_file = procedure.shacl_files[-1]
        procedure.cw_set(shacl_file=last_shacl_file)
drop_attribute("ImportProcedure", "shacl_files")
sync_schema_props_perms()
