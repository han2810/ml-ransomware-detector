from ..utils.excel_utils import validate_excel_width


class ExcelService:
    def write(self, feature_frame, output_path):
        validate_excel_width(feature_frame)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        feature_frame.to_excel(output_path, index=False, engine="openpyxl")
        return output_path

