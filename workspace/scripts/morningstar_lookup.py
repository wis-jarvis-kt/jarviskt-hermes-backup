#!/usr/bin/env python3
"""
Morningstar Stock Lookup via mstarpy
Usage: python3 morningstar_lookup.py AAPL
       python3 morningstar_lookup.py NVDA --full
"""

import sys
import json
import argparse
import mstarpy as ms


def flatten_rows(rows, depth=0):
    """Recursively flatten nested subLevel rows into (label, datum) list."""
    result = []
    for row in rows:
        label = row.get("label", "")
        datum = row.get("datum", [])
        result.append((label, datum, depth))
        sub = row.get("subLevel", [])
        if isinstance(sub, list):
            result.extend(flatten_rows(sub, depth + 1))
    return result


def fmt_val(v):
    if v is None or v in ("null", "_PO_"):
        return "N/A"
    try:
        return f"{float(v):>10,.1f}"
    except:
        return str(v)


def print_section(title, data, key_labels=None, col_count=4):
    if isinstance(data, str):
        print(f"  {title}: {data}")
        return
    try:
        cols = data.get("columnDefs", [])
        rows = data.get("rows", [])
        currency = data.get("footer", {}).get("currency", "")
        magnitude = data.get("footer", {}).get("orderOfMagnitude", "")

        display_cols = cols[-col_count:] if len(cols) >= col_count else cols
        col_indices = [cols.index(c) for c in display_cols if c in cols]

        print(f"\n{title} ({', '.join(display_cols)})" + (f" [{currency} {magnitude}]" if currency else "") + ":")

        all_rows = flatten_rows(rows)
        for label, datum, depth in all_rows:
            if key_labels and not any(k.lower() in label.lower() for k in key_labels):
                continue
            vals = [fmt_val(datum[i] if i < len(datum) else None) for i in col_indices]
            indent = "  " + ("  " * depth)
            print(f"{indent}{label:<35} {' | '.join(vals)}")
    except Exception as e:
        print(f"  [parse error: {e}]")


def print_valuation(stock):
    try:
        data = stock.valuation()
    except Exception as e:
        print(f"  Valuation: [unavailable: {e}]")
        return

    try:
        rows = data["Collapsed"]["rows"]
        cols = data["Collapsed"]["columnDefs"]
        display_cols = cols[-4:] if len(cols) >= 4 else cols
        col_indices = [cols.index(c) for c in display_cols if c in cols]

        print(f"\n💰 Valuation Ratios ({', '.join(display_cols)}):")
        for row in rows:
            label = row.get("label", "")
            datum = row.get("datum", [])
            vals = []
            for i in col_indices:
                v = datum[i] if i < len(datum) else None
                try:
                    vals.append(f"{float(v):>8.2f}" if v and str(v) not in ("null", "None") else "     N/A")
                except:
                    vals.append("     N/A")
            print(f"  {label:<22} {' | '.join(vals)}")
    except Exception as e:
        print(f"  [valuation parse error: {e}]")


def lookup_stock(ticker: str, full: bool = False):
    print(f"\n📊 Morningstar: {ticker.upper()}\n{'='*55}")

    try:
        stock = ms.Stock(ticker, language="en-gb")
        print(f"✅ {stock.name} ({ticker.upper()})")
    except Exception as e:
        print(f"❌ Could not find stock '{ticker}': {e}")
        sys.exit(1)

    # Always show valuation
    print_valuation(stock)

    if full:
        # Income Statement
        try:
            d = stock.incomeStatement()
            print_section(
                "📋 Income Statement",
                d,
                key_labels=["Total Revenue", "Gross Profit", "Operating Income",
                             "Net Income", "EPS", "EBITDA"]
            )
        except Exception as e:
            print(f"  [income-statement error: {e}]")

        # Balance Sheet
        try:
            d = stock.balanceSheet()
            print_section(
                "🏦 Balance Sheet",
                d,
                key_labels=["Total Assets", "Total Liabilities", "Total Equity",
                             "Cash", "Long-Term Debt", "Short-Term Debt"]
            )
        except Exception as e:
            print(f"  [balance-sheet error: {e}]")

        # Free Cash Flow (uses freeCashFlow method — cleaner data)
        try:
            d = stock.freeCashFlow()
            items = d.get("dataList", [])[-5:]  # last 5 years
            currency = d.get("currency", "USD")
            print(f"\n💵 Free Cash Flow ({currency}):")
            print(f"  {'Year':<10} {'OpCF Growth%':>14} {'FCF Growth%':>12} {'FCF/Sales%':>12} {'FCF/NetIncome':>14}")
            print(f"  {'-'*65}")
            for item in items:
                yr = item.get("fiscalPeriodYearMonth", "")[:7]
                ocfg = item.get("operatingCFGrowthPer")
                fcfg = item.get("freeCashFlowGrowthPer")
                fcfs = item.get("freeCFPerSales")
                fcfni = item.get("freeCashFlowPerNetIncome")
                def fv(v): return f"{v:>+.1f}" if v is not None else "  N/A"
                def fp(v): return f"{v:>8.2f}" if v is not None else "    N/A"
                print(f"  {yr:<10} {fv(ocfg):>14} {fv(fcfg):>12} {fp(fcfs):>12} {fp(fcfni):>14}")
        except Exception as e:
            print(f"  [cash-flow error: {e}]")

    print("\n✅ Done.\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Morningstar stock lookup via mstarpy")
    parser.add_argument("ticker", help="Stock ticker symbol (e.g. AAPL, NVDA, TSLA)")
    parser.add_argument("--full", action="store_true",
                        help="Include income statement, balance sheet, cash flow")
    args = parser.parse_args()
    lookup_stock(args.ticker.upper(), full=args.full)
