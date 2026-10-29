"""Deterministic contract for the independent article-rewrite Skill."""
from __future__ import annotations

from copy import deepcopy
from typing import Any


class ContractError(ValueError):
    pass


MODES = {"preserve_structure", "rebuild_from_thread", "rewrite_from_meaning"}


def _text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ContractError(f"字段必须是非空文字：{field}")
    return value.strip()


def _list(value: Any, field: str, minimum: int = 1) -> list[Any]:
    if not isinstance(value, list) or len(value) < minimum:
        raise ContractError(f"字段必须是至少 {minimum} 项的列表：{field}")
    return value


def validate_request(request: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(request, dict) or request.get("schema_version") != "cwf-article-rewrite-request/v1":
        raise ContractError("不是受支持的文章改写请求版本")
    _text(request.get("run_id"), "run_id")
    source = request.get("source")
    if not isinstance(source, dict) or source.get("kind") != "existing_article":
        raise ContractError("文章改写必须提供 existing_article 原文")
    source_text = source.get("text")
    _text(source_text, "source.text")
    task = request.get("task")
    if not isinstance(task, dict):
        raise ContractError("缺少 task")
    genre = _text(task.get("genre"), "task.genre")
    _text(task.get("audience"), "task.audience")
    length = task.get("length")
    if not isinstance(length, dict) or not isinstance(length.get("min_han"), int) or not isinstance(length.get("max_han"), int) or length["min_han"] <= 0 or length["min_han"] > length["max_han"]:
        raise ContractError("task.length 必须包含有效的 min_han/max_han")
    rewrite = request.get("rewrite")
    if not isinstance(rewrite, dict) or rewrite.get("mode") not in MODES:
        raise ContractError("rewrite.mode 必须是三档之一")
    mode = rewrite["mode"]
    preserve = rewrite.get("preserve")
    if not isinstance(preserve, dict):
        raise ContractError("缺少 rewrite.preserve")
    _text(rewrite.get("new_material_policy"), "rewrite.new_material_policy")
    if mode == "preserve_structure":
        _list(preserve.get("structure"), "rewrite.preserve.structure")
        _text(preserve.get("core_meaning"), "rewrite.preserve.core_meaning")
    elif mode == "rebuild_from_thread":
        _text(preserve.get("main_thread"), "rewrite.preserve.main_thread")
        _list(preserve.get("key_people_events"), "rewrite.preserve.key_people_events")
        _text(preserve.get("core_meaning"), "rewrite.preserve.core_meaning")
        _list(rewrite.get("reorganization_plan"), "rewrite.reorganization_plan", minimum=2)
    else:
        _text(preserve.get("core_meaning"), "rewrite.preserve.core_meaning")
        _text(preserve.get("stance"), "rewrite.preserve.stance")
        _text(preserve.get("emotional_landing"), "rewrite.preserve.emotional_landing")
    return {
        "run_id": request["run_id"],
        "genre": genre,
        "rewrite_mode": mode,
        "source_han": sum(1 for char in source_text if "\u4e00" <= char <= "\u9fff"),
        "source_text": source_text,
        "task": deepcopy(task),
        "rewrite": deepcopy(rewrite),
        "style": deepcopy(request.get("style")),
    }


def build_writer_input(request: dict[str, Any], style_payload: dict[str, Any] | None) -> dict[str, Any]:
    checked = validate_request(request)
    return {
        "schema_version": "cwf-article-rewrite-writer-input/v1",
        "task": checked["task"],
        "source_text": checked["source_text"],
        "rewrite": checked["rewrite"],
        "style": style_payload,
    }
