
import pandas as pd

class ObservableDataFrame(pd.DataFrame):
    _metadata = ['_change_callbacks']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._change_callbacks = []

    @property
    def _constructor(self):
        return ObservableDataFrame

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self._notify_change()

    def __delitem__(self, key):
        super().__delitem__(key)
        self._notify_change()

    def _notify_change(self):
        for callback in self._change_callbacks:
            callback()

    def register_change_callback(self, callback):
        if callback not in self._change_callbacks:
            self._change_callbacks.append(callback)

    def unregister_change_callback(self, callback):
        if callback in self._change_callbacks:
            self._change_callbacks.remove(callback)
