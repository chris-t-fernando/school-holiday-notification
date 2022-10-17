from .iparameter_store import IParameterStore

class Ephemeral(IParameterStore):
    class exceptions:
        class ParameterNotFound(Exception):
            ...

    def __init__(self, store=None):
        self.store = {}

    def put(
        self, path: str, value: str, field_type: str = "String", overwrite: bool = True
    ) -> dict:
        new_path = path not in self.store
        overwrite_path = path in self.store and overwrite == True
        if new_path or overwrite_path:
            self.store[path] = value
            # if len(json.dumps(self.store[path])) > 4096:
            #    raise Exception("Length of dict exceeds 4096 characters")
            return
        if path in self.store and overwrite == False:
            raise ValueError

    def get(self, path: str, with_decryption: bool = True) -> dict:
        if path not in self.store:
            return "[]"
            raise self.exceptions.ParameterNotFound(f"{path} not found in Parameter Store")

        return self.store[path]

    def _bootstrap(self, source:IParameterStore, *args):
        # BOOTSTRAP - put alpaca and slack config into the local store for backtesting
        bootstrap_source = source()

        for this_path in args:
            this_value = bootstrap_source.get(path=this_path)
            self.put(path=this_path, value=this_value)
