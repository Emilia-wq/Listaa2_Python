"""
@author Emilia Romanowska

Źródła:
- Dokumentacja Python: https://docs.python.org/3/reference/index.html
- Wsparcie koncepcyjne i techniczne: ChatGPT
"""


# Zadanie 1

class Wielomian:
    """
    Klasa reprezentująca wielomian dowolnego stopnia.
    Współczynniki przechowywane są w liście, gdzie indeks odpowiada potędze x.
    """

    def __init__(self, wspolczynniki):
        """
        Konstruktor wielomianu.

        Args:
            wspolczynniki: lista współczynników
        """
        if not isinstance(wspolczynniki, (list)):
            raise Exception("Współczynniki muszą być podane jako lista")

        if not wspolczynniki:
            raise Exception("Lista współczynników nie może być pusta")

        # Sprawdzenie czy wszystkie współczynniki są liczbami
        for i, wsp in enumerate(wspolczynniki):
            if not isinstance(wsp, (int, float)):
                raise Exception(f"Współczynnik na pozycji {i} musi być liczbą")

        # Kopiujemy współczynniki żeby uniknąć modyfikacji z zewnątrz
        self._wspolczynniki = list(wspolczynniki)

        # Usuwamy zera (oprócz przypadku gdy wielomian to samo zero)
        self._usun_wiodace_zera()

    def _usun_wiodace_zera(self):
        """Usuwa wiodące zera z wielomianu."""
        while len(self._wspolczynniki) > 1 and self._wspolczynniki[-1] == 0:
            self._wspolczynniki.pop()

    def stopien(self):
        """
        Zwraca stopień wielomianu.

        Returns:
            int: stopień wielomianu
        """
        return len(self._wspolczynniki) - 1

    def __str__(self):
        """
        Zwraca tekstową reprezentację wielomianu.

        Returns:
            str: reprezentacja w postaci W(x) = anx^n + ... + a1x + a0
        """
        if not self._wspolczynniki:
            return "W(x) = 0"

        # Przypadek wielomianu zerowego
        if len(self._wspolczynniki) == 1 and self._wspolczynniki[0] == 0:
            return "W(x) = 0"

        terminy = []

        # od najwyższego stopnia do najniższego
        for i in range(len(self._wspolczynniki) - 1, -1, -1):
            wsp = self._wspolczynniki[i]

            if wsp == 0:
                continue

            # Formatowanie współczynnika
            if i == 0:  # wyraz wolny
                if not terminy:  # pierwszy element
                    terminy.append(str(wsp))
                else:
                    if wsp > 0:
                        terminy.append(f" + {wsp}")
                    else:
                        terminy.append(f" - {abs(wsp)}")
            elif i == 1:  # x^1
                if wsp == 1:
                    if not terminy:
                        terminy.append("x")
                    else:
                        terminy.append(" + x")
                elif wsp == -1:
                    if not terminy:
                        terminy.append("-x")
                    else:
                        terminy.append(" - x")
                else:
                    if not terminy:
                        terminy.append(f"{wsp}x")
                    else:
                        if wsp > 0:
                            terminy.append(f" + {wsp}x")
                        else:
                            terminy.append(f" - {abs(wsp)}x")
            else:  # x^n gdzie n > 1
                if wsp == 1:
                    if not terminy:
                        terminy.append(f"x^{i}")
                    else:
                        terminy.append(f" + x^{i}")
                elif wsp == -1:
                    if not terminy:
                        terminy.append(f"-x^{i}")
                    else:
                        terminy.append(f" - x^{i}")
                else:
                    if not terminy:
                        terminy.append(f"{wsp}x^{i}")
                    else:
                        if wsp > 0:
                            terminy.append(f" + {wsp}x^{i}")
                        else:
                            terminy.append(f" - {abs(wsp)}x^{i}")

        return "W(x) = " + "".join(terminy)

    def __call__(self, x):
        """
        Oblicza wartość wielomianu dla danego x.

        Args:
            x: wartość zmiennej x

        Returns:
            wartość wielomianu W(x)
        """
        if not isinstance(x, (int, float)):
            raise Exception("Argument x musi być liczbą")

        wynik = 0
        for i, wsp in enumerate(self._wspolczynniki):
            wynik += wsp * (x ** i)

        return wynik

    def __add__(self, other):
        """Dodawanie wielomianów."""
        if not isinstance(other, Wielomian):
            raise Exception("Można dodawać tylko wielomiany")

        # Określamy długość wyniku
        max_len = max(len(self._wspolczynniki), len(other._wspolczynniki))
        wynik = []

        for i in range(max_len):
            a = self._wspolczynniki[i] if i < len(self._wspolczynniki) else 0
            b = other._wspolczynniki[i] if i < len(other._wspolczynniki) else 0
            wynik.append(a + b)

        return Wielomian(wynik)

    def __sub__(self, other):
        """Odejmowanie wielomianów."""
        if not isinstance(other, Wielomian):
            raise Exception("Można odejmować tylko wielomiany")

        # Określamy długość wyniku
        max_len = max(len(self._wspolczynniki), len(other._wspolczynniki))
        wynik = []

        for i in range(max_len):
            a = self._wspolczynniki[i] if i < len(self._wspolczynniki) else 0
            b = other._wspolczynniki[i] if i < len(other._wspolczynniki) else 0
            wynik.append(a - b)

        return Wielomian(wynik)

    def __mul__(self, other):
        """Mnożenie wielomianów."""
        if not isinstance(other, Wielomian):
            raise Exception("Można mnożyć tylko wielomiany")

        # Stopień wyniku to suma stopni
        wynik_len = len(self._wspolczynniki) + len(other._wspolczynniki) - 1
        wynik = [0] * wynik_len

        # Mnożenie każdego składnika pierwszego wielomianu przez każdy składnik drugiego
        for i in range(len(self._wspolczynniki)):
            for j in range(len(other._wspolczynniki)):
                wynik[i + j] += self._wspolczynniki[i] * other._wspolczynniki[j]

        return Wielomian(wynik)

    def __iadd__(self, other):
        """Operator +="""
        if not isinstance(other, Wielomian):
            raise Exception("Można dodawać tylko wielomiany")

        # Rozszerzamy listę współczynników
        while len(self._wspolczynniki) < len(other._wspolczynniki):
            self._wspolczynniki.append(0)

        # Dodajemy współczynniki
        for i in range(len(other._wspolczynniki)):
            self._wspolczynniki[i] += other._wspolczynniki[i]

        self._usun_wiodace_zera()
        return self

    def __isub__(self, other):
        """Operator -="""
        if not isinstance(other, Wielomian):
            raise Exception("Można odejmować tylko wielomiany")

        while len(self._wspolczynniki) < len(other._wspolczynniki):
            self._wspolczynniki.append(0)

        # Odejmujemy współczynniki
        for i in range(len(other._wspolczynniki)):
            self._wspolczynniki[i] -= other._wspolczynniki[i]

        self._usun_wiodace_zera()
        return self

    def __imul__(self, other):
        """Operator *="""
        if not isinstance(other, Wielomian):
            raise Exception("Można mnożyć tylko wielomiany")

        wynik = self * other
        self._wspolczynniki = wynik._wspolczynniki
        return self

    def __eq__(self, other):
        """Operator równości."""
        if not isinstance(other, Wielomian):
            return False
        return self._wspolczynniki == other._wspolczynniki

    def __ne__(self, other):
        """Operator nierówności."""
        return not self.__eq__(other)

    def get_wspolczynniki(self):
        """Zwraca kopię listy współczynników."""
        return self._wspolczynniki.copy()

if __name__ == "__main__":
    try:

        w1 = Wielomian([1, 2, 3])        # 1 + 2x + 3x^2
        w2 = Wielomian([4, -1, 0, 2])    # 4 - x + 2x^3

        print(f"w1 = {w1}")
        print(f"w2 = {w2}")
        print(f"Stopień w1: {w1.stopien()}")
        print(f"Stopień w2: {w2.stopien()}")

        x = 2
        print(f"w1({x}) = {w1(x)}")
        print(f"w2({x}) = {w2(x)}")

        print("\nDodawanie:")
        print(f"w1 + w2 = {w1 + w2}")

        print("\nOdejmowanie:")
        print(f"w1 - w2 = {w1 - w2}")

        print("\nMnożenie:")
        print(f"w1 * w2 = {w1 * w2}")

        print("\nOperatory złożone:")
        w_copy = Wielomian([1, 2, 3])
        w_copy += w2
        print(f"(w1 += w2): {w_copy}")

        w_copy = Wielomian([1, 2, 3])
        w_copy -= Wielomian([1, 1, 1])
        print(f"(w1 -= [1,1,1]): {w_copy}")

        w_copy = Wielomian([1, 1])
        w_copy *= Wielomian([1, 1])
        print(f"(w1 *= [1,1]): {w_copy}")

    except Exception as e:
        print("Błąd:", e)
