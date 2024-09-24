from math import isclose

from scipy.spatial.distance import cosine
import numpy as np
import pytest

from oxli import KmerCountTable

# Cosine similarity tests


def test_cosine_similarity_identical_tables():
    """
    Test cosine similarity for two identical KmerCountTable objects.

    The cosine similarity should be 1.0 because the vectors representing
    the k-mer counts are exactly the same, meaning the angle between them
    is 0 degrees (cos(0) = 1).
    """
    kct1 = KmerCountTable(ksize=4)
    kct2 = KmerCountTable(ksize=4)

    # Manually set k-mer counts
    kct1["AAAA"] = 5
    kct1["AATT"] = 3
    kct1["GGGG"] = 1
    kct1["CCAA"] = 4
    kct1["ATTG"] = 6

    # Copy the exact same counts to kct2
    kct2["AAAA"] = 5
    kct2["AATT"] = 3
    kct2["GGGG"] = 1
    kct2["CCAA"] = 4
    kct2["ATTG"] = 6

    # Cosine similarity between identical tables should be 1.0
    # Allow value within 0.001%
    assert isclose(kct1.cosine(kct2), 1.0, rel_tol=1e-5)
    assert isclose(kct2.cosine(kct1), 1.0, rel_tol=1e-5)

    # Using scipy to calculate the expected value
    vector1 = [5, 3, 1, 4, 6]
    vector2 = [5, 3, 1, 4, 6]
    expected_cosine_sim = 1 - cosine(vector1, vector2)

    # Allow value within 0.001%
    assert isclose(kct1.cosine(kct2), expected_cosine_sim, rel_tol=1e-5)
    assert isclose(kct2.cosine(kct1), expected_cosine_sim, rel_tol=1e-5)


def test_cosine_similarity_different_tables():
    """
    Test cosine similarity for two different KmerCountTable objects.

    The cosine similarity will be less than 1.0 since the vectors
    are not identical. We will calculate the expected cosine
    similarity using scipy.
    """
    kct1 = KmerCountTable(ksize=4)
    kct2 = KmerCountTable(ksize=4)

    # Manually set k-mer counts for kct1
    kct1["AAAA"] = 4
    kct1["AATT"] = 3
    kct1["GGGG"] = 1
    kct1["CCAA"] = 4
    kct1["ATTG"] = 6

    # Manually set different counts for kct2
    kct2["AAAA"] = 5
    kct2["AATT"] = 3
    kct2["GGGG"] = 1
    kct2["CCAA"] = 4
    kct2["ATTG"] = 0

    # Using scipy to calculate the expected value
    vector1 = [4, 3, 1, 4, 6]
    vector2 = [5, 3, 1, 4, 0]
    expected_cosine_sim = 1 - cosine(vector1, vector2)

    # Allow value within 0.001%
    assert isclose(kct1.cosine(kct2), expected_cosine_sim, rel_tol=1e-5)
    assert isclose(kct2.cosine(kct1), expected_cosine_sim, rel_tol=1e-5)


def test_cosine_similarity_empty_table():
    """
    Test cosine similarity for two KmerCountTable objects where one is empty.

    The cosine similarity should be 0.0 because the dot product with an
    empty table will result in zero, making the numerator of the cosine
    similarity formula zero.
    """
    kct1 = KmerCountTable(ksize=4)
    kct2 = KmerCountTable(ksize=4)

    # Set counts for kct1
    kct1["AAAA"] = 5
    kct1["TTTG"] = 10

    # Leave kct2 empty

    # Cosine similarity should be 0 since one table is empty
    assert kct1.cosine(kct2) == 0.0

    # Set kct2 with 1 non-overlapping kmer
    kct2["ATTG"] = 1

    # Cosine similarity should be 0 since no shared kmers
    assert kct1.cosine(kct2) == 0.0

    # Using scipy for comparison
    vector1 = [5, 10, 0]
    vector2 = [0, 0, 1]  # Representing the empty table with no overlap
    expected_cosine_sim = 1 - cosine(vector1, vector2)

    assert isclose(kct1.cosine(kct2), expected_cosine_sim, rel_tol=1e-5)
    assert isclose(kct2.cosine(kct1), expected_cosine_sim, rel_tol=1e-5)


def test_cosine_similarity_both_empty():
    """
    Test cosine similarity for two empty KmerCountTable objects.
    """
    # Both tables are empty
    kct1 = KmerCountTable(ksize=4)
    kct2 = KmerCountTable(ksize=4)

    # Cosine similarity should be 0.0 for two empty tables
    assert kct1.cosine(kct2) == 0.0
    assert kct2.cosine(kct1) == 0.0


def test_cosine_similarity_partial_overlap():
    """
    Test cosine similarity for two KmerCountTable objects with partial overlap in k-mers.

    The cosine similarity should be less than 1.0 but greater than 0.0 because
    the tables have overlapping k-mers, but their counts differ.
    """
    kct1 = KmerCountTable(ksize=4)
    kct2 = KmerCountTable(ksize=4)

    # Manually set k-mer counts for kct1
    # kct1["AAAA"] = 0  # Not in kct2
    kct1["AATT"] = 3
    kct1["GGGG"] = 1
    kct1["CCAA"] = 4
    kct1["ATTG"] = 0
    kct1["AGAT"] = 0  # Set but not in either

    # Manually set k-mer counts for kct2
    kct2["AAAA"] = 5
    kct2["AATT"] = 4  # Diff value to kct1
    kct2["GGGG"] = 1
    kct2["CCAA"] = 4
    kct2["ATTG"] = 1  # Not in kct1

    # Using scipy for comparison
    vector1 = [0, 3, 1, 4, 0, 0]
    vector2 = [5, 4, 1, 4, 1, 0]
    expected_cosine_sim = 1 - cosine(vector1, vector2)

    # Cosine similarity is expected to be > 0 but < 1
    assert isclose(kct1.cosine(kct2), expected_cosine_sim, rel_tol=1e-5)
    assert isclose(kct2.cosine(kct1), expected_cosine_sim, rel_tol=1e-5)


# Jaccard coefficient similarity tests


def test_jaccard_similarity_identical_tables():
    """
    Test Jaccard similarity for two identical KmerCountTable objects.

    The Jaccard similarity should be 1.0 because both tables contain exactly the same k-mers.
    """
    kct1 = KmerCountTable(ksize=4)
    kct2 = KmerCountTable(ksize=4)

    # Manually set identical k-mer counts for both tables
    kct1["AAAA"] = 5
    kct1["TTTC"] = 2
    kct1["AATT"] = 3
    kct1["GGGG"] = 1

    kct2["AAAA"] = 5
    kct2["TTTC"] = 2
    kct2["AATT"] = 3
    kct2["GGGG"] = 1

    # Jaccard similarity should be 1.0 for identical sets
    assert kct1.jaccard(kct2) == 1.0
    assert kct2.jaccard(kct1) == 1.0


def test_jaccard_similarity_different_tables():
    """
    Test Jaccard similarity for two KmerCountTable objects with different k-mers.

    The Jaccard similarity will be less than 1.0 because the sets of k-mers differ.
    """
    kct1 = KmerCountTable(ksize=4)
    kct2 = KmerCountTable(ksize=4)

    # Set different k-mer counts for both tables
    kct1["AAAA"] = 5
    kct1["TTTC"] = 2

    kct2["AATT"] = 3
    kct2["GGGG"] = 4

    # Expected result: 0 overlap between the sets
    assert kct1.jaccard(kct2) == 0.0
    assert kct2.jaccard(kct1) == 0.0


def test_jaccard_similarity_partial_overlap():
    """
    Test Jaccard similarity for two KmerCountTable objects with partial overlap in k-mers.

    The Jaccard similarity should be greater than 0.0 but less than 1.0 because there are overlapping k-mers.
    """
    kct1 = KmerCountTable(ksize=4)
    kct2 = KmerCountTable(ksize=4)

    # Set k-mer counts for kct1
    kct1["AAAA"] = 5
    kct1["AATT"] = 1
    kct1["TTTC"] = 2

    # Set k-mer counts for kct2
    kct2["AAAA"] = 2
    kct2["AATT"] = 1
    kct2["GGGG"] = 4

    # Calculate expected Jaccard similarity: intersection {AAAA, AATT}, union {AAAA, TTTT, AATT, GGGG}
    assert kct1.jaccard(kct2) == 2 / 4
    assert kct2.jaccard(kct1) == 2 / 4


def test_jaccard_similarity_empty_table():
    """
    Test Jaccard similarity for two KmerCountTable objects where one is empty.

    The Jaccard similarity should be 0.0 because one set is empty, and the union is non-empty.
    """
    kct1 = KmerCountTable(ksize=4)
    kct2 = KmerCountTable(ksize=4)

    # Set counts for kct1
    kct1["AAAA"] = 5
    kct1["TTTC"] = 5

    # kct2 is empty
    assert kct1.jaccard(kct2) == 0.0
    assert kct2.jaccard(kct1) == 0.0


def test_jaccard_similarity_both_empty():
    """
    Test Jaccard similarity for two empty KmerCountTable objects.

    The Jaccard similarity should be 1.0 because both sets are empty, and thus identical.
    """
    kct1 = KmerCountTable(ksize=4)
    kct2 = KmerCountTable(ksize=4)

    # Both tables are empty
    assert kct1.jaccard(kct2) == 1.0
    assert kct2.jaccard(kct1) == 1.0
