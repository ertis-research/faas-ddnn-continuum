# wsk action create helloPY hello.py
# wsk action invoke helloPY --result --param name world
def main(dict):
    name = dict['name'] if 'name' in dict else 'unknown'
    return {"greeting": f'Hello {name}'}
