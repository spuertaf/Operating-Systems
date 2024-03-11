class Dtypes:
    DTYPE_N_BYTES = {
        'int8': 4,
        'int16': 4,
        'int32': 4,
        'int64': 8,
        'uint8': 4,
        'uint16': 4,
        'uint32': 4,
        'uint64': 8,
        'float16': 2,
        'float32': 4,
        'float64': 8,
    }

    @classmethod
    def get_dtype_bytes(cls, dtype: str):
        return cls.DTYPE_N_BYTES[dtype]