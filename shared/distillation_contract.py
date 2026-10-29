"""Deterministic contract for the independent style-distillation Skill."""
from __future__ import annotations

from typing import Any


class DistillationError(ValueError):
    pass


def _text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise DistillationError(f"字段必须是非空文字：{field}")
    return value.strip()


def validate_distillation_request(request: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(request, dict) or request.get("schema_version") != "cwf-style-distillation-request/v1":
        raise DistillationError("不是受支持的文风蒸馏请求版本")
    _text(request.get("run_id"), "run_id")
    if "rewrite_mode" in request:
        raise DistillationError("文风蒸馏不接受文章改写档位")
    subject = request.get("subject")
    if not isinstance(subject, dict) or subject.get("kind") not in {"public_author", "personal"}:
        raise DistillationError("subject.kind 必须是 public_author 或 personal")
    for field in ("name", "genre", "purpose"):
        _text(subject.get(field), f"subject.{field}")
    sources = request.get("sources")
    if not isinstance(sources, list) or len(sources) < 2:
        raise DistillationError("文风蒸馏至少需要两个来源记录")
    families = set()
    for source in sources:
        if not isinstance(source, dict):
            raise DistillationError("source 必须是对象")
        for field in ("id", "url", "family", "split"):
            _text(source.get(field), f"source.{field}")
        if source["split"] not in {"development", "holdout", "excluded"}:
            raise DistillationError("source.split 不支持")
        families.add(source["family"])
    if len(families) < 2:
        raise DistillationError("来源必须覆盖至少两个独立作品家族")
    outputs = request.get("outputs")
    if not isinstance(outputs, dict):
        raise DistillationError("缺少 outputs")
    _text(outputs.get("profile_id"), "outputs.profile_id")
    if outputs.get("status") not in {"draft", "research_trial", "scenario_validated", "user_confirmed"}:
        raise DistillationError("outputs.status 不支持")
    return {"run_id": request["run_id"], "subject": subject, "sources": sources, "outputs": outputs}
