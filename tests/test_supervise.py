import importlib.util
from pathlib import Path
import unittest
from unittest.mock import Mock, patch

spec = importlib.util.spec_from_file_location('supervise', Path(__file__).resolve().parents[1] / 'hypr/scripts/supervise.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class SupervisorTests(unittest.TestCase):
    def test_restarts_after_failure_while_session_alive(self):
        with patch.object(module.subprocess, 'run', return_value=Mock(returncode=1)) as run:
            with patch.object(module.time, 'sleep') as sleep:
                module.supervise(['waybar'], Mock(side_effect=[True, True, True, False, False]))
        self.assertEqual(run.call_count, 2)
        sleep.assert_called_once_with(3)

    def test_does_not_start_without_session(self):
        with patch.object(module.subprocess, 'run') as run:
            module.supervise(['swaybg'], lambda: False)
        run.assert_not_called()
