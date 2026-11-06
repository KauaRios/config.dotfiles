#!/usr/bin/env python3
"""Executa a suíte de qualquer pasta, com resumo em português."""
from pathlib import Path
import argparse
import sys
import time
import unittest

sys.dont_write_bytecode = True
GROUPS = {
    'CheatsheetTests': 'Ajuda e atalhos',
    'VolumeTests': 'Volume e notificações',
    'RunnerTests': 'Relatório e código de saída da suíte',
    'ConfigTests': 'Configurações e sintaxe',
    'InstallTests': 'Links, backups e preservação do KDE',
    'ScreenshotTests': 'Captura de tela e área de transferência',
    'HyprlandSessionTests': 'Sessão Hyprland',
    'HyprlandApiTests': 'API real do Hyprland (configuração isolada)',
}


class Result(unittest.TestResult):
    def __init__(self):
        super().__init__()
        self.groups = {}

    def startTest(self, test):
        super().startTest(test)
        key = type(test).__name__
        self.groups.setdefault(key, []).append(test)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--strict', action='store_true',
                        help='retorna erro também se houver testes ignorados ou falhas esperadas')
    args = parser.parse_args(argv)
    started = time.monotonic()
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
        label = 'Sintaxe Lua' if getattr(test, '_testMethodName', '') == 'test_lua_syntax' else test.id()
        print(f'\nNão verificado — {label}: {reason}')
    for test, traceback in result.failures + result.errors:
        print(f'\nDetalhes da falha: {test.id()}\n{traceback}')
    for test in result.unexpectedSuccesses:
        print(f'\nResultado inesperado: {test.id()} passou, embora estivesse marcado como falha esperada.')
    successful = result.wasSuccessful() and not (
        args.strict and (result.skipped or result.expectedFailures))
    if result.wasSuccessful():
        print('\nNenhuma falha nos testes executados.')
    else:
        print('\nHá falhas que precisam ser corrigidas.')
    if args.strict and (result.skipped or result.expectedFailures):
        print('Modo estrito: validação incompleta impede aprovação.')
    print(f'{result.testsRun} testes em {time.monotonic() - started:.2f}s.')
    print('Aparência e interação gráfica não são testadas aqui.\n')
    return 0 if successful else 1


if __name__ == '__main__':
    sys.exit(main())
