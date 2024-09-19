from attr import field, define
from typing import List

__ALL__ = ["ForeignKeyDef"]


@define
class ForeignKeyDef:
    """
    Represents one foreign key.
    """

    src_columns: List[str] = field(converter=list)
    """
    The referencing columns (in this table)
    """

    ref_table: str
    """
    The referenced table name
    """

    ref_columns: List[str] = field(converter=list)
    """
    The referenced columns (in the referenced table)
    """
