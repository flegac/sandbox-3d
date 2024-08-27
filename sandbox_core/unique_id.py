class UniqueId:
    gen_id: int = 0

    @staticmethod
    def next():
        idx = UniqueId.gen_id
        UniqueId.gen_id += 1
        return idx
