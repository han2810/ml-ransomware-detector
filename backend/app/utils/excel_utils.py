EXCEL_MAX_COLUMNS = 16_384


def validate_excel_width(frame):
    if len(frame.columns) > EXCEL_MAX_COLUMNS:
        raise ValueError(f"So cot ({len(frame.columns)}) vuot gioi han Excel.")

