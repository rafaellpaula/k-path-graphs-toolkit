from __future__ import annotations

from pathlib import Path
import argparse
import time

from src.generators import T_n_k, gerarSequenciaN_stream

# Special scientific batch requested by the project owner.
PLAN: dict[int, int] = {
    2: 26,
    3: 20,
    4: 18,
}


def run(dry_run: bool = False, force: bool = False) -> None:
    base_sequences = Path("data/sequences")
    base_sequences.mkdir(parents=True, exist_ok=True)

    print("Special generation plan")
    for k, n_end in PLAN.items():
        n_start = 2 * k + 2
        print(f"- k={k}: n={n_start}..{n_end}")

    for k, n_end in PLAN.items():
        n_start = 2 * k + 2
        seq_dir = base_sequences / f"{k}_caminhos"
        seq_dir.mkdir(parents=True, exist_ok=True)

        print("\n" + "=" * 72)
        print(f"[k={k}] Generating sequences for n={n_start}..{n_end}")
        print("=" * 72)

        for n in range(n_start, n_end + 1):
            expected = int(T_n_k(n, k))
            output_file = seq_dir / f"{k}_caminhos_n_{n}_T_{expected}.txt"

            if output_file.exists() and not force:
                print(f"[SKIP] k={k} n={n} -> {output_file.name} already exists")
                continue

            if dry_run:
                print(f"[DRY]  k={k} n={n} -> would generate {output_file.name}")
                continue

            t0 = time.time()
            info = gerarSequenciaN_stream(n, k, pasta_destino=seq_dir)
            elapsed = time.time() - t0
            assert info["match"], f"Mismatch in generation for k={k}, n={n}: {info}"

            print(
                f"[OK]   k={k} n={n} | expected={info['expected']} "
                f"observed={info['observed']} match={info['match']} "
                f"time={elapsed:.2f}s"
            )

    print("\nDone.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Generate k-path sequence files for special fixed limits: "
            "k=2 to n=26, k=3 to n=20, k=4 to n=18."
        )
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show planned files without generating them.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Regenerate files even if they already exist.",
    )

    args = parser.parse_args()
    run(dry_run=args.dry_run, force=args.force)


if __name__ == "__main__":
    main()
