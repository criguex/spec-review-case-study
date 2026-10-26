import sys
from datetime import date

SOCIAL, WEB, UNIQUE, WEB_SHOWN = 1334, 1158, 2070, 736
THREATS, NOISE, IGNORE_SHARE = 1753, 0.67, 0.04
ESCALATED_KPI, ESCALATED_BAR, ESCALATED_PANEL = 31, 2, 2
BRIEF_PROMISED, BRIEF_SHOWN = 3, 2
PER_COMPETITOR = [318, 245, 210, 154, 112, 96, 89, 74, 67, 61, 53, 38]
COMPETITORS_CLAIMED, GRAPH_NODES = 14, 7
WINDOW = (date(2026, 8, 20), date(2026, 9, 27))
OUTPUT_TOKENS, INPUT_TOKENS_PER_SIGNAL = 24849, 1000
WEEK_SPEND, INPUT_PRICE_PER_M = 0.2087, 0.10


def mark(ok):
    return "✓" if ok else "✗"


def checks():
    raw = SOCIAL + WEB
    dupes = raw - UNIQUE
    web_cut = WEB - WEB_SHOWN
    social_cut = SOCIAL - (UNIQUE - WEB_SHOWN)
    yield "F01", "!" if social_cut == 0 and web_cut else "✓", f"{SOCIAL} + {WEB} = {raw} raw, {UNIQUE} unique: {dupes} duplicates ({dupes / raw:.1%}), all of them web ({web_cut / WEB:.1%} of web), none social"

    not_noise_max = round(UNIQUE * (1 - NOISE))
    yield "F02", mark(THREATS <= not_noise_max), f"{THREATS} threats = {THREATS / UNIQUE:.1%} of signals, but {NOISE:.0%} noise leaves at most {not_noise_max} non-noise"

    yield "F03", mark(abs(NOISE - IGNORE_SHARE) < 0.01), f"noise KPI {NOISE:.0%} vs 'ignore' label {IGNORE_SHARE:.0%} in the taxonomy"

    same = ESCALATED_KPI == ESCALATED_BAR == ESCALATED_PANEL and BRIEF_PROMISED == BRIEF_SHOWN
    yield "F04", mark(same), f"escalated: {ESCALATED_KPI} (KPI) / {ESCALATED_BAR} (bar) / {ESCALATED_PANEL} (panel); brief promises {BRIEF_PROMISED} actions, shows {BRIEF_SHOWN}"

    listed = sum(PER_COMPETITOR)
    missing = UNIQUE - listed
    ok = listed == UNIQUE and len(PER_COMPETITOR) == COMPETITORS_CLAIMED == GRAPH_NODES
    yield "F05", mark(ok), f"{len(PER_COMPETITOR)} of {COMPETITORS_CLAIMED} competitors listed, sum {listed}: {missing} signals ({missing / UNIQUE:.0%}) unaccounted; graph draws {GRAPH_NODES}"

    days = (WINDOW[1] - WINDOW[0]).days
    yield "F06", mark(days == 7), f"'weekly' window {WINDOW[0]:%d %b} - {WINDOW[1]:%d %b} = {days} days"

    input_tokens = UNIQUE * INPUT_TOKENS_PER_SIGNAL
    share_in = input_tokens / (input_tokens + OUTPUT_TOKENS)
    yield "F07", mark(OUTPUT_TOKENS >= input_tokens), f"'tokens processed' {OUTPUT_TOKENS:,} counts output only; input ~{input_tokens:,} is {share_in:.0%} of all tokens"

    input_cost = input_tokens / 1e6 * INPUT_PRICE_PER_M
    covers_input_only = abs(WEEK_SPEND - input_cost) < 0.002
    yield "F08", "!" if covers_input_only else "✓", f"week spend ${WEEK_SPEND} ~ {input_tokens / 1e6:.2f}M input tokens x ${INPUT_PRICE_PER_M}/M = ${input_cost:.4f}: classifier input only"


def main():
    results = list(checks())
    for fid, m, msg in results:
        print(f"{m} {fid}  {msg}")
    wrong = sum(m == "✗" for _, m, _ in results)
    unclear = sum(m == "!" for _, m, _ in results)
    print(f"{wrong} contradictions, {unclear} unexplained, {len(results) - wrong - unclear} ok")
    return 1 if wrong or unclear else 0


if __name__ == "__main__":
    sys.exit(main())
