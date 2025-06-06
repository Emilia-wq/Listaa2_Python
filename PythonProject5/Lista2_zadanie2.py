from abc import ABC, abstractmethod


class BioSequence(ABC):
    """
    Abstrakcyjna klasa bazowa dla wszystkich sekwencji biologicznych.
    Implementuje wspólne funkcjonalności i definiuje interfejs.
    """

    # Zbiory dozwolonych znaków
    VALID_CHARS = set()

    def __init__(self, identifier, data):
        """
        Konstruktor bazowy dla sekwencji biologicznych.

        Args:
            identifier: identyfikator sekwencji
            data: sekwencja znaków reprezentująca dane biologiczne
        """
        if not isinstance(identifier, str) or not identifier.strip():
            raise Exception("Identyfikator musi być niepustym stringiem")

        if not isinstance(data, str):
            raise Exception("Dane sekwencji muszą być stringiem")

        # Normalizacja danych
        normalized_data = data.upper().replace(' ', '').replace('\n', '').replace('\t', '')

        # Walidacja znaków
        self._validate_sequence(normalized_data)

        self.identifier = identifier.strip()
        self.data = normalized_data
        self.length = len(self.data)

    def _validate_sequence(self, data):
        """Waliduje czy wszystkie znaki w sekwencji są dozwolone."""
        if not data:
            raise Exception("Sekwencja nie może być pusta")

        invalid_chars = set(data) - self.VALID_CHARS
        if invalid_chars:
            raise Exception(f"Nieprawidłowe znaki w sekwencji: {invalid_chars}")

    def __str__(self):
        """Zwraca reprezentację w formacie FASTA."""
        return f">{self.identifier}\n{self.data}"

    def mutate(self, position, value):
        """
        Zmienia znak na zadanej pozycji.

        Args:
            position: pozycja do zmiany (0-indexed)
            value: nowa wartość
        """
        if not isinstance(position, int):
            raise Exception("Pozycja musi być liczbą całkowitą")

        if not (0 <= position < self.length):
            raise Exception(f"Pozycja {position} poza zakresem sekwencji (0-{self.length - 1})")

        if not isinstance(value, str) or len(value) != 1:
            raise Exception("Wartość musi być pojedynczym znakiem")

        value = value.upper()
        if value not in self.VALID_CHARS:
            raise Exception(f"Nieprawidłowy znak: {value}. Dozwolone: {self.VALID_CHARS}")

        data_list = list(self.data)
        data_list[position] = value
        self.data = ''.join(data_list)

    def findMotif(self, motif):
        """
        Znajduje pozycję motywu w sekwencji.

        Args:
            motif: szukany motyw

        Returns:
            int: pozycja pierwszego wystąpienia motywu
        """
        if not isinstance(motif, str):
            raise Exception("Motyw musi być stringiem")

        motif = motif.upper().replace(' ', '')
        if not motif:
            raise Exception("Motyw nie może być pusty")

        # Walidacja znaków w motywie
        invalid_chars = set(motif) - self.VALID_CHARS
        if invalid_chars:
            raise Exception(f"Nieprawidłowe znaki w motywie: {invalid_chars}")

        return self.data.find(motif)

    def __len__(self):
        """Zwraca długość sekwencji."""
        return self.length

    def __eq__(self, other):
        """Porównanie sekwencji."""
        if not isinstance(other, BioSequence):
            return False
        return self.data == other.data and self.identifier == other.identifier


class DNASequence(BioSequence):
    """Klasa reprezentująca sekwencję DNA."""

    VALID_CHARS = {'A', 'T', 'G', 'C'}

    # Mapowanie komplementarności zasad DNA
    COMPLEMENT_MAP = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}

    # Mapowanie transkrypcji DNA -> RNA
    TRANSCRIPTION_MAP = {'A': 'A', 'T': 'U', 'G': 'G', 'C': 'C'}

    def complement(self):
        """
        Zwraca nić komplementarną do sekwencji DNA.

        Returns:
            DNASequence: komplementarna sekwencja DNA
        """
        complement_data = ''.join(self.COMPLEMENT_MAP[base] for base in self.data)
        return DNASequence(f"{self.identifier}_complement", complement_data)

    def transcribe(self):
        """
        Transkrybuje DNA do RNA.

        Returns:
            RNASequence: sekwencja RNA powstała z transkrypcji
        """
        rna_data = ''.join(self.TRANSCRIPTION_MAP[base] for base in self.data)
        return RNASequence(f"{self.identifier}_RNA", rna_data)


class RNASequence(BioSequence):
    """Klasa reprezentująca sekwencję RNA."""

    VALID_CHARS = {'A', 'U', 'G', 'C'}

    # Kod genetyczny
    GENETIC_CODE = {
        'UUU': 'F', 'UUC': 'F', 'UUA': 'L', 'UUG': 'L',
        'UCU': 'S', 'UCC': 'S', 'UCA': 'S', 'UCG': 'S',
        'UAU': 'Y', 'UAC': 'Y', 'UAA': '*', 'UAG': '*',
        'UGU': 'C', 'UGC': 'C', 'UGA': '*', 'UGG': 'W',
        'CUU': 'L', 'CUC': 'L', 'CUA': 'L', 'CUG': 'L',
        'CCU': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
        'CAU': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
        'CGU': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
        'AUU': 'I', 'AUC': 'I', 'AUA': 'I', 'AUG': 'M',
        'ACU': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
        'AAU': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
        'AGU': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
        'GUU': 'V', 'GUC': 'V', 'GUA': 'V', 'GUG': 'V',
        'GCU': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
        'GAU': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
        'GGU': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G'
    }

    def translate(self):
        """
        Tłumaczy RNA na białko.

        Returns:
            ProteinSequence: sekwencja białka powstała z translacji
        """
        if len(self.data) % 3 != 0:
            raise ValueError("Długość sekwencji RNA musi być wielokrotnością 3 dla prawidłowej translacji")

        protein_data = []

        # Czytamy kodony (po 3 nukleotydy)
        for i in range(0, len(self.data), 3):
            codon = self.data[i:i + 3]
            amino_acid = self.GENETIC_CODE.get(codon, 'X')  # X dla nieznanych kodonów

            # Zatrzymujemy translację na kodonie stop (*)
            if amino_acid == '*':
                break

            protein_data.append(amino_acid)

        return ProteinSequence(f"{self.identifier}_protein", ''.join(protein_data))


class ProteinSequence(BioSequence):
    """Klasa reprezentująca sekwencję białka."""

    # Standardowe 20 aminokwasów + kodony stop i nieznane
    VALID_CHARS = {
        'A', 'R', 'N', 'D', 'C', 'E', 'Q', 'G', 'H', 'I',
        'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V',
        'X', '*'  # X - nieznany aminokwas, * - kodon stop
    }


def demonstracja():
    print("=== DEMONSTRACJA KLAS SEKWENCJI BIOLOGICZNYCH ===\n")

    # 1. Tworzenie sekwencji DNA
    print("1. Tworzenie sekwencji DNA:")
    dna = DNASequence("gene1", "ATGCGATCGTAGC")
    print(f"DNA: {dna}")
    print(f"Długość: {dna.length}")
    print()

    # 2. Operacje na DNA
    print("2. Operacje na DNA:")

    # Mutacja
    print("Przed mutacją:", dna.data)
    dna.mutate(0, 'G')
    print("Po mutacji (pozycja 0 -> G):", dna.data)

    # Przywrócenie oryginalnej sekwencji
    dna.mutate(0, 'A')

    # Znajdowanie motywu
    motif_pos = dna.findMotif("GCG")
    print(f"Pozycja motywu 'GCG': {motif_pos}")

    # Komplementarność
    complement = dna.complement()
    print(f"Komplementarna: {complement.data}")

    # Transkrypcja
    rna = dna.transcribe()
    print(f"RNA z transkrypcji: {rna.data}")
    print()

    # 3. Operacje na RNA
    print("3. Operacje na RNA:")

    # Tworzenie sekwencji RNA kodującej białko
    rna_coding = RNASequence("mRNA1", "AUGUGCGAUCGUAGC")
    print(f"RNA kodujące: {rna_coding.data}")

    # Sprawdzenie czy można przetłumaczyć (długość musi być wielokrotnością 3)
    if len(rna_coding.data) % 3 == 0:
        try:
            protein = rna_coding.translate()
            print(f"Białko z translacji: {protein.data}")
        except ValueError as e:
            print(f"Błąd translacji: {e}")
    else:
        print("Sekwencja RNA nie ma odpowiedniej długości do translacji")

    # Przykład z prawidłową sekwencją
    rna_proper = RNASequence("mRNA2", "AUGUGCGAUCGU")  # 12 nukleotydów = 4 kodony
    protein = rna_proper.translate()
    print(f"RNA prawidłowe: {rna_proper.data}")
    print(f"Białko: {protein.data}")
    print()

    # 4. Operacje na białku
    print("4. Operacje na białku:")

    protein_seq = ProteinSequence("protein1", "MAIDV")
    print(f"Białko: {protein_seq}")

    # Mutacja w białku
    print("Przed mutacją:", protein_seq.data)
    protein_seq.mutate(1, 'L')
    print("Po mutacji (pozycja 1 -> L):", protein_seq.data)

    # Znajdowanie motywu w białku
    motif_pos = protein_seq.findMotif("LI")
    print(f"Pozycja motywu 'LI': {motif_pos}")
    print()

    # 5. Kompletny przepływ: DNA -> RNA -> Protein
    print("5. Kompletny przepływ: DNA -> RNA -> Protein:")

    # Sekwencja DNA kodująca krótkie białko
    original_dna = DNASequence("complete_gene", "ATGAAATTCGGATAA")
    print(f"DNA: {original_dna.data}")

    # Transkrypcja
    mrna = original_dna.transcribe()
    print(f"mRNA: {mrna.data}")

    # Translacja
    final_protein = mrna.translate()
    print(f"Białko: {final_protein.data}")

    # Dekodowanie aminokwasów
    amino_names = {
        'M': 'Metionina', 'K': 'Lizyna', 'F': 'Fenyloalanina',
        'G': 'Glicyna', '*': 'STOP'
    }
    decoded = [amino_names.get(aa, aa) for aa in final_protein.data]
    print(f"Aminokwasy: {' - '.join(decoded)}")

    if __name__ == "__main__":
        demonstracja()

