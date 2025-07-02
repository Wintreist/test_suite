from pydantic import BaseModel


class TestSuiteParams(BaseModel):
    @property
    def kwargs(self):
        return self.model_dump()

    @property
    def params_without_descriptions(self):
        kwargs = {}
        for key, value in self.kwargs.items():
            if isinstance(value, tuple) and len(value) == 2:
                value = value[0]
            kwargs[key] = value
        return kwargs

    def get(self, item, default=None):
        return self.kwargs.get(item, default)

    def update(self, data):
        return self.kwargs.update(data)

    def items(self):
        return self.kwargs.items()

    def __getitem__(self, item):
        return self.kwargs[item]

    def __setitem__(self, key, value):
        self.kwargs[key] = value

    def _to_dict(self):
        return {"kwargs": self.kwargs}

    @classmethod
    def _from_dict(cls, dict_):
        return cls(**dict_["kwargs"])

    def __bool__(self):
        return bool(self.kwargs)
