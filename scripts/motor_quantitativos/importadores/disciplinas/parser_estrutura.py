"""Compatibilidade bloqueada do parser legado de estrutura.

Use `extrair_estrutura` pelo roteador contratual.
"""


class ParserEstrutura:
    def __init__(self, *_args, **_kwargs):
        raise RuntimeError("ParserEstrutura legado desativado; use extrair_estrutura")
