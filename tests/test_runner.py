"""Verifica o relatório com suítes artificiais em uma pasta temporária."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


class RunnerTests(unittest.TestCase):
    def run_suite(self, body, *args):
        with tempfile.TemporaryDirectory(prefix='suite report ') as folder:
            root = Path(folder)
            shutil.copy2(Path(__file__).with_name('run.py'), root / 'run.py')
            (root / 'test_fixture.py').write_text('import unittest\n' + body)
            return subprocess.run([sys.executable, str(root / 'run.py'), *args],
                                  cwd='/', capture_output=True, text=True, timeout=10)

    def test_success_from_another_directory(self):
        result = self.run_suite('class Sample(unittest.TestCase):\n    def test_ok(self): pass\n')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('[OK] Sample: 1/1 passaram', result.stdout)

    def test_skipped_is_visible_and_strict_rejects_it(self):
        body = '''class Sample(unittest.TestCase):
    @unittest.skip('dependência ausente')
    def test_optional(self): pass
'''
        normal = self.run_suite(body)
        strict = self.run_suite(body, '--strict')
        self.assertEqual(normal.returncode, 0, normal.stderr)
        self.assertEqual(strict.returncode, 1, strict.stderr)
        self.assertIn('0/1 passaram; 1 não executado(s)', normal.stdout)
        self.assertIn('dependência ausente', normal.stdout)
        self.assertIn('Modo estrito', strict.stdout)

    def test_subtest_failure_counts_parent_once(self):
        result = self.run_suite('''class Sample(unittest.TestCase):
    def test_bad(self):
        for i in range(2):
            with self.subTest(i=i): self.fail('falha simulada')
''')
        self.assertEqual(result.returncode, 1)
        self.assertIn('[FALHOU] Sample: 0/1 passaram', result.stdout)
        self.assertIn('falha simulada', result.stdout)

    def test_import_error_is_reported_as_failure(self):
        result = self.run_suite("raise RuntimeError('erro ao carregar')\n")
        self.assertEqual(result.returncode, 1)
        self.assertIn('erro ao carregar', result.stdout)

    def test_unexpected_success_is_failure(self):
        result = self.run_suite('''class Sample(unittest.TestCase):
    @unittest.expectedFailure
    def test_unexpected(self): pass
''')
        self.assertEqual(result.returncode, 1)
        self.assertIn('Resultado inesperado', result.stdout)
