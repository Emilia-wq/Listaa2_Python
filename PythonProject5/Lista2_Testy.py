import unittest

from PythonProject5.Lista2_zadanie1 import Wielomian
from PythonProject5.Lista2_zadanie2 import DNASequence, RNASequence, ProteinSequence


class TestWielomian(unittest.TestCase):
    """Testy jednostkowe dla klasy Wielomian."""

    def setUp(self):
        """Przygotowanie danych testowych."""
        self.w1 = Wielomian([1, 2, 3])  # 1 + 2x + 3x^2
        self.w2 = Wielomian([4, -1, 0, 2])  # 4 - x + 2x^3
        self.w_zero = Wielomian([0])  # wielomian zerowy
        self.w_const = Wielomian([5])  # wielomian stały

    def test_konstruktor_poprawny(self):
        """Test poprawnego tworzenia wielomianu."""
        w = Wielomian([1, 2, 3])
        self.assertEqual(w.get_wspolczynniki(), [1, 2, 3])

        # Test z tuplą
        w_tuple = Wielomian((1, 2, 3))
        self.assertEqual(w_tuple.get_wspolczynniki(), [1, 2, 3])

    def test_konstruktor_usuwanie_wiodacych_zer(self):
        """Test usuwania wiodących zer."""
        w = Wielomian([1, 2, 0, 0, 0])
        self.assertEqual(w.get_wspolczynniki(), [1, 2])

        # Test wielomianu z samymi zerami na końcu
        w_zero_end = Wielomian([1, 0, 0])
        self.assertEqual(w_zero_end.get_wspolczynniki(), [1])

    def test_konstruktor_bledy(self):
        """Test błędnych argumentów konstruktora."""
        # Pusta lista
        with self.assertRaises(ValueError):
            Wielomian([])

        # Nieprawidłowy typ argumentu
        with self.assertRaises(TypeError):
            Wielomian("123")

        # Nieprawidłowy typ współczynnika
        with self.assertRaises(TypeError):
            Wielomian([1, "abc", 3])

        # None jako współczynnik
        with self.assertRaises(TypeError):
            Wielomian([1, None, 3])

    def test_stopien(self):
        """Test metody stopien()."""
        self.assertEqual(self.w1.stopien(), 2)
        self.assertEqual(self.w2.stopien(), 3)
        self.assertEqual(self.w_zero.stopien(), 0)
        self.assertEqual(self.w_const.stopien(), 0)

        # Test po usunięciu wiodących zer
        w = Wielomian([1, 2, 0, 0])
        self.assertEqual(w.stopien(), 1)

    def test_str_representation(self):
        """Test reprezentacji tekstowej."""
        # Test podstawowy
        w_simple = Wielomian([1, 2, 3])
        str_repr = str(w_simple)
        self.assertIn("W(x) =", str_repr)
        self.assertIn("3x^2", str_repr)
        self.assertIn("2x", str_repr)
        self.assertIn("1", str_repr)

        # Test wielomianu zerowego
        self.assertEqual(str(self.w_zero), "W(x) = 0")

        # Test wielomianu stałego
        w_const = Wielomian([5])
        self.assertIn("W(x) = 5", str(w_const))

        # Test z ujemnymi współczynnikami
        w_neg = Wielomian([1, -2, 3])
        str_neg = str(w_neg)
        self.assertIn("- 2x", str_neg)

    def test_call_operator(self):
        """Test operatora wywołania."""
        w = Wielomian([1, 2, 3])  # 1 + 2x + 3x^2

        # Test dla różnych wartości x
        self.assertEqual(w(0), 1)  # 1 + 0 + 0 = 1
        self.assertEqual(w(1), 6)  # 1 + 2 + 3 = 6
        self.assertEqual(w(2), 17)  # 1 + 4 + 12 = 17

        # Test z liczbami ujemnymi
        self.assertEqual(w(-1), 2)  # 1 - 2 + 3 = 2

        # Test z liczbami zmiennoprzecinkowymi
        self.assertAlmostEqual(w(0.5), 2.75)  # 1 + 1 + 0.75 = 2.75

        # Test błędnego typu argumentu
        with self.assertRaises(TypeError):
            w("abc")

    def test_dodawanie(self):
        """Test operatora dodawania."""
        w1 = Wielomian([1, 2, 3])  # 1 + 2x + 3x^2
        w2 = Wielomian([4, -1, 0, 2])  # 4 - x + 2x^3

        wynik = w1 + w2
        oczekiwane = [5, 1, 3, 2]  # 5 + x + 3x^2 + 2x^3
        self.assertEqual(wynik.get_wspolczynniki(), oczekiwane)

        # Test dodawania wielomianów różnych stopni
        w3 = Wielomian([1])
        w4 = Wielomian([0, 1, 1])
        wynik2 = w3 + w4
        self.assertEqual(wynik2.get_wspolczynniki(), [1, 1, 1])

        # Test błędnego typu
        with self.assertRaises(TypeError):
            w1 + 5

    def test_odejmowanie(self):
        """Test operatora odejmowania."""
        w1 = Wielomian([1, 2, 3])
        w2 = Wielomian([1, 1, 1])

        wynik = w1 - w2
        oczekiwane = [0, 1, 2]
        self.assertEqual(wynik.get_wspolczynniki(), oczekiwane)

        # Test odejmowania od siebie
        wynik_zero = w1 - w1
        self.assertEqual(wynik_zero.get_wspolczynniki(), [0])

        # Test błędnego typu
        with self.assertRaises(TypeError):
            w1 - "abc"

    def test_mnozenie(self):
        """Test operatora mnożenia."""
        w1 = Wielomian([1, 1])  # 1 + x
        w2 = Wielomian([1, 1])  # 1 + x

        wynik = w1 * w2  # (1 + x)^2 = 1 + 2x + x^2
        oczekiwane = [1, 2, 1]
        self.assertEqual(wynik.get_wspolczynniki(), oczekiwane)

        # Test mnożenia przez wielomian zerowy
        w_zero = Wielomian([0])
        wynik_zero = w1 * w_zero
        self.assertEqual(wynik_zero.get_wspolczynniki(), [0])

        # Test mnożenia przez stałą
        w_const = Wielomian([2])
        wynik_const = w1 * w_const
        self.assertEqual(wynik_const.get_wspolczynniki(), [2, 2])

        # Test błędnego typu
        with self.assertRaises(TypeError):
            w1 * 3.14

    def test_operator_iadd(self):
        """Test operatora +=."""
        w1 = Wielomian([1, 2])
        w2 = Wielomian([3, 4])

        w1 += w2
        self.assertEqual(w1.get_wspolczynniki(), [4, 6])

        # Test z wielomianami różnych stopni
        w3 = Wielomian([1])
        w4 = Wielomian([0, 1, 1])
        w3 += w4
        self.assertEqual(w3.get_wspolczynniki(), [1, 1, 1])

        # Test błędnego typu
        with self.assertRaises(TypeError):
            w1 += 5

    def test_operator_isub(self):
        """Test operatora -=."""
        w1 = Wielomian([5, 6])
        w2 = Wielomian([1, 2])

        w1 -= w2
        self.assertEqual(w1.get_wspolczynniki(), [4, 4])

        # Test odejmowania większego wielomianu
        w3 = Wielomian([1])
        w4 = Wielomian([0, 1, 1])
        w3 -= w4
        self.assertEqual(w3.get_wspolczynniki(), [1, -1, -1])

        # Test błędnego typu
        with self.assertRaises(TypeError):
            w1 -= "test"

    def test_operator_imul(self):
        """Test operatora *=."""
        w1 = Wielomian([1, 1])  # 1 + x
        w2 = Wielomian([1, 1])  # 1 + x

        w1 *= w2  # (1 + x)^2
        self.assertEqual(w1.get_wspolczynniki(), [1, 2, 1])

        # Test błędnego typu
        with self.assertRaises(TypeError):
            w1 *= 2

    def test_equality(self):
        """Test operatorów równości."""
        w1 = Wielomian([1, 2, 3])
        w2 = Wielomian([1, 2, 3])
        w3 = Wielomian([1, 2, 4])

        # Test równości
        self.assertTrue(w1 == w2)
        self.assertFalse(w1 == w3)

        # Test nierówności
        self.assertFalse(w1 != w2)
        self.assertTrue(w1 != w3)

        # Test z innym typem
        self.assertFalse(w1 == "wielomian")
        self.assertTrue(w1 != 42)

    def test_liczby_zespolone(self):
        """Test z liczbami zespolonymi."""
        w = Wielomian([1 + 2j, 3 - 1j])
        self.assertEqual(w.get_wspolczynniki(), [1 + 2j, 3 - 1j])

        # Test obliczania wartości
        wynik = w(1j)  # (1+2j) + (3-1j)*1j = 1+2j + 3j+1 = 2+5j
        self.assertEqual(wynik, 2 + 5j)

    def test_edge_cases(self):
        """Test przypadków brzegowych."""
        # Wielomian z jednym współczynnikiem zerowym
        w_single_zero = Wielomian([0])
        self.assertEqual(w_single_zero.stopien(), 0)
        self.assertEqual(str(w_single_zero), "W(x) = 0")

        # Wielomian z bardzo dużymi współczynnikami
        w_big = Wielomian([1e10, 2e10])
        self.assertEqual(w_big(1), 3e10)

        # Wielomian z bardzo małymi współczynnikami
        w_small = Wielomian([1e-10, 2e-10])
        self.assertAlmostEqual(w_small(1), 3e-10)

    class TestBioSequenceBase(unittest.TestCase):
        """Testy bazowe dla funkcjonalności wspólnych."""

        def setUp(self):
            """Przygotowanie danych testowych."""
            self.dna = DNASequence("test_dna", "ATGC")
            self.rna = RNASequence("test_rna", "AUGC")
            self.protein = ProteinSequence("test_protein", "MK")

    class TestDNASequence(TestBioSequenceBase):
        """Testy dla klasy DNASequence."""

        def test_utworzenie_dna(self):
            """Test tworzenia sekwencji DNA."""
            dna = DNASequence("gene1", "ATGC")
            self.assertEqual(dna.identifier, "gene1")
            self.assertEqual(dna.data, "ATGC")
            self.assertEqual(dna.length, 4)

        def test_normalizacja_danych(self):
            """Test normalizacji danych wejściowych."""
            dna = DNASequence("test", "atgc  \n\t")
            self.assertEqual(dna.data, "ATGC")

            # Test z mieszanymi przypadkami
            dna2 = DNASequence("test2", "AtGc")
            self.assertEqual(dna2.data, "ATGC")

        def test_walidacja_znakow(self):
            """Test walidacji dozwolonych znaków."""
            # Prawidłowe znaki
            try:
                DNASequence("test", "ATGC")
            except ValueError:
                self.fail("Prawidłowe znaki DNA zostały odrzucone")

            # Nieprawidłowe znaki
            with self.assertRaises(ValueError):
                DNASequence("test", "ATGCX")

            with self.assertRaises(ValueError):
                DNASequence("test", "ATGCU")  # U zamiast T

        def test_puste_sekwencje(self):
            """Test obsługi pustych sekwencji."""
            with self.assertRaises(ValueError):
                DNASequence("test", "")

            with self.assertRaises(ValueError):
                DNASequence("", "ATGC")

        def test_fasta_format(self):
            """Test formatu FASTA."""
            dna = DNASequence("gene1", "ATGC")
            fasta_str = str(dna)

            self.assertIn(">gene1", fasta_str)
            self.assertIn("ATGC", fasta_str)
            self.assertTrue(fasta_str.startswith(">"))

        def test_mutacja(self):
            """Test mutacji DNA."""
            dna = DNASequence("test", "ATGC")

            # Prawidłowa mutacja
            dna.mutate(0, 'G')
            self.assertEqual(dna.data, "GTGC")

            # Test walidacji pozycji
            with self.assertRaises(IndexError):
                dna.mutate(10, 'A')