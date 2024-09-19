from cubicweb import Binary

dataservice = cnx.create_entity(
    "DataService",
    data_url="https://dbpedia.org/resource/Leonardo_da_Vinci",
    name="DBpedia Leo",
)
recipe = cnx.create_entity(
    "ImportRecipe",
    name="Ma recette",
    dataservice=[dataservice],
)

with open("./test/data/dboPerson.rdf", "rb") as fp:
    file = cnx.create_entity(
        "File",
        **{
            "title": f"dboPerson.rdf",
            "data": Binary(fp.read()),
            "data_format": "application/rdf+xml",
            "data_name": "dbo:person ontology",
        },
    )

with open("./test/data/ok_shacl.ttl", "rb") as fp:
    ok_shacl = cnx.create_entity(
        "File",
        **{
            "title": f"ok_shacl.ttl",
            "data": Binary(fp.read()),
            "data_format": "text/turtle",
            "data_name": "shacl ok",
        },
    )


with open("./test/data/nok_shacl.ttl", "rb") as fp:
    nok_shacl = cnx.create_entity(
        "File",
        **{
            "title": f"nok_shacl.ttl",
            "data": Binary(fp.read()),
            "data_format": "text/turtle",
            "data_name": "shacl nok",
        },
    )


importprocedure = cnx.create_entity(
    "ImportProcedure",
    sparql_endpoint="https://sparql.poulet",
    import_recipes=[recipe],
    ontology_file=file,
    shacl_files=[ok_shacl, nok_shacl],
)
cnx.commit()
