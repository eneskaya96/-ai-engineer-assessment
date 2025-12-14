"""Benchmark tests for similarity methods using the addresses.csv dataset."""

import csv
import time
from pathlib import Path
from dataclasses import dataclass
from typing import List

import pytest

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

from similarity import get_all_methods, SimilarityMethod


@dataclass
class BenchmarkResult:
    """Result of benchmarking a similarity method."""
    method_name: str
    method_value: str
    mae: float  # Mean Absolute Error
    mse: float  # Mean Squared Error
    correlation: float  # Pearson correlation
    total_time_ms: float
    avg_time_ms: float
    sample_count: int


def load_test_data() -> List[dict]:
    """Load test data from addresses.csv."""
    csv_path = Path(__file__).parent.parent.parent / "data" / "addresses.csv"

    data = []
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Skip rows with missing data
            if row["address"] and row["matched_address"]:
                data.append({
                    "address": row["address"],
                    "matched_address": row["matched_address"],
                    "semantic_similarity": float(row["semantic_similarity"]),
                })
    return data


def calculate_correlation(x: List[float], y: List[float]) -> float:
    """Calculate Pearson correlation coefficient."""
    n = len(x)
    if n == 0:
        return 0.0

    mean_x = sum(x) / n
    mean_y = sum(y) / n

    numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))

    sum_sq_x = sum((xi - mean_x) ** 2 for xi in x)
    sum_sq_y = sum((yi - mean_y) ** 2 for yi in y)

    denominator = (sum_sq_x * sum_sq_y) ** 0.5

    if denominator == 0:
        return 0.0

    return numerator / denominator


def run_benchmark(test_data: List[dict]) -> List[BenchmarkResult]:
    """Run benchmark for all similarity methods."""
    methods = get_all_methods()
    results = []

    for method_enum, method_instance in methods.items():
        predicted_scores = []
        actual_scores = []

        start_time = time.perf_counter()

        for row in test_data:
            score = method_instance.calculate(
                row["address"],
                row["matched_address"]
            )
            predicted_scores.append(score)
            actual_scores.append(row["semantic_similarity"])

        end_time = time.perf_counter()
        total_time_ms = (end_time - start_time) * 1000

        # Calculate metrics
        n = len(predicted_scores)

        # MAE
        mae = sum(abs(p - a) for p, a in zip(predicted_scores, actual_scores)) / n

        # MSE
        mse = sum((p - a) ** 2 for p, a in zip(predicted_scores, actual_scores)) / n

        # Correlation
        correlation = calculate_correlation(predicted_scores, actual_scores)

        results.append(BenchmarkResult(
            method_name=method_instance.name,
            method_value=method_enum.value,
            mae=mae,
            mse=mse,
            correlation=correlation,
            total_time_ms=total_time_ms,
            avg_time_ms=total_time_ms / n,
            sample_count=n,
        ))

    return results


def print_results_table(results: List[BenchmarkResult]) -> None:
    """Print benchmark results as a formatted table."""
    # Sort by MAE (lower is better)
    results_sorted = sorted(results, key=lambda r: r.mae)

    print("\n" + "=" * 100)
    print("SIMILARITY METHOD BENCHMARK RESULTS")
    print("=" * 100)
    print(f"\n{'Method':<30} {'MAE':>10} {'MSE':>10} {'Corr':>10} {'Time(ms)':>12} {'Avg(ms)':>10}")
    print("-" * 100)

    for r in results_sorted:
        print(
            f"{r.method_name:<30} "
            f"{r.mae:>10.4f} "
            f"{r.mse:>10.4f} "
            f"{r.correlation:>10.4f} "
            f"{r.total_time_ms:>12.2f} "
            f"{r.avg_time_ms:>10.4f}"
        )

    print("-" * 100)
    print(f"Total samples: {results[0].sample_count}")
    print("\nLower MAE = Better | Higher Correlation = Better")
    print("=" * 100 + "\n")


class TestSimilarityBenchmark:
    """Benchmark test suite for similarity methods."""

    @pytest.fixture(scope="class")
    def test_data(self) -> List[dict]:
        """Load test data once for all tests."""
        return load_test_data()

    @pytest.fixture(scope="class")
    def benchmark_results(self, test_data) -> List[BenchmarkResult]:
        """Run benchmark once for all tests."""
        return run_benchmark(test_data)

    def test_data_loads_correctly(self, test_data):
        """Verify test data loads properly."""
        assert len(test_data) > 0
        assert all("address" in row for row in test_data)
        assert all("matched_address" in row for row in test_data)
        assert all("semantic_similarity" in row for row in test_data)

    def test_all_methods_run(self, benchmark_results):
        """Verify all methods complete without errors."""
        expected_methods = len(SimilarityMethod)
        assert len(benchmark_results) == expected_methods

    def test_scores_in_valid_range(self, test_data):
        """Verify all methods return scores in [0, 1] range."""
        methods = get_all_methods()

        for method_enum, method_instance in methods.items():
            for row in test_data[:10]:  # Test subset for speed
                score = method_instance.calculate(
                    row["address"],
                    row["matched_address"]
                )
                assert 0.0 <= score <= 1.0, (
                    f"{method_enum.value} returned {score} for "
                    f"{row['address']} vs {row['matched_address']}"
                )

    def test_print_benchmark_results(self, benchmark_results):
        """Print benchmark results (always passes, just for output)."""
        print_results_table(benchmark_results)
        assert True


# Allow running as standalone script
if __name__ == "__main__":
    print("Loading test data...")
    data = load_test_data()
    print(f"Loaded {len(data)} address pairs")

    print("\nRunning benchmark...")
    results = run_benchmark(data)

    print_results_table(results)

    # Export results to CSV for EXPERIMENTS.md
    output_path = Path(__file__).parent.parent.parent / "benchmark_results.csv"
    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Method", "MAE", "MSE", "Correlation", "Total Time (ms)", "Avg Time (ms)"])
        for r in sorted(results, key=lambda x: x.mae):
            writer.writerow([
                r.method_name,
                f"{r.mae:.4f}",
                f"{r.mse:.4f}",
                f"{r.correlation:.4f}",
                f"{r.total_time_ms:.2f}",
                f"{r.avg_time_ms:.4f}",
            ])
    print(f"\nResults exported to: {output_path}")