#!/usr/bin/env python3
"""Menu explícito: clicar no ícone de energia não desliga o computador."""
import subprocess

ACTIONS = {'Bloquear': ['hyprlock'], 'Suspender': ['systemctl', 'suspend'],
           'Reiniciar': ['systemctl', 'reboot'], 'Desligar': ['systemctl', 'poweroff']}


def main():
    result = subprocess.run(['rofi', '-dmenu', '-i', '-no-custom', '-p', 'Sessão'],
                            input='\n'.join(ACTIONS), text=True, capture_output=True)
    if result.returncode != 0:
        return
    command = ACTIONS.get(result.stdout.strip())
    if command:
        subprocess.run(command, check=True)


if __name__ == '__main__':
    main()
