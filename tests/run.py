#!/usr/bin/env python3
"""Executa a suíte de qualquer pasta, com resumo em português."""
from pathlib import Path
import sys
import unittest

sys.dont_write_bytecode = True
GROUPS = {
    'ConfigTests': 'Configurações e sintaxe',
    'InstallTests': 'Links, backups e preservação do KDE',
    'ScreenshotTests': 'Captura de tela e área de transferência',
    'HyprlandSessionTests': 'Sessão Hyprland',
}


class Result(unittest.TestResult):
    def __init__(self):
        super().__init__()
        self.groups = {}

    def startTest(self, test):
        super().startTest(test)
        key = type(test).__name__
        self.groups.setdefault(key, []).append(test)


def main():
    suite = unittest.defaultTestLoader.discover(str(Path(__file__).resolve().parent))
    result = Result()
    suite.run(result)
    failed = {test.id() for test, _ in result.failures + result.errors}
    failed.update(test.id() for test in result.unexpectedSuccesses)
    skipped = {test.id() for test, _ in result.skipped}
    expected = {test.id() for test, _ in result.expectedFailures}
    print('\nVerificação das dotfiles\n')
    for key, tests in result.groups.items():
        ids = [test.id() for test in tests]
        # Uma falha em subteste também faz o teste pai falhar.
        bad = sum(any(f == name or f.startswith(name + ' ') for f in failed) for name in ids)
        omitted = sum(name in skipped for name in ids)
        known = sum(name in expected for name in ids)
        passed = len(ids) - bad - omitted - known
        status = 'FALHOU' if bad else ('ATENÇÃO' if omitted or known else 'OK')
        detail = f'{passed}/{len(ids)} passaram'
        if omitted:
            detail += f'; {omitted} não executado(s)'
        if known:
            detail += f'; {known} falha(s) esperada(s)'
        print(f'[{status}] {GROUPS.get(key, key)}: {detail}')
    for test, reason in result.skipped:
        label = 'Sintaxe Lua' if test._testMethodName == 'test_lua_syntax' else test.id()
        print(f'\nNão verificado — {label}: {reason}')
    for test, traceback in result.failures + result.errors:
        print(f'\nDetalhes da falha: {test.id()}\n{traceback}')
    for test in result.unexpectedSuccesses:
        print(f'\nResultado inesperado: {test.id()} passou, embora estivesse marcado como falha esperada.')
    if result.wasSuccessful():
        print('\nNenhuma falha nos testes executados.')
    else:
        print('\nHá falhas que precisam ser corrigidas.')
    print('Aparência e interação gráfica não são testadas aqui.\n')
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(main())
