class ASTNode:
    def __init__(self, ntype, **kwargs):
        self.type = ntype
        self.__dict__.update(kwargs)
