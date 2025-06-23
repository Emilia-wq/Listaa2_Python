import unittest

from PythonProject5.Lista2_zadanie1 import Wielomian
from PythonProject5.Lista2_zadanie2 import DNASequence, RNASequence, ProteinSequence

"""
@author Emilia Romanowska

Źródła:
- Dokumentacja Python: https://docs.python.org/3/reference/index.html
- Wsparcie koncepcyjne i techniczne: ChatGPT 
"""


class TestWielomian(unittest.TestCase):
    """Testy jednostkowe dla klasy Wielomian."""

    
# użycie metody setUp(self) - chat.gpt
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
        with self.assertRaises(Exception):
            Wielomian([])

        # Nieprawidłowy typ argumentu - chat.gpt
        with self.assertRaises(Exception):
            Wielomian("123")

        # Nieprawidłowy typ współczynnika - chat.gpt
        with self.assertRaises(Exception):
            Wielomian([1, "abc", 3])


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

        # Test dla różnych wartości x = chat.gpt
        self.assertEqual(w(0), 1)  # 1 + 0 + 0 = 1
        self.assertEqual(w(1), 6)  # 1 + 2 + 3 = 6
        self.assertEqual(w(2), 17)  # 1 + 4 + 12 = 17

        # Test z liczbami ujemnymi
        self.assertEqual(w(-1), 2)  # 1 - 2 + 3 = 2

        # Test z liczbami zmiennoprzecinkowymi
        self.assertAlmostEqual(w(0.5), 2.75)  # 1 + 1 + 0.75 = 2.75

        # Test błędnego typu argumentu - chat.gpt
        with self.assertRaises(Exception):
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

        # Test błędnego typu - chat.gpt
        with self.assertRaises(Exception):
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

        # Test błędnego typu - chat.gpt
        with self.assertRaises(Exception):
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

        # Test błędnego typu - chat.gpt
        with self.assertRaises(Exception):
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

        # Test błędnego typu - chat.gpt
        with self.assertRaises(Exception):
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
        with self.assertRaises(Exception):
            w1 -= "test"

    def test_operator_imul(self):
        """Test operatora *=."""
        w1 = Wielomian([1, 1])  # 1 + x
        w2 = Wielomian([1, 1])  # 1 + x

        w1 *= w2  # (1 + x)^2
        self.assertEqual(w1.get_wspolczynniki(), [1, 2, 1])

        # Test błędnego typu - chat.gpt
        with self.assertRaises(Exception):
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

        # Test z innym typem - chat.gpt
        self.assertFalse(w1 == "wielomian")
        self.assertTrue(w1 != 42)


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

        def test_normalizacja_danych(self): - chat.gpt
            """Test normalizacji danych wejściowych."""
            dna = DNASequence("test", "atgc  \n\t")
            self.assertEqual(dna.data, "ATGC")

            # Test z mieszanymi przypadkami
            dna2 = DNASequence("test2", "AtGc")
            self.assertEqual(dna2.data, "ATGC")

        def test_walidacja_znakow(self): - chat.gpt
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

        def test_puste_sekwencje(self): - chat.gpt
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

    class TestRNASequence(unittest.TestCase):
        """Testy dla klasy RNASequence."""

        def test_utworzenie_rna(self):
            rna = RNASequence("rna1", "AUGC")
            self.assertEqual(rna.data, "AUGC")
            self.assertEqual(rna.identifier, "rna1")
            self.assertEqual(rna.length, 4)

        def test_format_fasta(self):
            rna = RNASequence("rna1", "AUGC")
            fasta = str(rna)
            self.assertTrue(fasta.startswith(">"))
            self.assertIn("AUGC", fasta)

        def test_walidacja_znakow(self):
            with self.assertRaises(ValueError):
                RNASequence("bad", "AUGCX")

        def test_translate_correct(self):
            rna = RNASequence("test", "AUGGAAUAA")  # Met-Glu-STOP
            protein = rna.translate()
            self.assertEqual(protein.data, "ME")

        def test_translate_with_unknown_codon(self):
            rna = RNASequence("test", "AUGXYZUAA")  # 'XYZ' to nieznany kodon
            with self.assertRaises(ValueError):
                rna.translate()  # Długość niepodzielna przez 3 – też łapie błąd

        def test_translate_invalid_length(self): - chat.gpt
            rna = RNASequence("test", "AUGAA")
            with self.assertRaises(ValueError):
                rna.translate()

        def test_find_motif_rna(self):
            rna = RNASequence("test", "AUGCGUGGA")
            self.assertEqual(rna.findMotif("CGU"), 3)

        def test_mutacja_rna(self):
            rna = RNASequence("test", "AUGC")
            rna.mutate(0, 'G')
            self.assertEqual(rna.data, "GUGC")

            with self.assertRaises(IndexError):
                rna.mutate(99, 'A')

            with self.assertRaises(ValueError):
                rna.mutate(1, 'X')

    class TestProteinSequence(unittest.TestCase):
        """Testy dla klasy ProteinSequence."""

        def test_utworzenie_protein(self):
            protein = ProteinSequence("prot1", "MKL")
            self.assertEqual(protein.data, "MKL")
            self.assertEqual(protein.identifier, "prot1")
            self.assertEqual(protein.length, 3)

        def test_format_fasta_protein(self):
            protein = ProteinSequence("prot1", "MKL")
            fasta = str(protein)
            self.assertTrue(fasta.startswith(">"))
            self.assertIn("MKL", fasta)

        def test_walidacja_protein(self): - chat.gpt
            with self.assertRaises(ValueError):
                ProteinSequence("bad", "MKTZ")  # 'Z' nie jest dozwolonym znakiem

        def test_mutacja_protein(self):
            protein = ProteinSequence("prot1", "MKV")
            protein.mutate(2, 'L')
            self.assertEqual(protein.data, "MKL")

            with self.assertRaises(ValueError):
                protein.mutate(0, "Z")

            with self.assertRaises(IndexError):
                protein.mutate(99, 'L')

        def test_find_motif_protein(self):
            protein = ProteinSequence("prot1", "MALKG")
            self.assertEqual(protein.findMotif("ALK"), 1)
            self.assertEqual(protein.findMotif("XYZ"), -1)

        def test_equality_protein(self): -chat.gpt
            p1 = ProteinSequence("p", "MK")
            p2 = ProteinSequence("p", "MK")
            p3 = ProteinSequence("p", "ML")
            self.assertTrue(p1 == p2)
            self.assertFalse(p1 == p3)
