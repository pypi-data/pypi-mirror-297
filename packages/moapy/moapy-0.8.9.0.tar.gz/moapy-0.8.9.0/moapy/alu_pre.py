from pydantic import Field as dataclass_field
from moapy.auto_convert import MBaseModel

class AluMaterial(MBaseModel):
    """
    Alu DB Material
    """
    matl: str = dataclass_field(default='2014-T6', description="material name")
    product: str = dataclass_field(default='Extrusions', description="product name")

    class Config(MBaseModel.Config):
        title = "Alu DB Material"
        description = "Alu DB Material"

