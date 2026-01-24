# PROJECT: F1 "Weekend-Accumulator" Strategy Engine 

Algorithm decides the winner based on four weighted layers.

Layer 1: The "Qualifying Anchor" (Base Pace)
The Logic: The model assumes Qualifying is the only "true" test of car speed, free from fuel/tyre management.

The Math: RacePace = PoleTime + 5.0s + DeltaToPole

The Effect: If Lando Norris qualifies P1 and Max Verstappen qualifies P2 (+0.2s), the model starts the race assuming Lando is 0.2s per lap faster.

Critique: This is the model's biggest weakness. In reality, cars like the Red Bull are often setup for Race Pace, meaning they are faster on Sunday than Saturday. The model struggles to see this.

Layer 2: The "Elite Tier" Buff (Tyre Management)
The Logic: Top teams don't just drive fast; they consume tyres slower.

The Coefficient: -0.2s per lap pace bonus.

Who gets it: VER, NOR, PIA, LEC, HAM, RUS, SAI.

The Effect: This effectively kills the chances of mid-field teams (Aston Martin, Alpine) winning, even if they qualify P3. This corrects the "Fernando Alonso / George Russell Glory Run" anomalies from earlier versions.

Layer 3: The "Max Factor" (Driver Skill)
The Logic: Max Verstappen and Lando Norris are currently statistically superior at delivering consistent lap times without mistakes.

The Coefficients:

Max (VER): -0.1s Pace Bonus, 0.2 Consistency Variance (Low Variance).

Lando (NOR): -0.05s Pace Bonus, 0.25 Consistency Variance.

The Effect: This is the "Tie Breaker." If Max and Charles Leclerc have the exact same car performance, the model hands the win to Max because of this -0.1s constant.

Layer 4: The "Hunter" Logic (Overtaking)
The Logic: Starting P10 at Monaco is a death sentence. Starting P10 at Spa is just a minor inconvenience.

The Math: TrafficDrag = (GridPos * 0.5) * PassDifficulty

The Hunter Bonus: If the driver is Elite (Tier 1), the PassDifficulty is halved.

The Effect:

At Monaco (Diff 0.95), starting P5 adds 2.3s of drag. Impossible to win.

At Spa (Diff 0.2), starting P5 adds only 0.5s of drag. Max Verstappen (Hunter) reduces this to 0.25s. He can easily win from P5.

## How to run
python f1_predictor_v10.py --year 2025 --gp "Australia" --session Q

```
python -c "import fastf1; print(fastf1.get_event_schedule(2025)[['RoundNumber', 'Country', 'EventName']].to_string())"
```

## Testing Algorithm Accuracy using 2025

| Round | Country              | Event Name                | Actual Winner | Predicted Winner | Whether algorithm was correct or not |
|------:|----------------------|---------------------------|---------------|------------------|---------|
|     1 | Australia            | Australian Grand Prix     |      Lando > Max > George         |                  |         |
|     2 | China                | Chinese Grand Prix        |         Oscar > Lando > George      |                  |         |
|     3 | Japan                | Japanese Grand Prix       |       Max > Lando > Oscar       |                  |         |
|     4 | Bahrain              | Bahrain Grand Prix        |        Oscar > George > Lando       |                  |         |
|     5 | Saudi Arabia         | Saudi Arabian Grand Prix  |       Oscar > Max > Charles        |                  |         |
|     6 | United States        | Miami Grand Prix          |       Oscar > Lando > George        |                  |         |
|     7 | Italy                | Emilia Romagna Grand Prix |       Max > Lando > Oscar        |                  |         |
|     8 | Monaco               | Monaco Grand Prix         |       Lando > Charles > Oscar        |                  |         |
|     9 | Spain                | Spanish Grand Prix        |       Oscar > Lando > Charles        |                  |         |
|    10 | Canada               | Canadian Grand Prix       |      George > Max > Kimi         |                  |         |
|    11 | Austria              | Austrian Grand Prix       |      Lando > Oscar > Charles         |                  |         |
|    12 | United Kingdom       | British Grand Prix        |   Lando > Oscar > Nico            |                  |         |
|    13 | Belgium              | Belgian Grand Prix        |     Oscar > Lando > Charles          |                  |         |
|    14 | Hungary              | Hungarian Grand Prix      |      Lando > Oscar > George         |                  |         |
|    15 | Netherlands          | Dutch Grand Prix          |      Oscar > Max > Issac         |                  |         |
|    16 | Italy                | Italian Grand Prix        |       Max > Lando > Oscar        |                  |         |
|    17 | Azerbaijan           | Azerbaijan Grand Prix     |       Max > George > Carlos        |                  |         |
|    18 | Singapore            | Singapore Grand Prix      |         George > Max > Lando      |                  |         |
|    19 | United States        | United States Grand Prix  |        Max > Lando > Charles       |                  |         |
|    20 | Mexico               | Mexico City Grand Prix    |        Lando > Charles > Max       |                  |         |
|    21 | Brazil               | São Paulo Grand Prix      |   Lando > Kimi > Max            |                  |         |
|    22 | United States        | Las Vegas Grand Prix      |       Max > George > Kimi        |                  |         |
|    23 | Qatar                | Qatar Grand Prix          |        Max > Oscar > Carlos       |                  |         |
|    24 | United Arab Emirates | Abu Dhabi Grand Prix      |        Max > Oscar > Lando       |                  |         |


