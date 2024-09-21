from io import BufferedReader
from typing import Optional, BinaryIO, Union, Any

from pydantic import BaseModel, Field

from dvr_pdf.util.enums import PaginationPosition, ElementType, PageBehavior, ElementAlignment, Font, AlignSetting, \
    TableStyleName
from dvr_pdf.util.util import px_to_pt


class PDFElement(BaseModel):
    x: int
    y: int
    width: int
    height: int
    element_type: ElementType = Field(alias='elementType')
    page_behaviour: PageBehavior = Field(alias='pageBehavior')
    alignment: Optional[ElementAlignment] = None

    @property
    def x_pt(self):
        return px_to_pt(self.x)

    @property
    def y_pt(self):
        return px_to_pt(self.y)

    @property
    def width_pt(self):
        return px_to_pt(self.width)

    @property
    def height_pt(self):
        return px_to_pt(self.height)


class PDFTextElement(PDFElement):
    text: str
    font_size: Optional[int] = Field(alias='fontSize', default=None)
    font: Optional[Font] = None
    color: Optional[str] = None


class PDFImageElement(PDFElement):
    class Config:
        arbitrary_types_allowed = True

    image: Union[BinaryIO, BufferedReader]


class PDFBackgroundElement(PDFElement):
    color: str


class ConfigurableTableElement(BaseModel):
    bold: Optional[bool] = False
    italic: Optional[bool] = False
    background_color: Optional[str] = Field(alias='backgroundColor', default=None)
    color: Optional[str] = None
    border_bottom_color: Optional[str] = Field(alias='borderBottomColor', default=None)
    border_top_color: Optional[str] = Field(alias='borderTopColor', default=None)


class PDFCellElement(ConfigurableTableElement):
    text: Union[str, float, int]
    text_alignment: Optional[AlignSetting] = Field(alias='textAlignment', default=None)


class PDFRowElement(ConfigurableTableElement):
    columns: list[PDFCellElement]
    key: str


class PDFTableElement(PDFElement):
    rows: list[PDFRowElement]
    column_widths: list[int] = Field(alias='columnWidths')
    font: Optional[Font] = None
    font_size: Optional[int] = Field(alias='fontSize', default=None)
    background_color: Optional[str] = Field(alias='backgroundColor', default=None)
    color: Optional[str] = None
    border_color: Optional[str] = Field(alias='borderColor', default=None)


class Pagination(BaseModel):
    position: PaginationPosition
    render_total_pages: bool = Field(alias='renderTotalPages')


class PDFTemplate(BaseModel):
    font: Font
    font_size: int = Field(alias='fontSize')
    pagination: Pagination
    elements: list[dict]
    background_color: Optional[str] = Field(alias='backgroundColor', default=None)


TableStyleProp = tuple[TableStyleName, tuple[int, int], tuple[int, int], Any]
