"""Read and validate the shared style library."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class LibraryError(ValueError):
    pass


CALLABLE_STATUSES = {"research_trial", "scenario_validated", "user_confirmed"}
REQUIRED_ENTRY_FIELDS = {"id", "display_name", "genre", "profile", "status", "availability", "limitations"}


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise LibraryError(f"无法读取文风档案：{path}") from exc
    if not isinstance(value, dict):
        raise LibraryError(f"文风档案必须是对象：{path}")
    return value


def _safe_relative(root: Path, relative: str) -> Path:
    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError as exc:
        raise LibraryError(f"文风库路径越界：{relative}") from exc
    return candidate


def _validate_profile(profile: dict[str, Any], entry_id: str) -> None:
    required = {"schema_version", "mode", "id", "version", "scope", "rules", "expression_guides"}
    missing = required - set(profile)
    if missing:
        raise LibraryError(f"文风档案缺少字段：{entry_id}: {sorted(missing)}")
    if profile["schema_version"] != "cwf-public-style-profile/v2":
        raise LibraryError(f"文风档案版本不支持：{entry_id}")
    if profile["id"] != entry_id:
        raise LibraryError(f"文风档案 id 与文风卡不一致：{entry_id}")
    if profile["mode"] not in {"public_author_research", "personal"}:
        raise LibraryError(f"文风档案 mode 不支持：{entry_id}")
    if not isinstance(profile["scope"], list) or not profile["scope"]:
        raise LibraryError(f"文风档案 scope 不能为空：{entry_id}")
    if not isinstance(profile["rules"], list) or not profile["rules"]:
        raise LibraryError(f"文风档案 rules 不能为空：{entry_id}")
    if not isinstance(profile["expression_guides"], list) or not profile["expression_guides"]:
        raise LibraryError(f"文风档案必须有完整表达说明：{entry_id}")


def load_library(index_path: str | Path) -> dict[str, Any]:
    index_path = Path(index_path).resolve()
    root = index_path.parent
    index = _read_json(index_path)
    if index.get("schema_version") != "cwf-style-library/v1":
        raise LibraryError("文风库版本不支持")
    entries = index.get("entries")
    if not isinstance(entries, list) or not entries:
        raise LibraryError("文风库 entries 不能为空")
    seen: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise LibraryError("文风卡必须是对象")
        missing = REQUIRED_ENTRY_FIELDS - set(entry)
        if missing:
            raise LibraryError(f"文风卡缺少字段：{sorted(missing)}")
        entry_id = entry["id"]
        if not isinstance(entry_id, str) or not entry_id or entry_id in seen:
            raise LibraryError(f"文风卡 id 无效或重复：{entry_id}")
        seen.add(entry_id)
        if entry["status"] not in {"draft", "research_trial", "scenario_validated", "user_confirmed", "archived"}:
            raise LibraryError(f"文风卡状态不支持：{entry_id}")
        if entry["availability"] not in {"callable", "needs_build", "archived"}:
            raise LibraryError(f"文风卡可用状态不支持：{entry_id}")
        if not isinstance(entry["genre"], list) or not entry["genre"]:
            raise LibraryError(f"文风卡 genre 不能为空：{entry_id}")
        if not isinstance(entry["limitations"], list):
            raise LibraryError(f"文风卡 limitations 必须是列表：{entry_id}")
        profile_path = _safe_relative(root, entry["profile"])
        profile = _read_json(profile_path)
        if entry["availability"] == "callable":
            _validate_profile(profile, entry_id)
    return {"schema_version": index["schema_version"], "entries": entries, "root": root}


def resolve_style(library: dict[str, Any], style_id: str, genre: str | None = None) -> dict[str, Any]:
    entry = next((item for item in library["entries"] if item["id"] == style_id), None)
    if entry is None:
        raise LibraryError(f"找不到文风卡：{style_id}")
    if entry["availability"] != "callable" or entry["status"] not in CALLABLE_STATUSES:
        raise LibraryError(f"文风卡当前不可调用：{style_id}")
    if genre is not None and genre not in entry["genre"]:
        raise LibraryError(f"文风卡与当前体裁不匹配：{style_id} / {genre}")
    profile_path = _safe_relative(library["root"], entry["profile"])
    return {"entry": entry, "profile": _read_json(profile_path), "profile_path": entry["profile"]}
