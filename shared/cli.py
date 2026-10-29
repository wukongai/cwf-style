"""Small deterministic CLI for the public repository."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .distillation_contract import validate_distillation_request
from .rewrite_contract import validate_request
from .style_library import load_library, resolve_style


def main() -> int:
    parser = argparse.ArgumentParser(prog="cwf-style")
    sub = parser.add_subparsers(dest="command", required=True)
    library = sub.add_parser("library")
    library_sub = library.add_subparsers(dest="library_command", required=True)
    list_cmd = library_sub.add_parser("list")
    list_cmd.add_argument("--index", required=True)
    show_cmd = library_sub.add_parser("show")
    show_cmd.add_argument("--index", required=True)
    show_cmd.add_argument("--style-id", required=True)
    show_cmd.add_argument("--genre")
    rewrite = sub.add_parser("rewrite")
    rewrite_sub = rewrite.add_subparsers(dest="rewrite_command", required=True)
    rewrite_validate = rewrite_sub.add_parser("validate")
    rewrite_validate.add_argument("--request", required=True)
    distill = sub.add_parser("distill")
    distill_sub = distill.add_subparsers(dest="distill_command", required=True)
    distill_validate = distill_sub.add_parser("validate")
    distill_validate.add_argument("--request", required=True)
    args = parser.parse_args()
    if args.command == "library":
        library_data = load_library(args.index)
        if args.library_command == "list":
            print(json.dumps(library_data["entries"], ensure_ascii=False, indent=2))
        else:
            print(json.dumps(resolve_style(library_data, args.style_id, args.genre), ensure_ascii=False, indent=2))
        return 0
    request = json.loads(Path(args.request).read_text(encoding="utf-8"))
    if args.command == "rewrite":
        print(json.dumps(validate_request(request), ensure_ascii=False, indent=2))
    else:
        print(json.dumps(validate_distillation_request(request), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
