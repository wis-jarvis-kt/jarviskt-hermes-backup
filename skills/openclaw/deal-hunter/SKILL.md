---
name: deal-hunter
description: >
  Hunt for the best flight and hotel deals across multiple platforms (Skyscanner,
  Google Flights, Airpaz, AirAsia, Agoda, Booking.com, Hotels.com). Trigger when
  Master KT mentions flights, hotels, travel deals, or asks to find the cheapest
  way to get somewhere. Compares across sources and returns the best options with
  direct booking links.
---

# Deal Hunter — Flight & Hotel Comparison Skill

## Trigger Phrases
- "find me flights to [place]"
- "cheapest flight from [origin] to [destination]"
- "I want to go to [place]"
- "find me a hotel in [place]"
- "plan a trip to [place]"
- "any deals to [place]"
- "how much to fly to [place]"
- Any mention of travel dates + destination

## Default Assumptions (for Master KT)
- **Origin:** Kuala Lumpur (KUL / KLIA or KLIA2)
- **Currency:** MYR
- **Preferred airlines:** AirAsia (budget), MAS/MASwings, Batik Air — check all
- **Preferred OTAs:** Agoda (hotels), Airpaz (flights), Skyscanner
- **Travellers:** Ask if not stated — assume 2 pax (KT + 1) unless told otherwise
- **Class:** Economy unless stated otherwise

## Workflow

### Step 1 — Parse the request
Extract:
- Origin (default: KUL)
- Destination (city + country)
- Dates (exact or flexible: "end of April", "sometime in June")
- Duration / return date
- Number of travellers
- Budget if stated
- Flights only / hotels only / both

### Step 2 — Search Flights (run all in parallel via web_search)

Search the following and extract best prices:

**a) Skyscanner**
- URL pattern: `https://www.skyscanner.com.my/transport/flights/{ORIGIN}/{DEST}/{DATE}/`
- Web search query: `site:skyscanner.com.my flights {ORIGIN} to {DESTINATION} {DATE}`
- Also: `skyscanner cheapest flights {ORIGIN} {DESTINATION} {MONTH}`

**b) Google Flights**
- Web search query: `google flights {ORIGIN} to {DESTINATION} {DATE} cheapest`
- Look for price calendar mentions in results

**c) Airpaz**
- Web search query: `airpaz cheapest flight {ORIGIN} {DESTINATION} {DATE}`
- URL: `https://www.airpaz.com/en/flight?org={IATA_ORIGIN}&dst={IATA_DEST}&type=oneway&date={DATE}&pax=1`

**d) AirAsia**
- Web search query: `airasia cheapest flight {ORIGIN} {DESTINATION} {MONTH} {YEAR}`
- URL: `https://www.airasia.com/flights/search?origin={IATA_ORIGIN}&destination={IATA_DEST}&departDate={DATE}`

**e) Direct airline sites** (if relevant route)
- MAS/Malaysia Airlines: `malaysiaairlines.com`
- Batik Air: `batikair.com`
- Firefly: `fireflyz.com.my`

**f) Booking aggregators**
- Kayak: `kayak.com.my`
- Trip.com: `trip.com`

### Step 3 — Search Hotels (run in parallel)

**a) Agoda**
- Web search: `agoda best deal hotel {DESTINATION} {CHECKIN} {NIGHTS} nights`
- Look for: star rating, review score, price per night, location

**b) Booking.com**
- Web search: `booking.com hotel {DESTINATION} {CHECKIN} {NIGHTS} nights cheapest highly rated`

**c) Hotels.com**
- Web search: `hotels.com {DESTINATION} {CHECKIN} deals`

**d) Airbnb** (if destination suits it)
- Web search: `airbnb {DESTINATION} {CHECKIN} {NIGHTS} cheap`

**e) Cross-check**
- Also search: `cheapest hotel {DESTINATION} {DATE} {NIGHTS} nights Malaysia booking`

### Step 4 — Compare & Rank

**Flights — present as:**
```
✈️ FLIGHT OPTIONS: {ORIGIN} → {DESTINATION} | {DATE}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🥇 BEST DEAL
   Airline: [name]
   Price: RM [X] per pax | RM [total] for [N] pax
   Depart: [time] | Arrive: [time] | Duration: [Xh Xm]
   Stops: [direct/1 stop via X]
   Book: [direct link]
   Source: [Skyscanner/Airpaz/etc]

🥈 2ND OPTION
   ...

🥉 3RD OPTION
   ...

💡 TIPS:
- [Flexible date tip if applicable]
- [Cheapest day of week if known]
- [Alert if price is unusually good]
```

**Hotels — present as:**
```
🏨 HOTEL OPTIONS: {DESTINATION} | {CHECKIN} – {CHECKOUT} ({N} nights)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🥇 BEST VALUE
   Name: [Hotel name]
   Stars: ⭐⭐⭐⭐
   Rating: [X.X/10] ([N] reviews)
   Price: RM [X]/night | RM [total] total
   Location: [area/distance from centre]
   Includes: [breakfast/wifi/pool]
   Book: [direct link]
   Source: [Agoda/Booking.com/etc]

🥈 BEST LOCATION
   ...

🥉 BUDGET PICK
   ...
```

### Step 5 — Final Summary

```
🎯 DEAL HUNTER SUMMARY
Trip: {ORIGIN} → {DESTINATION}
Dates: {dates}
Pax: {N}

✈️ Cheapest flight: RM [X] total ([source])
🏨 Best hotel: RM [X]/night ([source])
💰 Estimated total: RM [X] – RM [Y]

⚡ Best combo deal found: [if any package deal spotted]
🔗 Quick links:
- Skyscanner: [link]
- Agoda: [link]
- Airpaz: [link]
```

## Flexible Date Handling

If user gives vague dates ("end of April", "sometime in June"):
- Search for the full date range (e.g., Apr 25–30)
- Report which specific dates are cheapest
- Flag: "Flying on [DAY] instead of [DAY] saves RM X"

## Deal Alert Rules

Flag these as 🚨 HOT DEAL:
- Flight price >30% below typical route average
- Hotel price >40% below normal for that star rating
- Flash sales spotted on AirAsia/Agoda

## Notes
- Always check if KLIA2 vs KLIA matters for the airline (AirAsia = KLIA2)
- For short trips (<4h flight), budget airline usually wins
- For overnight flights, comfort matters — mention seat pitch if found
- Hotel: prioritize properties with free cancellation when prices are similar
- Always mention if prices are one-way or return
