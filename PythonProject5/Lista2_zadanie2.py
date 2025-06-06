from abc import ABC, abstractmethod

"""
@author Emilia Romanowska

Źródła:
- Dokumentacja Python: https://docs.python.org/3/reference/index.html
- Wsparcie koncepcyjne i techniczne: ChatGPT 
"""


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


if __name__ == "__main__":

    # DNA
    dna = DNASequence("gene1", "ATGCGT")
    print("1. Sekwencja DNA:")
    print(dna)
    print(f"Długość: {len(dna)}")

    print("\n2. Mutacja DNA na pozycji 2 (C -> A):")
    dna.mutate(2, 'A')
    print(dna)

    print("\n3. Komplementarna sekwencja DNA:")
    print(dna.complement())

    print("\n4. Transkrypcja do RNA:")
    rna = dna.transcribe()
    print(rna)

    # RNA
    print("\n5. Znajdowanie motywu w RNA:")
    pos = rna.findMotif("UG")
    print(f"Motyw 'UG' znaleziony na pozycji: {pos}")

    print("\n6. Translacja RNA do białka:")
    try:
        protein = rna.translate()
        print(protein)
    except ValueError as e:
        print("Błąd translacji:", e)

    # Protein
    print("\n7. Mutacja białka na pozycji 0:")
    if len(protein.data) > 0:
        protein.mutate(0, 'L')
        print(protein)

    print("\n8. Znajdowanie motywu 'LA' w białku:")
    print("Pozycja:", protein.findMotif("LA"))
