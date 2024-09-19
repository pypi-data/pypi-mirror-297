add_attribute("ImportProcedure", "sparql_url")

for import_procedure in cnx.find("ImportProcedure").entities():
    if not import_procedure.sparql_url:
        import_procedure.cw_set(sparql_url=import_procedure.virtuoso_url)

commit()
