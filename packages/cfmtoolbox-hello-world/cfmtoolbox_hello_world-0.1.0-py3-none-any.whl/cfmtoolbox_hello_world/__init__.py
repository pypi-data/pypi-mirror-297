from cfmtoolbox import app, CFM

@app.command()
def hello_world(cfm: CFM) -> CFM:
    print(f"Nice CFM! It even has a Hello World command!")
    return cfm