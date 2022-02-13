# -*- coding: UTF-8 -*-
from abc import ABCMeta, abstractmethod


class Estado_de_um_orcamento(object):
    __meta__ = ABCMeta

    def __init__(self):
        self.desconto_aplicado = False

    @abstractmethod
    def aplica_desconto_extra(self, orcamento):
        pass

    @abstractmethod
    def aprova(self, orcamento):
        pass

    @abstractmethod
    def reprova(self, orcamento):
        pass

    @abstractmethod
    def finaliza(self, orcamento):
        pass


class EM_APROVACAO(Estado_de_um_orcamento):

    def aplica_desconto_extra(self, orcamento):
        if not self.desconto_aplicado:
            orcamento.adiciona_desconto_extra(orcamento.valor * 0.02)
            self.desconto_aplicado = True
        else:
            raise Exception('Desconto já aplicado')

    def aprova(self, orcamento):
        orcamento.estado_atual = APROVADO()

    def reprova(self, orcamento):
        orcamento.estado_atual = REPROVADO()

    def finaliza(self, orcamento):
        raise Exception('Orçamento em aprovação não pode ser finalizado')


class APROVADO(Estado_de_um_orcamento):
    def aplica_desconto_extra(self, orcamento):
        if not self.desconto_aplicado:
            orcamento.adiciona_desconto_extra(orcamento.valor * 0.05)
            self.desconto_aplicado = True
        else:
            raise Exception('Desconto já aplicado')

    def aprova(self, orcamento):
        raise Exception('Orçamento aprovado não pode ser aprovado novamente')

    def reprova(self, orcamento):
        raise Exception('Orçamento em aprovado não pode ser reprovado')

    def finaliza(self, orcamento):
        orcamento.estado_atual = FINALIZADO()

class REPROVADO(Estado_de_um_orcamento):
    def aplica_desconto_extra(self, orcamento):
        raise Exception('Orçamentos reprovados não recebem desconto extra')

    def aprova(self, orcamento):
        raise Exception('Orçamento aprovado não pode ser reprovado')

    def reprova(self, orcamento):
        raise Exception('Orçamento reprovado não pode ser reprovado')

    def finaliza(self, orcamento):
        orcamento.estado_atual = FINALIZADO()

class FINALIZADO(Estado_de_um_orcamento):

    def aplica_desconto_extra(self, orcamento):
        raise Exception('Orçamentos finalizados não receberam desconto extra')

    def aprova(self, orcamento):
        raise Exception('Orçamento finalizado não pode ser aprovado')

    def reprova(self, orcamento):
        raise Exception('Orçamento finalizado não pode ser reprovado')

    def finaliza(self, orcamento):
        raise Exception('Orçamento finalizado não pode ser finalizado novamente')

class Orcamento(object):

    def __init__(self):
        self.__itens = []
        self.estado_atual = EM_APROVACAO()
        self.__desconto_extra = 0

    def aprova(self):
        self.estado_atual.aprova(orcamento)

    def reprova(self):
        self.estado_atual.reprova(orcamento)

    def finaliza(self):
        self.estado_atual.finaliza(orcamento)

    def aplica_desconto_extra(self):
        self.estado_atual.aplica_desconto_extra(self)

    def adiciona_desconto_extra(self, desconto):
        self.__desconto_extra += desconto

    @property
    def valor(self):
        total = 0.0
        for item in self.__itens:
            total += item.valor
        return total - self.__desconto_extra

    @property
    def total_itens(self):
        return len(self.__itens)

    def obter_items(self):
        return tuple(self.__itens)

    def adiciona_item(self, item):
        return self.__itens.append(item)


class Item(object):
    def __init__(self, nome, valor):
        self.__nome = nome
        self.__valor = valor

    @property
    def valor(self):
        return self.__valor

    @property
    def nome(self):
        return self.__nome


if __name__ == '__main__':
    orcamento = Orcamento()

    orcamento.adiciona_item(Item('ITEM 1', 100))
    orcamento.adiciona_item(Item('ITEM 2', 50))
    orcamento.adiciona_item(Item('ITEM 3', 400))

    print(orcamento.valor)
    orcamento.aprova()
    orcamento.aplica_desconto_extra()
    orcamento.finaliza()

    print(orcamento.valor)
