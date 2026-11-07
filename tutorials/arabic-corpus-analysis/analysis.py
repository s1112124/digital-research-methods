"""Educational Arabic corpus comparison using wholly synthetic documents.

Token frequencies, G^2 (log-likelihood) keyness and token-based KWIC.
No web requests, credentials or access to real platform data.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import math
from pathlib import Path
import re
import unicodedata

HERE = Path(__file__).resolve().parent
DIACRITICS = re.compile(r"[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06ED]")
ARABIC_WORD = re.compile(r"[\u0621-\u064A\u0671]+")
ALEF_FOLD = str.maketrans({"آ": "ا", "أ": "ا", "إ": "ا", "ٱ": "ا"})


def normalize_arabic(text: str, *, fold_alef: bool = False) -> str:
    """Remove tashkeel/tatweel; preserve lexical spellings unless opted-in."""
    cleaned = unicodedata.normalize("NFKC", text)
    cleaned = DIACRITICS.sub("", cleaned).replace("ـ", "")
    if fold_alef:
        cleaned = cleaned.translate(ALEF_FOLD)
    return cleaned


def tokenize(text: str, *, fold_alef: bool = False) -> list[str]:
    """Simple surface-word tokenizer, not stemming or clitic segmentation."""
    return ARABIC_WORD.findall(normalize_arabic(text, fold_alef=fold_alef))


def read_documents(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or not {"doc_id", "text"}.issubset(reader.fieldnames):
            raise ValueError(f"{path.name}: expected 'doc_id' and 'text' columns")
        documents = []
        seen = set()
        for row in reader:
            doc_id = (row.get("doc_id") or "").strip()
            text = (row.get("text") or "").strip()
            if not doc_id or not text:
                raise ValueError(f"{path.name}: document ID and text must be non-empty")
            if doc_id in seen:
                raise ValueError(f"{path.name}: duplicate document ID {doc_id!r}")
            seen.add(doc_id)
            documents.append({"doc_id": doc_id, "text": text})
    if not documents:
        raise ValueError(f"{path.name}: no documents found")
    return documents


def count_tokens(documents: list[dict[str, str]], *, fold_alef: bool = False) -> Counter[str]:
    counts: Counter[str] = Counter()
    for doc in documents:
        counts.update(tokenize(doc["text"], fold_alef=fold_alef))
    if not counts:
        raise ValueError("No Arabic word tokens found in corpus")
    return counts


def likelihood_ratio(focus_count: int, focus_total: int,
                     reference_count: int, reference_total: int) -> float:
    """2x2 likelihood-ratio statistic G^2, using 0 * log(0/E) = 0."""
    if focus_total <= 0 or reference_total <= 0:
        raise ValueError("Both corpus totals must be positive")
    if not (0 <= focus_count <= focus_total and 0 <= reference_count <= reference_total):
        raise ValueError("Token counts must lie within corpus totals")
    observed = ((focus_count, focus_total - focus_count),
                (reference_count, reference_total - reference_count))
    column_totals = (focus_count + reference_count,
                     focus_total + reference_total - focus_count - reference_count)
    grand_total = focus_total + reference_total
    score = 0.0
    for row, row_total in zip(observed, (focus_total, reference_total)):
        for cell, col_total in zip(row, column_totals):
            expected = row_total * col_total / grand_total
            if cell and expected:
                score += cell * math.log(cell / expected)
    return max(0.0, 2.0 * score)


def bh_adjust(p_values: list[float]) -> list[float]:
    """Benjamini-Hochberg adjustment across all tested word types."""
    m = len(p_values)
    if not m:
        return []
    order = sorted(range(m), key=lambda i: p_values[i])
    result = [1.0] * m
    running = 1.0
    for rank in range(m, 0, -1):
        idx = order[rank - 1]
        running = min(running, p_values[idx] * m / rank)
        result[idx] = min(1.0, running)
    return result


def frequency_rows(counts: Counter[str]) -> list[dict[str, object]]:
    total = sum(counts.values())
    return [{"word": word, "count": freq,
             "per_10000": round(freq * 10000 / total, 2)}
            for word, freq in sorted(counts.items(), key=lambda t: (-t[1], t[0]))]


def keyness_rows(focus: Counter[str], reference: Counter[str]) -> list[dict[str, object]]:
    total_f = sum(focus.values())
    total_r = sum(reference.values())
    rows = []
    for word in sorted(set(focus) | set(reference)):
        f = focus[word]
        r = reference[word]
        g2 = likelihood_ratio(f, total_f, r, total_r)
        # Chi-square(1) survival function: P(chi^2 >= G^2) = erfc(sqrt(G^2/2))
        p = math.erfc(math.sqrt(g2 / 2.0))
        # Continuity-adjusted log2 rate ratio, useful even when one count is zero.
        effect = math.log2((f + 0.5) / (total_f + 0.5)) - math.log2(
            (r + 0.5) / (total_r + 0.5))
        direction = "focus" if f / total_f > r / total_r else (
            "reference" if f / total_f < r / total_r else "equal")
        rows.append({"word": word, "focus_count": f, "reference_count": r,
                     "focus_per_10000": round(10000 * f / total_f, 2),
                     "reference_per_10000": round(10000 * r / total_r, 2),
                     "g2": round(g2, 5), "p_chi2_approx": p,
                     "log2_rate_ratio_adjusted": round(effect, 4), "direction": direction})
    q_values = bh_adjust([float(row["p_chi2_approx"]) for row in rows])
    for row, q in zip(rows, q_values):
        row["bh_q_exploratory"] = q
    rows.sort(key=lambda row: (-float(row["g2"]), str(row["word"])))
    return rows


def kwic_rows(documents: list[dict[str, str]], query: str, *,
              corpus_label: str, window: int = 4, fold_alef: bool = False
              ) -> list[dict[str, object]]:
    if window < 0:
        raise ValueError("KWIC window must be nonnegative")
    query_tokens = tokenize(query, fold_alef=fold_alef)
    if len(query_tokens) != 1:
        raise ValueError("Query must contain exactly one Arabic surface-word token")
    target = query_tokens[0]
    found = []
    for doc in documents:
        tokens = tokenize(doc["text"], fold_alef=fold_alef)
        for i, word in enumerate(tokens):
            if word == target:
                found.append({"corpus": corpus_label, "doc_id": doc["doc_id"],
                              "position_0based": i,
                              "left": " ".join(tokens[max(0, i - window):i]),
                              "node": word,
                              "right": " ".join(tokens[i + 1:i + window + 1])})
    return found


def write_csv(path: Path, rows: list[dict[str, object]], columns: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def run(focus_path: Path, reference_path: Path, output_dir: Path, *,
        query: str, window: int = 4, fold_alef: bool = False) -> dict[str, int]:
    focus = read_documents(focus_path)
    reference = read_documents(reference_path)
    focus_counts = count_tokens(focus, fold_alef=fold_alef)
    reference_counts = count_tokens(reference, fold_alef=fold_alef)
    comparison = keyness_rows(focus_counts, reference_counts)
    concordance = kwic_rows(focus, query, corpus_label="focus", window=window,
                            fold_alef=fold_alef)
    concordance += kwic_rows(reference, query, corpus_label="reference",
                             window=window, fold_alef=fold_alef)
    output_dir.mkdir(parents=True, exist_ok=True)
    columns_freq = ["word", "count", "per_10000"]
    write_csv(output_dir / "focus_frequencies.csv", frequency_rows(focus_counts), columns_freq)
    write_csv(output_dir / "reference_frequencies.csv", frequency_rows(reference_counts), columns_freq)
    write_csv(output_dir / "keyness.csv", comparison, [
        "word", "focus_count", "reference_count", "focus_per_10000",
        "reference_per_10000", "g2", "p_chi2_approx",
        "bh_q_exploratory", "log2_rate_ratio_adjusted", "direction"])
    write_csv(output_dir / "kwic.csv", concordance,
              ["corpus", "doc_id", "position_0based", "left", "node", "right"])
    return {"focus_documents": len(focus), "reference_documents": len(reference),
            "focus_tokens": sum(focus_counts.values()),
            "reference_tokens": sum(reference_counts.values()),
            "tested_word_types": len(comparison), "kwic_hits": len(concordance)}


def main() -> None:
    parser = argparse.ArgumentParser(description="Synthetic Arabic corpus analysis: frequency, keyness, KWIC")
    parser.add_argument("--focus", type=Path, default=HERE / "data" / "focus.csv")
    parser.add_argument("--reference", type=Path, default=HERE / "data" / "reference.csv")
    parser.add_argument("--output", type=Path, default=HERE / "outputs")
    parser.add_argument("--query", default="البيانات", help="Exact single surface-word for KWIC")
    parser.add_argument("--window", type=int, default=4, help="Context tokens on each side")
    parser.add_argument("--fold-alef", action="store_true",
                        help="Optional: merge آ/أ/إ/ٱ into ا; preserve distinctions by default")
    args = parser.parse_args()
    summary = run(args.focus, args.reference, args.output,
                  query=args.query, window=args.window, fold_alef=args.fold_alef)
    print("\n".join(f"{k}: {v}" for k, v in summary.items()))

if __name__ == "__main__":
    main()
