from random import randint, getrandbits

caracteristicas = ("impulsivo", "exigente", "cauteloso", "aleatorio")


class Banco_imobiliario():

    def __init__(self, num_jogadores=4):

        self.propriedades = {x: {"valor": randint(0, 200),"dono": None} for x in range(1, 21)}

        i = 0
        self.jogadores = {}
        for jogador in range(1, num_jogadores + 1):
            self.jogadores.update({
                jogador: {
                    "caracteristica": caracteristicas[i],
                    "saldo": 300,
                    "casa_atual": 0
                    }
                })
            
            i = 0 if i > len(caracteristicas) else i + 1
    
    def rodar_dado(self):
        return randint(1,6)
    
    def verificar_vencedor(self):
        for jogador in range(1, 5):
            if self.jogadores[jogador]["saldo"] > 0:
                return jogador

    def verifica_rodada(self, jogador):
        if self.jogadores[jogador]["casa_atual"] > 20:
            self.jogadores[jogador]["casa_atual"] -= 20
            self.jogadores[jogador]["saldo"] += 100

    def pagar_pela_casa(self, jogador):
        self.propriedades[self.jogadores[jogador]["casa_atual"]]["dono"] = jogador
        self.jogadores[jogador]["saldo"] -= self.propriedades[self.jogadores[jogador]["casa_atual"]]["valor"]

    def comprar_casa(self, jogador):
        if self.jogadores[jogador]["caracteristica"] == "impulsivo":

            if self.jogadores[jogador]["saldo"] >= self.propriedades[self.jogadores[jogador]["casa_atual"]]["valor"]:
                self.pagar_pela_casa(jogador)
            
        elif self.jogadores[jogador]["caracteristica"] == "exigente":

            if (
                self.propriedades[self.jogadores[jogador]["casa_atual"]]["valor"] > 50 
                and self.jogadores[jogador]["saldo"] >= self.propriedades[self.jogadores[jogador]["casa_atual"]]["valor"]
            ):

                self.pagar_pela_casa(jogador)

        elif self.jogadores[jogador]["caracteristica"] == "cauteloso":

            saldo_restante = self.jogadores[jogador]["saldo"] - self.propriedades[self.jogadores[jogador]["casa_atual"]]["valor"]
            if saldo_restante >= 80:
                self.pagar_pela_casa(jogador)

        elif self.jogadores[jogador]["caracteristica"] == "aleatorio":    
            if bool(getrandbits(1)):
                self.pagar_pela_casa(jogador)

    def pagar_aluguel(self, jogador):
        self.jogadores[
            self.propriedades[
                self.jogadores[jogador]["casa_atual"]
            ]["dono"]
        ]["saldo"] += self.propriedades[self.jogadores[jogador]["casa_atual"]]["valor"]

        self.jogadores[jogador]["saldo"] -= self.propriedades[self.jogadores[jogador]["casa_atual"]]["valor"]

    def perdedor(self, jogador):
        self.jogadores[
            self.propriedades[
                self.jogadores[jogador]["casa_atual"]
            ]["dono"]
        ]["saldo"] += self.jogadores[jogador]["saldo"]

        self.jogadores[jogador]["saldo"] = 0

        for key, value in self.propriedades.items():
            if value["dono"] == jogador:
                self.propriedades[key]["dono"] = None

    def jogar(self):
        perdedores = 0
        for rodada in range(1, 1001):
            for jogador in range(1, 5):
                if self.jogadores[jogador]["saldo"] > 0:
                    dado = self.rodar_dado()
                    self.jogadores[jogador]["casa_atual"] += dado

                    self.verifica_rodada(jogador)

                    if self.propriedades[self.jogadores[jogador]["casa_atual"]]["dono"] == None:
                        self.comprar_casa(jogador)

                    else:
                        if self.jogadores[jogador]["saldo"] > self.propriedades[self.jogadores[jogador]["casa_atual"]]["valor"]:
                            self.pagar_aluguel(jogador)

                        else:
                            self.perdedor(jogador)
                            perdedores += 1
                else:
                    perdedores += 1

            if perdedores > 3:
                vencedor = self.verificar_vencedor()
                return rodada, vencedor
        print(self.jogadores)
        return rodada, None

if __name__ == "__main__":
    time_out = 0
    media_rodadas = 0
    vitorias = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
    }

    for simulacoes in range(1, 301):
        jogo = Banco_imobiliario()
        rodada, vencedor = jogo.jogar()
        
        if vencedor is None:
            time_out += 1
        else:
            media_rodadas += rodada
            vitorias.update({vencedor: vitorias[vencedor] + 1 })

    print(f"Quantas partidas terminam por timeout (1000 rodadas): {time_out}")
    print(f"Quantos turnos em média demora uma partida: {media_rodadas/300}")
    print(f"Qual a porcentagem de vitórias por comportamento dos jogadores:\n")
    print(f"impulsivo: {(vitorias[1]*100)/300}%")
    print(f"exigente: {(vitorias[2]*100)/300}%")
    print(f"cauteloso: {(vitorias[3]*100)/300}%")
    print(f"aleatório: {(vitorias[4]*100)/300}%\n")
    print(f"Qual o comportamento que mais vence: {caracteristicas[max(vitorias, key=vitorias.get)-1]}")