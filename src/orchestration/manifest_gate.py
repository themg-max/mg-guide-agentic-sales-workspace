import yaml
from pathlib import Path
from typing import Set

class RuntimeManifestGate:
    def __init__(self, manifest_path: Path):
        data = yaml.safe_load(manifest_path.read_text())
        self.blocked_classes: Set[str] = set(data.get("blocked_capability_classes", []))
        self._classifier_map = {
            "create-contact": "contact_create",
        }

    def classify_operation(self, operation_id: str) -> str:
        return self._classifier_map.get(operation_id, f"unknown:{operation_id}")

    def is_blocked(self, operation_id: str) -> bool:
        cap_class = self.classify_operation(operation_id)
        return cap_class in self.blocked_classes
