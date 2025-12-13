# Address Similarity Experiments

This document describes the experiments conducted to improve the address similarity function.

## Problem Statement

Given two addresses (original input and Mapbox geocoded result), we need to score how likely they refer to the same real-world location on a scale of 0.0 to 1.0.

### Challenges

- **Language differences**: "Parijs, Frankrijk" vs "Paris, France"
- **Spelling variations**: "Königstraße" vs "Konigstrasse"
- **Format differences**: "Germany,Bremen,28309" vs "Am Wasserturm 2, 28309 Bremen"
- **Abbreviations**: "NR." vs "Number", "AT" vs "Austria"
- **Missing/Extra information**: Some addresses have more detail than others

## Methods Tested

### 1. Baseline (SequenceMatcher)

- **Description**: Python's built-in `difflib.SequenceMatcher` using longest contiguous matching subsequence
- **Pros**: Simple, no dependencies, fast
- **Cons**: Character-level comparison, sensitive to word order

### 2. Levenshtein Distance

- **Description**: Minimum edit operations (insert, delete, substitute) normalized to [0,1]
- **Pros**: Well-understood metric, handles typos well
- **Cons**: Still character-level, expensive for long strings

### 3. Jaro-Winkler

- **Description**: Originally designed for name matching, gives bonus to matching prefixes
- **Pros**: Good for names and short strings, handles transpositions
- **Cons**: Less effective for long addresses with different structures

### 4. Token-Based (Jaccard)

- **Description**: Splits into tokens, calculates intersection/union ratio
- **Pros**: Order-independent, handles reordering well
- **Cons**: Loses positional information, sensitive to tokenization

### 5. Phonetic (Soundex)

- **Description**: Encodes words by pronunciation, matches phonetically similar words
- **Pros**: Handles transliterations (Parijs/Paris), spelling variations
- **Cons**: Designed for English, may miss numeric differences

### 6. RapidFuzz Combined

- **Description**: Weighted combination of ratio, partial_ratio, token_sort_ratio, token_set_ratio
- **Pros**: Best of multiple approaches, handles various edge cases
- **Cons**: Heavier dependency, slightly slower

## Benchmark Results

Run the benchmark script to generate results:

```bash
cd backend
python tests/test_similarity_benchmark.py
```

| Method | MAE | MSE | Correlation | Total Time (ms) | Avg Time (ms) |
|--------|-----|-----|-------------|-----------------|---------------|
| **Jaro-Winkler** | **0.1387** | 0.0310 | **0.5218** | 15.86 | 0.0317 |
| RapidFuzz Combined | 0.1656 | 0.0437 | 0.4647 | 5.65 | 0.0113 |
| Baseline (SequenceMatcher) | 0.2085 | 0.0741 | 0.4654 | 14.45 | 0.0289 |
| Token-Based (Jaccard) | 0.2496 | 0.0797 | 0.5119 | 17.75 | 0.0355 |
| Phonetic (Soundex) | 0.2599 | 0.0980 | 0.4779 | 6.88 | 0.0138 |
| Levenshtein Distance | 0.2945 | 0.1168 | 0.4799 | 139.38 | 0.2788 |

**Metrics Explanation:**
- **MAE (Mean Absolute Error)**: Average absolute difference from ground truth. Lower is better.
- **MSE (Mean Squared Error)**: Penalizes large errors more. Lower is better.
- **Correlation**: How well the ranking matches ground truth. Higher is better (max 1.0).

## Analysis

### Key Observations

1. **Token-based methods** generally perform better for addresses because:
   - Address components can appear in different orders
   - Partial matches (same city, different street) should still score moderately

2. **Phonetic matching** helps with:
   - International addresses with transliterated names
   - Common spelling variations

3. **Character-level methods** (Baseline, Levenshtein) struggle with:
   - Completely different word orders
   - Extra/missing address components

### Selected Approach

Based on the benchmark results, **Jaro-Winkler** was selected as the default method because:

1. **Best MAE (0.1387)**: Lowest average error compared to ground truth
2. **Best Correlation (0.5218)**: Most accurate ranking of address pairs
3. **Reasonable speed**: 15.86ms for 500 samples (~0.03ms per comparison)
4. **No external dependencies**: Pure Python implementation
5. **Prefix bonus**: Particularly effective for addresses that often share common prefixes (street names, city names)

## Future Improvements

### Pre-processing
- **Address normalization**: Expand abbreviations (St. -> Street), standardize country names
- **LLM-based cleaning**: Use Gemini/GPT to standardize address format before comparison
- **Component extraction**: Parse addresses into structured parts (street, city, postal code, country)

### Advanced Methods
- **Sentence embeddings**: Use transformer models (sentence-transformers) for semantic similarity
- **Fine-tuned models**: Train on address-specific datasets
- **Ensemble methods**: Combine multiple methods with learned weights

### Evaluation
- **Threshold analysis**: Find optimal score thresholds for accept/review/reject
- **Error analysis**: Categorize failure cases to guide improvements
- **A/B testing**: Compare methods on real user feedback

## Reproduction

To run experiments:

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Run benchmark
python tests/test_similarity_benchmark.py

# Or via pytest
pytest tests/test_similarity_benchmark.py -v -s
```

## Architecture

```
backend/
├── similarity/
│   ├── __init__.py          # Module exports
│   ├── base.py              # Abstract base class
│   ├── enums.py             # SimilarityMethod enum
│   ├── factory.py           # Factory pattern
│   └── methods/
│       ├── baseline.py      # SequenceMatcher
│       ├── levenshtein.py   # Edit distance
│       ├── jaro_winkler.py  # Jaro-Winkler
│       ├── token_based.py   # Jaccard similarity
│       ├── phonetic.py      # Soundex encoding
│       └── fuzzy.py         # RapidFuzz combined
├── similarity.py            # Main entry point
└── tests/
    └── test_similarity_benchmark.py
```

### Adding New Methods

1. Create new file in `similarity/methods/`
2. Extend `BaseSimilarity` class
3. Add to `SimilarityMethod` enum
4. Register in `factory.py`
5. Run benchmark to compare