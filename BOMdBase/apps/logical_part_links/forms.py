from logical_parts.forms import LogicalPartBaseForm
from manufacturer_parts.forms import ManufacturerPartBaseForm

class LogicalPart2ManufacturerPartForm(
    LogicalPartBaseForm,
    ManufacturerPartBaseForm
):
    pass