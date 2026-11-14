"""Mídia e menu de sessão da Sora, sem controlar serviços ou áudio reais."""
import importlib.util
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch

ASSETS = Path(__file__).resolve().parents[1] / 'hypr/scripts/waybar-templetes/sora/assets'

def load(name):
    spec = importlib.util.spec_from_file_location(name, ASSETS / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SoraControlsTests(unittest.TestCase):
    def test_media_fallback_and_markup(self):
        """Ausência/timeout mantém o bloco; caracteres do título não viram markup."""
        media = load('sora-media')
        with patch.object(media.subprocess, 'run', return_value=subprocess.CompletedProcess([], 1, '', '')):
            self.assertEqual(media.current_media()['class'], 'idle')
        with patch.object(media.subprocess, 'run', side_effect=subprocess.TimeoutExpired('playerctl', 2)):
            self.assertIn('Nothing playing', media.current_media()['text'])
        with patch.object(media.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, '<track & title>', '')):
            data = media.current_media()
            self.assertEqual(data['text'], '▪ &lt;track &amp; title&gt;')

    def test_session_cancel_and_unknown_do_nothing(self):
        """Escape e seleções desconhecidas nunca executam uma ação de sessão."""
        session = load('sora-session')
        for code, text in ((1, ''), (0, ''), (0, 'unknown')):
            with self.subTest(code=code, text=text):
                with patch.object(session.subprocess, 'run', return_value=subprocess.CompletedProcess([], code, text, '')) as run:
                    session.main()
                    self.assertEqual(run.call_count, 1)

    def test_session_executes_only_selected_action(self):
        """Cada opção chama seu comando exato; nenhuma ação real é executada."""
        session = load('sora-session')
        commands = {'Bloquear': ['hyprlock'], 'Suspender': ['systemctl', 'suspend'],
                    'Reiniciar': ['systemctl', 'reboot'], 'Desligar': ['systemctl', 'poweroff']}
        for label, command in commands.items():
            with self.subTest(action=label):
                with patch.object(session.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, label+'\n', '')) as run:
                    session.main()
                    self.assertEqual(run.call_count, 2)
                    self.assertEqual(run.call_args.args[0], command)
