# PROJECT: F1 "Weekend-Accumulator" Strategy Engine 

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


