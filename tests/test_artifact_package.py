"""実データを使わず、梱包→取得→検証→復元と失敗時の保護を通して確認する。"""

import copy
import hashlib
import json
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
import zipfile
from unittest.mock import patch

import src.artifact_package as artifacts

from src.artifact_package import FetchError, fetch, pack, package_plan, sha256_file, validate_zip
from src.research_paths import ResearchPaths


class ArtifactPackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.source = self.root / 'frozen'
        self.source.mkdir()
        (self.source / 'history.csv').write_text('evaluation,value\n1,3\n')
        (self.source / '.gitkeep').write_text('')
        (self.source / '.env').write_text('FAKE_SECRET=do-not-package')
        (self.source / '.venv').mkdir()
        (self.source / '.venv' / 'python').write_text('excluded')
        self.code = self.root / 'code-snapshot'
        self.code.mkdir()
        (self.code / 'run.py').write_text('# frozen execution code\n')
        self.spec = {'schema_version': 1, 'study': 'toy', 'package_id': 'toy-001',
                     'run_ids': ['run_001'], 'code_version': 'snapshot-toy',
                     'compute_status': 'partial', 'snapshot_confirmed': True,
                     'sources': [{'source': str(self.source), 'target': 'data/runs/toy/run_001'},
                                 {'source': str(self.code), 'target': 'code_snapshot'}],
                     'required_paths': ['data/runs/toy/run_001/history.csv', 'code_snapshot/run.py']}
        self.paths = ResearchPaths(self.root / 'project', self.root / 'data',
                                   self.root / 'analysis', self.root / 'cache')
        self.output = self.root / 'ready' / 'toy-001'

    def request(self, source, digest, kind='local'):
        return {'schema_version': 1, 'packages': [{'package_id': 'toy-001',
                'sha256': digest, 'source': {'kind': kind, 'path': str(source)}}]}

    def test_pack_fetch_roundtrip_and_no_overwrite(self):
        plan = package_plan(self.spec)
        self.assertFalse(self.output.exists())
        self.assertIn('data/runs/toy/run_001/.gitkeep', plan['files'])
        self.assertNotIn('data/runs/toy/run_001/.env', plan['files'])
        self.assertTrue(any('.venv' in p for p in plan['excluded_files']))
        report = pack(self.spec, self.output)
        self.assertEqual(report['storage_status'], 'pending')
        request = self.request(self.output / 'artifacts.zip', report['archive_sha256'])
        result = fetch(request, self.paths)[0]
        restored = Path(result['destination'])
        self.assertTrue(result['internal_manifest_verified'])
        self.assertEqual((restored / 'data/runs/toy/run_001/history.csv').read_bytes(),
                         (self.source / 'history.csv').read_bytes())
        self.assertEqual((restored / 'code_snapshot/run.py').read_bytes(), (self.code / 'run.py').read_bytes())
        self.assertTrue((self.source / '.env').exists())
        with self.assertRaises(FileExistsError):
            pack(self.spec, self.output)
        with self.assertRaises(FileExistsError):
            fetch(request, self.paths)

    def test_missing_required_snapshot_and_bad_targets(self):
        for mutation in ['missing', 'snapshot', 'traversal', 'case_collision']:
            with self.subTest(mutation=mutation):
                spec = copy.deepcopy(self.spec)
                if mutation == 'missing':
                    spec['required_paths'].append('missing/checkpoint')
                elif mutation == 'snapshot':
                    spec['snapshot_confirmed'] = False
                elif mutation == 'traversal':
                    spec['sources'][0]['target'] = '../outside'
                else:
                    spec['sources'].append({'source': str(self.code / 'run.py'), 'target': 'CODE_SNAPSHOT/RUN.PY'})
                with self.assertRaises(ValueError):
                    pack(spec, self.output)
                self.assertFalse(self.output.exists())

    def test_changed_source_aborts_without_publishing(self):
        original = artifacts.copy_hashed
        changed = False

        def copy_then_change(source, destination):
            nonlocal changed
            result = original(source, destination)
            if not changed:
                changed = True
                (self.source / 'history.csv').write_text('changed while packaging')
            return result

        with patch.object(artifacts, 'copy_hashed', side_effect=copy_then_change):
            with self.assertRaises(ValueError):
                pack(self.spec, self.output)
        self.assertFalse(self.output.exists())

    def test_output_inside_source_is_rejected(self):
        with self.assertRaises(ValueError):
            pack(self.spec, self.source / 'generated-package')
        self.assertFalse((self.source / 'generated-package').exists())

    def test_partial_batch_failure_reports_already_restored_packages(self):
        report = pack(self.spec, self.output)
        request = self.request(self.output / 'artifacts.zip', report['archive_sha256'])
        second = copy.deepcopy(request['packages'][0])
        second.update(package_id='toy-002', sha256='0'*64)
        request['packages'].append(second)
        with self.assertRaises(FetchError) as captured:
            fetch(request, self.paths)
        self.assertEqual(captured.exception.completed[0]['package_id'], 'toy-001')
        self.assertTrue((self.paths.data_root / '_packages/toy-001').is_dir())
        self.assertFalse((self.paths.data_root / '_packages/toy-002').exists())

    def test_symlinks_are_rejected(self):
        (self.source / 'link.csv').symlink_to(self.code / 'run.py')
        with self.assertRaises(ValueError):
            pack(self.spec, self.output)

    def test_wrong_archive_checksum_leaves_no_restore(self):
        pack(self.spec, self.output)
        with self.assertRaises(ValueError):
            fetch(self.request(self.output / 'artifacts.zip', '0'*64), self.paths)
        self.assertFalse((self.paths.data_root / '_packages/toy-001').exists())

    def test_tampered_manifest_blocks_restore_even_with_new_outer_hash(self):
        pack(self.spec, self.output)
        tampered = self.root / 'tampered.zip'
        with zipfile.ZipFile(self.output / 'artifacts.zip') as src, zipfile.ZipFile(tampered, 'w') as dst:
            for name in src.namelist():
                dst.writestr(name, b'changed' if name.endswith('history.csv') else src.read(name))
        with self.assertRaises(ValueError):
            fetch(self.request(tampered, sha256_file(tampered)), self.paths)
        self.assertFalse((self.paths.data_root / '_packages/toy-001').exists())

    def test_malicious_zip_paths_and_links(self):
        for variant in ['../escaped', 'link', 'duplicate', 'case_parent']:
            with self.subTest(variant=variant):
                path = self.root / 'malicious.zip'
                with zipfile.ZipFile(path, 'w') as archive:
                    if variant == '../escaped':
                        archive.writestr('../escaped', b'x')
                    elif variant == 'link':
                        info = zipfile.ZipInfo('link')
                        info.external_attr = (stat.S_IFLNK | 0o777) << 16
                        archive.writestr(info, b'outside')
                    elif variant == 'duplicate':
                        archive.writestr('A', b'x')
                        archive.writestr('a', b'x')
                    else:
                        archive.writestr('A', b'x')
                        archive.writestr('a/b', b'x')
                    names = [i.filename for i in archive.infolist()]
                    archive.writestr('manifest.json', json.dumps({'schema_version': 1, 'package_id': 'toy-001',
                        'files': [{'path': n, 'size': 1, 'sha256': hashlib.sha256(b'x').hexdigest()} for n in names]}))
                with self.assertRaises(ValueError):
                    fetch(self.request(path, sha256_file(path)), self.paths)
                self.assertFalse((self.root / 'escaped').exists())
                self.assertFalse((self.paths.data_root / '_packages/toy-001').exists())

    def test_archive_only_retains_legacy_bytes_without_claiming_internal_validation(self):
        legacy = self.root / 'checkpoints.tar'
        legacy.write_bytes(b'legacy archive opaque to this tool')
        result = fetch(self.request(legacy, sha256_file(legacy)), self.paths, archive_only=True)[0]
        self.assertTrue(result['archive_verified'])
        self.assertFalse(result['internal_manifest_verified'])
        self.assertIsNone(result['destination'])

    @unittest.skipUnless(shutil.which('rclone'), 'rclone is optional for local-only tests')
    def test_rclone_directory_is_not_downloaded(self):
        with self.assertRaises(ValueError):
            fetch(self.request(self.source, '0'*64, 'rclone'), self.paths)
        self.assertFalse((self.paths.data_root / '_packages/toy-001').exists())

    @unittest.skipUnless(shutil.which('rclone'), 'rclone is optional for local-only tests')
    def test_cli_rclone_download_with_local_backend(self):
        # rclone自体のcopytoを通す。ネットワーク・Drive認証は使わない。
        script = Path(__file__).resolve().parents[1] / 'scripts/artifacts.py'
        spec_path = self.root / 'spec.json'
        spec_path.write_text(json.dumps(self.spec))
        subprocess.run([sys.executable, str(script), 'pack', '--spec', str(spec_path),
                        '--output', str(self.output)], capture_output=True, check=True)
        digest = sha256_file(self.output / 'artifacts.zip')
        request_path = self.root / 'request.json'
        request_path.write_text(json.dumps(self.request(self.output / 'artifacts.zip', digest, 'rclone')))
        paths_file = self.root / 'paths.json'
        paths_file.write_text(json.dumps({'profiles': {'mac': {
            k: str(getattr(self.paths, k)) for k in self.paths.__dataclass_fields__}}}))
        completed = subprocess.run([sys.executable, str(script), 'fetch', '--request', str(request_path),
                                   '--paths', str(paths_file), '--profile', 'mac'],
                                  capture_output=True, text=True, check=True)
        result = json.loads(completed.stdout)[0]
        self.assertTrue(result['internal_manifest_verified'])
        self.assertTrue(Path(result['destination']).is_dir())


if __name__ == '__main__':
    unittest.main()
