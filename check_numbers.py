import sys
from datetime import date

SPEC = {
    "social": 1334, "web": 1158, "unique": 2070, "web_shown": 736,
    "threats": 1753, "noise": 0.67, "ignore_share": 0.04,
    "escalated_kpi": 31, "escalated_bar": 2, "escalated_panel": 2,
    "brief_promised": 3, "brief_shown": 2,
    "per_competitor": [318, 245, 210, 154, 112, 96, 89, 74, 67, 61, 53, 38],
    "competitors_claimed": 14, "graph_nodes": 7,
    "window": (date(2026, 8, 20), date(2026, 9, 27)),
    "output_tokens": 24849, "week_spend": 0.2087,
}

ASSUMPTIONS = {
    "input_tokens_per_signal": 1000,
    "input_price_per_m": 0.10,
    "spend_tolerance": 0.002,
}

ASSUMPTION_NOTES = [
    "F01: duplicates are raw (social + web) minus unique; the spec gives no dedup rule.",
    "F02: 'noise' is a share of unique signals, so threats must fit in what is left.",
    "F07, F08: ~1,000 input tokens per signal is our estimate, not a number in the spec.",
    "F08: $0.10 per million input tokens is the classifier price the spec quotes; output and brief costs have no price in the spec, so the weekly spend can never be fully verified here.",
]


def mark(ok):
    return "✓" if ok else "✗"


def share(part, whole):
    return f"{part / whole:.1%}" if whole else "n/a (division by zero)"


def checks(spec=SPEC, assume=ASSUMPTIONS):
    s, a = spec, assume
    raw = s["social"] + s["web"]
    dupes = raw - s["unique"]
    web_cut = s["web"] - s["web_shown"]
    social_cut = s["social"] - (s["unique"] - s["web_shown"])
    yield "F01", "!" if social_cut == 0 and web_cut else "✓", f"{s['social']} + {s['web']} = {raw} raw, {s['unique']} unique: {dupes} duplicates ({share(dupes, raw)}), all of them web ({share(web_cut, s['web'])} of web), none social"

    not_noise_max = round(s["unique"] * (1 - s["noise"]))
    yield "F02", mark(s["threats"] <= not_noise_max), f"{s['threats']} threats = {share(s['threats'], s['unique'])} of signals, but {s['noise']:.0%} noise leaves at most {not_noise_max} non-noise"

    yield "F03", mark(abs(s["noise"] - s["ignore_share"]) < 0.01), f"noise KPI {s['noise']:.0%} vs 'ignore' label {s['ignore_share']:.0%} in the taxonomy"

    same = s["escalated_kpi"] == s["escalated_bar"] == s["escalated_panel"] and s["brief_promised"] == s["brief_shown"]
    yield "F04", mark(same), f"escalated: {s['escalated_kpi']} (KPI) / {s['escalated_bar']} (bar) / {s['escalated_panel']} (panel); brief promises {s['brief_promised']} actions, shows {s['brief_shown']}"

    listed = sum(s["per_competitor"])
    missing = s["unique"] - listed
    ok = listed == s["unique"] and len(s["per_competitor"]) == s["competitors_claimed"] == s["graph_nodes"]
    yield "F05", mark(ok), f"{len(s['per_competitor'])} of {s['competitors_claimed']} competitors listed, sum {listed}: {missing} signals ({share(missing, s['unique'])}) unaccounted; graph draws {s['graph_nodes']}"

    start, end = s["window"]
    days = (end - start).days
    yield "F06", mark(days == 7), f"'weekly' window {start:%d %b} - {end:%d %b} = {days} days"

    input_tokens = s["unique"] * a["input_tokens_per_signal"]
    yield "F07", mark(s["output_tokens"] >= input_tokens), f"'tokens processed' {s['output_tokens']:,} counts output only; input ~{input_tokens:,} is {share(input_tokens, input_tokens + s['output_tokens'])} of all tokens"

    input_cost = input_tokens / 1e6 * a["input_price_per_m"]
    spend = s["week_spend"]
    if spend < input_cost - a["spend_tolerance"]:
        verdict, why = "✗", "below the classifier input cost alone"
    elif abs(spend - input_cost) <= a["spend_tolerance"]:
        verdict, why = "!", "classifier input only; output and brief costs missing"
    else:
        verdict, why = "!", "above input cost; the rest has no price in the spec, so it cannot be checked"
    yield "F08", verdict, f"week spend ${spend} vs {input_tokens / 1e6:.2f}M input tokens x ${a['input_price_per_m']}/M = ${input_cost:.4f}: {why}"


def main(argv=sys.argv[1:]):
    if "--assumptions" in argv:
        for note in ASSUMPTION_NOTES:
            print(f"- {note}")
        return 0
    results = list(checks())
    for fid, m, msg in results:
        print(f"{m} {fid}  {msg}")
    wrong = sum(m == "✗" for _, m, _ in results)
    unclear = sum(m == "!" for _, m, _ in results)
    print(f"{wrong} contradictions, {unclear} unexplained, {len(results) - wrong - unclear} ok")
    print("assumptions behind F01, F02, F07 and F08: python3 check_numbers.py --assumptions")
    return 1 if wrong or unclear else 0


if __name__ == "__main__":
    sys.exit(main())
