#!/usr/bin/env python3
"""保存対象の確認・梱包・検証と必要パッケージの取得・展開（Python 3.10+）。"""

import argparse
import json
from pathlib import Path
import subprocess
import sys
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.artifact_package import FetchError, fetch, pack, package_plan, validate_zip
from src.research_paths import load_paths


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    create = commands.add_parser('pack', help='対象一覧を確認して新しいZIPパッケージを作る')
    create.add_argument('--spec', type=Path, required=True)
    create.add_argument('--output', type=Path)
    create.add_argument('--dry-run', action='store_true')
    verify = commands.add_parser('verify', help='ZIP全体と内部manifestを検証する')
    verify.add_argument('--archive', type=Path, required=True)
    verify.add_argument('--sha256', required=True)
    restore = commands.add_parser('fetch', help='必要なパッケージだけ取得・検証・展開する')
    restore.add_argument('--request', type=Path, required=True)
    restore.add_argument('--paths', type=Path, required=True)
    restore.add_argument('--profile', required=True)
    restore.add_argument('--archive-only', action='store_true', help='SHA-256照合のみ。旧tar等を自動展開しない')
    args = parser.parse_args()
    try:
        if args.command == 'pack':
            spec = json.loads(args.spec.read_text())
            if not args.dry_run and args.output is None:
                parser.error('packには--outputまたは--dry-runが必要です')
            result = package_plan(spec) if args.dry_run else pack(spec, args.output)
        elif args.command == 'verify':
            manifest = validate_zip(args.archive, args.sha256)
            result = {'package_id': manifest['package_id'], 'files': len(manifest['files']),
                      'package_validation_status': 'passed'}
        else:
            request = json.loads(args.request.read_text())
            paths = load_paths(args.paths, args.profile)
            result = fetch(request, paths, args.archive_only)
    except (OSError, ValueError, KeyError, TypeError, zipfile.BadZipFile, subprocess.CalledProcessError) as error:
        if isinstance(error, FetchError) and error.completed:
            print(json.dumps({'completed_packages': error.completed}, ensure_ascii=False, indent=2))
        parser.exit(1, f'処理を停止しました: {error}\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
