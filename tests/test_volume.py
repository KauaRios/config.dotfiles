"""Controle de volume com wpctl e notificações simulados."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class VolumeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='volume test ')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.log = self.base / 'calls.jsonl'
        for name in ('wpctl', 'notify-send'):
            script = self.base / name
            script.write_text('''#!/usr/bin/env python3
import json, os, sys
from pathlib import Path
with open(os.environ['TEST_LOG'], 'a') as log:
    log.write(json.dumps([Path(sys.argv[0]).name, *sys.argv[1:]]) + '\\n')
if Path(sys.argv[0]).name == 'wpctl':
    if os.environ.get('TEST_FAIL') == sys.argv[1]:
        sys.exit(1)
    if sys.argv[1] == 'get-volume':
        print(os.environ.get('TEST_VOLUME', 'Volume: 0.42'))
''')
            script.chmod(0o755)

    def run_volume(self, *args, **overrides):
        env = dict(os.environ, PATH=str(self.base) + ':' + os.environ['PATH'],
                   TEST_LOG=str(self.log), TEST_FAIL='', TEST_VOLUME='Volume: 0.42')
        env.update(overrides)
        result = subprocess.run(['bash', str(ROOT / 'hypr/scripts/volume.sh'), *args],
                                env=env, capture_output=True, text=True, timeout=10)
        calls = [json.loads(line) for line in self.log.read_text().splitlines()] if self.log.exists() else []
        return result, calls

    def test_actions_and_percentage_notification(self):
        for action, expected in (
            ('up', ['set-volume', '-l', '1.0', '@DEFAULT_AUDIO_SINK@', '5%+']),
            ('down', ['set-volume', '@DEFAULT_AUDIO_SINK@', '5%-']),
            ('toggle', ['set-mute', '@DEFAULT_AUDIO_SINK@', 'toggle']),
        ):
            with self.subTest(action=action):
                self.log.write_text('')
                result, calls = self.run_volume(action)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(calls[0], ['wpctl', *expected])
                self.assertEqual(calls[1], ['wpctl', 'get-volume', '@DEFAULT_AUDIO_SINK@'])
                self.assertEqual(calls[2][0], 'notify-send')
                self.assertIn('int:value:42', calls[2])
                self.assertIn('42%', calls[2][-1])

    def test_muted_notification_has_no_percentage_bar(self):
        result, calls = self.run_volume('toggle', TEST_VOLUME='Volume: 0.42 [MUTED]')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Mutado', calls[-1][-1])
        self.assertFalse(any(arg.startswith('int:value:') for arg in calls[-1]))

    def test_invalid_arguments_have_no_side_effects(self):
        for args in ((), ('invalid',), ('up', 'extra')):
            with self.subTest(args=args):
                result, calls = self.run_volume(*args)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(calls, [])

    def test_audio_failure_does_not_send_success_notification(self):
        for operation in ('set-volume', 'get-volume'):
            with self.subTest(operation=operation):
                self.log.write_text('')
                result, calls = self.run_volume('up', TEST_FAIL=operation)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(any(call[0] == 'notify-send' for call in calls))
