from moapy.auto_convert import auto_schema
from moapy.data_pre import MemberForce, EffectiveLength
from moapy.data_post import ResultMD
from moapy.steel_pre import SteelSection, SteelLength_EC, SteelMomentModificationFactor_EC
from moapy.alu_pre import AluMaterial
from moapy.dgnengine.base import generate_report, load_dll

@auto_schema
def report_aluminum_beam_column(matl: AluMaterial, sect: SteelSection, load: MemberForce, length: SteelLength_EC, eff_len: EffectiveLength, factor: SteelMomentModificationFactor_EC) -> ResultMD:
    dll = load_dll()
    json_data_list = [matl.json(), sect.json(), load.json(), length.json(), eff_len.json(), factor.json()]
    return generate_report(dll, 'Report_Aluminum_BeamColumn', json_data_list)