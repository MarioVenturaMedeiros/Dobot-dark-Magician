from serial.tools import list_ports
import typer
import inquirer
import pydobot
from yaspin import yaspin

app = typer.Typer()
spinner = yaspin(text="Processando...", color="yellow")

# O basico da classe InteliArm foi fornecido pelo professor Murilo. Nessa classe básica foi importada o moveJ, o moveL e a lógica de pegar a posição. O resto foi desenvolvido pelo aluno.


class InteliArm(pydobot.Dobot):
    sugando = False

    def __init__(self, port=None, verbose=False):
        self.verbose = verbose
        porta_escolhida = port if port is not None else self.conectar_porta()
        super().__init__(port=porta_escolhida, verbose=self.verbose)

    def conectar_porta(self):
        portas_disponiveis = list_ports.comports()
        if not portas_disponiveis:
            print("Drake, cade a porta???")
            return None
        porta_escolhida = inquirer.prompt([
            inquirer.List("porta", message="Escolha a porta serial",
                          choices=[x.device for x in portas_disponiveis])
        ])["porta"]
        print('Porta escolhida:', porta_escolhida)
        return porta_escolhida

    def movej_to(self, x, y, z, r, wait=True):
        spinner.start()
        super()._set_ptp_cmd(x, y, z, r, mode=pydobot.enums.PTPMode.MOVJ_XYZ, wait=wait)
        spinner.stop()

    def movel_to(self, x, y, z, r, wait=True):
        spinner.start()
        super()._set_ptp_cmd(x, y, z, r, mode=pydobot.enums.PTPMode.MOVL_XYZ, wait=wait)
        spinner.stop()

    def posicao_atual(self):
        posicao_atual = self.pose()
        print(f"posição atual: {posicao_atual}")

    def home(self, wait=True):
        print("COUNTRY ROAD, TAKE ME HOME, TO THE PLACE, I BELOOOOOOONG")
        spinner.start()
        super()._set_ptp_cmd(240, 0, 150, 0,
                             mode=pydobot.enums.PTPMode.MOVJ_XYZ, wait=wait)
        spinner.stop()

    def sugada_dimensional(self):
        InteliArm.sugando = not InteliArm.sugando
        self.suck(self.sugando)

    def loop(self, acao: str):
        continuar = True
        while continuar:
            match(acao):
                case "mover modo J":
                    mover_rapidao()
                    acao = "escolha"
                case "mover modo L":
                    mover_lentinho()
                    acao = "escolha"
                case  "mostrar posição atual":
                    self.posicao_atual()
                    acao = "escolha"
                case "toggle ativador":
                    self.sugada_dimensional()
                    acao = "escolha"
                case "home":
                    self.home()
                    acao = "escolha"
                case "escolha":
                    acao = faca_algo()


def mover_rapidao(wait: bool = True):
    try:
        x = float(input("Digite o valor de X: ") or 0)
    except ValueError:
        x = 0.0
    try:
        y = float(input("Digite o valor de Y: ") or 0)
    except ValueError:
        y = 0.0
    try:
        z = float(input("Digite o valor de Z: ") or 0)
    except ValueError:
        z = 0.0
    try:
        r = float(input("Digite o valor de r: ") or 0)
    except ValueError:
        r = 0.0

    Robo.movej_to(x, y, z, r, wait)


def mover_lentinho(wait: bool = True):
    try:
        x = float(input("Digite o valor de X: ") or 0)
    except ValueError:
        x = 0.0
    try:
        y = float(input("Digite o valor de Y: ") or 0)
    except ValueError:
        y = 0.0
    try:
        z = float(input("Digite o valor de Z: ") or 0)
    except ValueError:
        z = 0.0
    try:
        r = float(input("Digite o valor de r: ") or 0)
    except ValueError:
        r = 0.0

    Robo.movel_to(x, y, z, r, wait)


def faca_algo():
    acao_lista = inquirer.prompt([
        inquirer.List("acao", message="Escolha o que fazer com o robô: ",
                      choices=["mover modo J", "mover modo L", "mostrar posição atual", "toggle ativador", "home"])
    ])["acao"]
    return acao_lista


Robo = InteliArm()

if __name__ == "__main__":
    acao_escolhida = faca_algo()
    Robo.loop(acao_escolhida)
