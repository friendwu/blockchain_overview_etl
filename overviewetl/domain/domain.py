from dataclasses import asdict, fields


class Domain:
    def asdict(self, remove_none_fields=True):
        d = asdict(self)

        # if remove_none_fields:
        #     for k, v in dict(d).items():
        #         if v is None:
        #             del d[k]

        return d

    @classmethod
    @property
    def fields(cls):
        return [f.name for f in fields(cls)]

    def __repr__(self):
        return f"{self.__class__.__name__}({self.asdict()})"