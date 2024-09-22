from typing import Callable, Any

from ._pbm import PBM

def get_pbm() -> PBM:
    return PBM()

def get_base() -> PBM.Base:
    pbm: PBM = get_pbm()

    return pbm.Base(pbm)

def get_dependencies() -> PBM.Dependencies:
    pbm: PBM = get_pbm()

    return pbm.Dependencies(pbm)

def run_pbm(obj: str | Callable, command: str, *args, **kwargs) -> Any:
    obj = eval(obj, {
        "get_pbm": get_pbm,
        "get_base": get_base,
        "get_dependencies": get_dependencies
    })() if isinstance(obj, str) else obj

    return getattr(obj, command)(*args, **kwargs)