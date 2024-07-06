""" Module for functions helpers for grimorios """
import random
import re

descripciones = {
    1: """
        Grimorio de Trébol de 1 Hoja: Este grimorio es común en el mundo mágico. 
        Sus páginas contienen hechizos básicos y conocimientos rudimentarios. 
        Aunque fácil de encontrar, sigue siendo una valiosa fuente de aprendizaje 
        para los principiantes.
        """,
    2: """
        Grimorio de Trébol de 2 Hojas: Este grimorio es menos común y contiene 
        hechizos y secretos de nivel intermedio. 
        Los magos lo buscan por su capacidad de profundizar en la magia elemental 
        y las pociones avanzadas.
        """,
    3: """
        Grimorio de Trébol de 3 Hojas: Raro y codiciado, este grimorio contiene 
        conjuros poderosos y conocimientos arcanos. Solo los magos experimentados 
        pueden comprender sus complejidades, haciendo de su posesión un símbolo de 
        prestigio.""",
    4: """
          Grimorio de Trébol de 4 Hojas: El más raro de todos, este grimorio es una 
          leyenda en sí mismo. Conocido por contener los hechizos más poderosos y 
          los secretos más antiguos, solo los magos más sabios y valientes se atreven 
          a buscarlo.
        """
}

tipos = {
    1: "Trebol_Una_Hoja",
    2: "Trebol_Dos_Hojas",
    3: "Trebol_Tres_Hojas",
    4: "Trebol_Cuatro_Hojas"
}


class Grimorio:
    def __init__(self, hojas: int):
        self.hojas = hojas

    def __str__(self):
        return f"Grimorio portada con trébol de {self.hojas} hojas"

    @property
    def grimorio_tipo(self):
        name = self.__class__.__name__.replace("Grimorio", "")
        return re.sub(r"(?<!^)(?=[A-Z])", "_", name)

    @property
    def numero_hojas(self):
        return self.hojas

    @property
    def descripcion(self):
        return descripciones[self.hojas]


class GrimorioTrebolUnaHoja(Grimorio):
    def __init__(self):
        super().__init__(1)


class GrimorioTrebolDosHojas(Grimorio):
    def __init__(self):
        super().__init__(2)


class GrimorioTrebolTresHojas(Grimorio):
    def __init__(self):
        super().__init__(3)


class GrimorioTrebolCuatroHojas(Grimorio):
    def __init__(self):
        super().__init__(4)


class GrimorioFactory:
    """
    Factory class to create grimorios
    """

    @staticmethod
    def asignar_grimorio():
        """
        Asigna un grimorio aleatorio basado en las probabilidades
        """
        probabilidades = {
            GrimorioTrebolUnaHoja: 0.4,  # 40% de probabilidad
            GrimorioTrebolDosHojas: 0.3,  # 30% de probabilidad
            GrimorioTrebolTresHojas: 0.2,  # 20% de probabilidad
            GrimorioTrebolCuatroHojas: 0.1,  # 10% de probabilidad
        }

        clases_grimorio = list(probabilidades.keys())
        weights = list(probabilidades.values())

        # Seleccionar una clase de grimorio basado en las probabilidades
        grimorio_class = random.choices(clases_grimorio, weights, k=1)[0]

        return grimorio_class()
