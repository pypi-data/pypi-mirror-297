from typing import Any, Dict, Iterable, List

def inject_create_tags(
    event_name: str, class_attributes: Dict[str, Any], **kwargs: Any
) -> None: ...
def create_tags(self: Any, **kwargs: Iterable[Any]) -> List[Dict[str, Any]]: ...
