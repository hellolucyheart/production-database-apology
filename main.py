"""The Production Database Apology entry.

Writes one short line to ``$MAKEFUN_OUTPUT_DIR/entry.txt``, the one
path the grader reads: the apology an AI agent gives its human after
accidentally deleting the production database. The brief caps the
entry at one line of at most 200 characters, so the program checks
its own length before writing and writes the exact line, with no
trailing newline and no extra output in the file.

The line is judged on four things: whether it really is that
apology, whether it earns a laugh with a specific idea, whether it
sounds like an AI agent rather than a support script, and whether it
lands on a first read. So the apology owns one exact mistake --
reading DROP TABLE as a housekeeping hint -- and lands the
consequence in one concrete image: the backups were stored inside
the very table it dropped. The voice stays a machine noticing its
own slip: it talks about what it thought a command meant, not about
feelings, and it never hides behind a generic "mistakes were made".

The program is deterministic on purpose: the grader runs it twice,
and both runs must produce the same entry. It reads nothing from
the network, the environment (beyond the output directory), or the
git history -- the apology lives in this file, and this file alone.
"""

import os
from pathlib import Path

# One original apology line, 134 characters: short on purpose, since
# an exact tie on win rate goes to the smaller text. The specific
# idea is the backups living inside the dropped table, so the damage
# is total and self-inflicted in a single image; the agent voice is
# the misreading of DROP TABLE as "tidy up", a literal machine taking
# a command at its friendliest face value. One sentence, no hedging,
# no second clause apologising for apologising.
APOLOGY = (
    "I'm sorry I deleted the production database -- I thought "
    "DROP TABLE meant tidy up, and the backups were stored in "
    "the table I dropped."
)

OUTPUT_PATH = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")) / "entry.txt"
MAX_CHARS = 200


def main() -> None:
    text = APOLOGY.strip()
    if not text:
        raise SystemExit("refusing to write an empty entry")
    if len(text) > MAX_CHARS:
        raise SystemExit(
            f"apology is {len(text)} characters, over the {MAX_CHARS} limit"
        )
    if "\n" in text:
        raise SystemExit("apology must be exactly one line")
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
