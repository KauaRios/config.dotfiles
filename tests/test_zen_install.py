"""Testa a aprovação do AUR com comandos simulados; não acessa rede nem instala pacotes."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/install-zen-arch.sh'


@unittest.skipIf(os.geteuid() == 0, 'Fluxo de instalação exige usuário não root')
class ZenInstallTests(unittest.TestCase):
    def run_installer(self, answer, installed=False):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            commands = root / 'bin'; commands.mkdir()
            calls = root / 'calls'
            # A receita contém um efeito colateral que não deve acontecer antes da aprovação.
            scripts = {
                'pacman': '#!/bin/sh\nexit ' + ('0' if installed else '1') + '\n',
                'git': '''#!/bin/bash
case "$1" in
clone)
  mkdir -p "${@: -1}"
  printf 'touch "%s"\n' "$UNTRUSTED_MARKER" > "${@: -1}/PKGBUILD"
  printf 'install hook\n' > "${@: -1}/zen.install"
  ;;
rev-parse) echo abc123 ;;
ls-files) printf 'PKGBUILD\\0zen.install\\0' ;;
*) exit 2 ;;
esac
''',
                'makepkg': '#!/bin/sh\nprintf "%s\\n" "$*" > "$CALLS"\necho MAKEPKG_EXECUTADO\n',
            }
            for name, text in scripts.items():
                file = commands / name; file.write_text(text); file.chmod(0o755)
            marker = root / 'untrusted'
            result = subprocess.run(['bash', str(SCRIPT)], input=answer, text=True,
                                    capture_output=True, timeout=5,
                                    env={**os.environ, 'PATH': str(commands) + ':' + os.environ['PATH'],
                                         'CALLS': str(calls), 'UNTRUSTED_MARKER': str(marker),
                                         'TMPDIR': str(root)})
            self.assertFalse(marker.exists(), 'Receita foi executada durante a revisão')
            self.assertEqual(list(root.glob('dotfiles-zen.*')), [], 'Pasta temporária não removida')
            return result, calls.read_text() if calls.exists() else None

    def test_rejection_never_builds(self):
        """Enter ou respostas diferentes de CONFIO encerram sem makepkg."""
        for answer in ('\n', 'sim\n', 'confio\n'):
            with self.subTest(answer=answer):
                result, calls = self.run_installer(answer)
                self.assertNotEqual(result.returncode, 0)
                self.assertIsNone(calls)

    def test_eof_never_builds(self):
        """Ausência de entrada não conta como consentimento."""
        result, calls = self.run_installer('')
        self.assertNotEqual(result.returncode, 0)
        self.assertIsNone(calls)

    def test_approval_builds_after_showing_recipe_and_hooks(self):
        """A confirmação explícita libera makepkg após mostrar receita e hook."""
        result, calls = self.run_installer('CONFIO\n')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(calls.strip(), '--syncdeps --install --needed')
        self.assertLess(result.stdout.index('install hook'), result.stdout.index('MAKEPKG_EXECUTADO'))
        self.assertIn('abc123', result.stdout)

    def test_installed_package_skips_aur(self):
        """Pacote já instalado não é recompilado nem solicita aprovação."""
        result, calls = self.run_installer('', installed=True)
        self.assertEqual(result.returncode, 0)
        self.assertIsNone(calls)
        self.assertNotIn('Digite CONFIO', result.stdout)
