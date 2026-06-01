# PubMed EUtils API — Research via Curl

Quick and reliable alternative to browser-based PubMed searches. Bypasses anti-bot blocks that plague browser navigation to NCBI.

## Core Endpoints

### ESearch — find PMIDs by topic
```bash
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=TOPIC&retmax=5&retmode=json"
```
Returns JSON with `idlist` of PMIDs. Parse with `python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('esearchresult',{}).get('idlist',[]))"`

### EFetch — retrieve abstracts by PMID
```bash
# Multiple IDs at once
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=PMID1,PMID2,PMID3&rettype=abstract&retmode=text"

# Single PMID
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=15936542&rettype=abstract&retmode=text"
```
Returns plain text abstracts, one per PMID. Works reliably in cron jobs.

### Combined workflow
```bash
# Step 1: Search for IDs
IDS=$(curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=11-beta-HSD1+visceral+fat&retmax=3&retmode=json" | python3 -c "import json,sys; d=json.load(sys.stdin); print(','.join(d.get('esearchresult',{}).get('idlist',[])))")

# Step 2: Fetch abstracts
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=$IDS&rettype=abstract&retmode=text"
```

## Search Query Syntax
- `TOPIC` → basic search
- `TOPIC[tiab]` → title/abstract only
- `TOPIC[mesh]` → MeSH terms
- `PMID[pmid]` → exact PMID lookup
- `TOPIC1+AND+TOPIC2` → AND
- `TOPIC1+OR+TOPIC2` → OR
- `TOPIC1+NOT+TOPIC2` → NOT

## Limits
- `retmax=5` default, increase for broader results
- No API key needed for basic use; rate-limited to ~3 req/sec without key
- Large responses truncate at stdout limits (~50KB)

## Verified queries from this session
| Query | IDs returned |
|-------|-------------|
| `11-beta-HSD1+visceral+fat` | 38791098, 31696216, 29225114, 28619249, 27715400 |
| `diaphragmatic+breathing+cortisol+stress+randomized` | 41984428, 40868462, 40792649, 40485947, 39543797 |
| `colon+massage+abdominal+massage+constipation` | 41919979, 41792381, 41288808, 39531948, 38720481 |

## Notes
- The `rettype=abstract&retmode=text` format gives clean plain text — easy to grep
- Abstracts often reveal that cited PMIDs don't support the claims made (as with the Instagram post's wrong citations)
- Very useful for fact-checking health/medical claims on social media by looking up actual paper content