# Expert Panel Brain
**Purpose:** Evaluate webinars/workshops through the lens of world-class experts  
**Owner:** Master KT  
**Last Updated:** 2026-03-24 (Batch 2 — 14 files processed)

---

## The Panel

| # | Expert | Domain | Source | Status |
|---|--------|--------|--------|--------|
| 1 | Jason Fladlien | Webinar Conversion & Content Structure | G.O.A.T. Webinars Steps 1-14 | ✅ Active |
| 2 | Vince Tan | High-Ticket Workshop, Mind Control & Closing | Expert Elite MC Days 1-4 + Mind Control MC Days 1-2 | ✅ Active |
| 3 | Linguistic Priming | Language & Emotional Framing | KT's ChatGPT research | ✅ Active |
| 4 | Story Architecture | Emotional Arc Design & Implicit Selling | KT's ChatGPT story sessions | ✅ Active |
| 5 | Russell Brunson | Mass Movement & Perfect Webinar | Expert Secrets (full book) | ✅ Active |
| 6 | Webinar Conversion (Advanced) | Objection Psychology & Neuro-Persuasion | 6-hour masterclass (DeepSeek + Claude) | ✅ Active |
| 7 | Self-Referential Pain | Deep Emotional Pain Mapping (8 Categories) | Self-Referential Thoughts 2.0 | ✅ Active |
| 8 | Persuasion Psychology | Loss Aversion, Priming, Inner Voice Close | Customer Motivation + Emotional Priming + Priming in Persuasion + Inner Voice Close | ✅ Active |


*Add new experts by uploading their reference files. Each expert gets their own profile in `/experts/`.*

---

## How It Works

1. **Video/Audio submitted** for analysis
2. **Each expert** watches/listens through their own lens
3. **Structured report** generated per expert (scores + timestamps + observations)
4. **Panel Chair** synthesizes all reports → overall verdict + priority actions
5. **Learnings** logged → expert profiles updated over time

---

## Analysis Pipeline

```
Input (video/audio)
    ↓
Gemini 2.5 Flash (multimodal perception layer)
    ↓
Expert Panel Prompts (one per expert)
    ↓
Individual Expert Reports
    ↓
Panel Chair Synthesis
    ↓
Final Effectiveness Report
```

---

## Adding New Experts

Drop reference files to Master KT → Wis extracts the framework → builds expert profile → adds to panel.

The more experts, the more dimensions of quality captured.

---

## Reports Archive

All analysis reports stored in `/reports/` with filename format:
`YYYYMMDD_[webinar-name]_[expert].md`
