import xxhash


def get_hash(buf):
    if not isinstance(buf, bytes):
        raise RuntimeError('buffer should bytes object')

    hash = xxhash.xxh64()
    hash.update(buf)

    return buf.hexdigest()
