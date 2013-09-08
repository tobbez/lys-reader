from imp import new_module

def get_config():
    module = new_module('config')
    module.__file__ = 'config.py'
    config = {}
    config_file = open(module.__file__)
    
    exec(compile(config_file.read(), 'config.py', 'exec'), module.__dict__)
    
    for key in dir(module):
        if key.isupper():
            config[key] = getattr(module, key)
    return config
