import json

import pandas as pd

from ..parsers import (
    api_parser, directory_parser, dropped_file_parser, file_parser,
    network_parser, registry_parser, signature_parser, strings_parser,
    system_parser,
)


PARSER_SPECS = (
    ("api", api_parser, "api_mapping_name.json"),
    ("registry", registry_parser, "registry_mapping_name.json"),
    ("file", file_parser, "file_mapping_name.json"),
    ("directory", directory_parser, "directory_mapping_name.json"),
    ("strings", strings_parser, "string_mapping_name.json"),
    ("network", network_parser, "network_mapping_name.json"),
    ("system", system_parser, "system_mapping_name.json"),
    ("dropped_file", dropped_file_parser, "dropped_file_mapping_name.json"),
    ("signature", signature_parser, "signature_mapping_name.json"),
)


class FeatureService:
    def __init__(self, mappings_dir):
        self.mappings_dir = mappings_dir

    def build(self, report_path):
        report = json.loads(report_path.read_text(encoding="utf-8-sig"))
        row, warnings = {}, []

        for name, parser, mapping_filename in PARSER_SPECS:
            mapping_path = self.mappings_dir / mapping_filename
            if not mapping_path.is_file() or mapping_path.stat().st_size == 0:
                warnings.append({"type": "empty_mapping", "parser": name,
                                 "file": mapping_filename})
                continue
            mapping = json.loads(mapping_path.read_text(encoding="utf-8-sig"))
            observed = parser.extract(report)
            row.update({column: int(feature_name in observed)
                        for column, feature_name in mapping.items()})

        if not row:
            raise ValueError("Khong tao duoc dac trung: cac mapping deu rong hoac bi thieu.")
        return pd.DataFrame([row]), warnings

