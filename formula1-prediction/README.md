# 🏎️ F1 Race Winner Predictor

> **A Monte Carlo simulation engine that predicts Formula 1 race winners using qualifying data and track-specific physics.**

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastF1](https://img.shields.io/badge/FastF1-3.3+-green.svg)

---

## 📋 Table of Contents

- [How It Works](#-how-it-works)
- [Installation](#-installation)
- [Usage](#-usage)
- [Benchmarking](#-benchmarking)
- [Historical Results](#-historical-results)
- [Algorithm Details](#-algorithm-details)

---

## 🧠 How It Works

The algorithm predicts race winners using **four weighted layers** combined with **Monte Carlo simulation** (5,000 runs).

### Layer 1: Qualifying Anchor (Base Pace)

Qualifying is treated as the purest test of car speed (no fuel/tyre management).

```
RacePace = PoleTime + 5.0s + DeltaToPole
```

**Example:** If Norris qualifies P1 and Verstappen qualifies P2 (+0.2s), the model assumes Norris is 0.2s/lap faster.

### Layer 2: Elite Tier Buff (Tyre Management)

Top teams consume tyres slower, giving them a pace advantage.

| Drivers with Buff | Pace Bonus |
|-------------------|------------|
| VER, NOR, PIA, LEC, HAM, RUS, SAI | -0.2s/lap |

### Layer 3: Driver Skill Factor

Elite drivers deliver more consistent lap times with fewer mistakes.

| Driver | Pace Bonus | Consistency Variance |
|--------|------------|---------------------|
| VER (Verstappen) | -0.1s | 0.2 (very low) |
| NOR (Norris) | -0.05s | 0.25 (low) |
| Others | 0s | 0.4 (standard) |

### Layer 4: Hunter Logic (Overtaking)

Starting position matters differently depending on the track.

```
TrafficDrag = (GridPosition × 0.5) × PassDifficulty
```

**Hunter Bonus:** Elite drivers (VER, NOR, PIA, LEC) have PassDifficulty halved.

| Track | Pass Difficulty | Effect of Starting P5 |
|-------|-----------------|----------------------|
| Monaco | 0.95 | +2.4s drag (nearly impossible to win) |
| Singapore | 0.85 | +2.1s drag |
| Hungary | 0.70 | +1.75s drag |
| Spa | 0.20 | +0.5s drag (easy recovery) |
| Bahrain | 0.30 | +0.75s drag |

---

## 🚀 Installation

```bash
cd formula1-prediction

# Install dependencies
pip install fastf1 scikit-learn numpy pandas rich
```

**Or create a requirements.txt:**
```txt
fastf1>=3.3.0
scikit-learn>=1.3.0
numpy>=1.24.0
pandas>=2.0.0
rich>=13.0.0
```

---

## 💻 Usage

### List Available Races

```bash
python -c "import fastf1; print(fastf1.get_event_schedule(2025)[['RoundNumber', 'Country', 'EventName']].to_string())"
```

### Run a Prediction

```bash
# Standard weekend (uses FP2 for physics)
python f1_predictor_v11.py --year 2025 --gp "Australia" --session Q

# Sprint weekend (uses FP1 for physics)
python f1_predictor_v11.py --year 2025 --gp "China" --session Q
```

### Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `--year` | Season year | `2025` |
| `--gp` | Grand Prix name | `"Australia"`, `"Monaco"`, `"Great Britain"` |
| `--session` | Session type | `Q` (Qualifying), `FP1`, `FP2` |

---

## 📊 Benchmarking

Test the algorithm against historical results:

```bash
# Test against 2023 season
python benchmark_2023.py

# Test against 2024 season
python benchmark_2024.py

# Test against 2025 season
python benchmark_2025.py
```

**Sprint Weekend Note:** The benchmarks automatically use FP1 for sprint weekends (FP2 is parc fermé).

### Sprint Rounds by Year

| Year | Sprint Weekends |
|------|-----------------|
| 2023 | Azerbaijan, Austria, Belgium, Qatar, United States, Brazil |
| 2024 | China, Miami, Austria, United States, Brazil, Qatar |
| 2025 | China, Miami, Belgium, United States, Brazil, Qatar |

---

## 🏆 Historical Results

### 2023 Season (Verstappen Dominance)

| Rd | Grand Prix | Winner |
|---:|------------|--------|
| 1 | Bahrain | VER |
| 2 | Saudi Arabia | PER |
| 3 | Australia | VER |
| 4 | Azerbaijan | PER |
| 5 | Miami | VER |
| 6 | Monaco | VER |
| 7 | Spain | VER |
| 8 | Canada | VER |
| 9 | Austria | VER |
| 10 | Great Britain | VER |
| 11 | Hungary | VER |
| 12 | Belgium | VER |
| 13 | Netherlands | VER |
| 14 | Italy | VER |
| 15 | Singapore | SAI |
| 16 | Japan | VER |
| 17 | Qatar | VER |
| 18 | United States | VER |
| 19 | Mexico | VER |
| 20 | Brazil | VER |
| 21 | Las Vegas | VER |
| 22 | Abu Dhabi | VER |

### 2024 Season (Multi-Team Competition)

| Rd | Grand Prix | Winner |
|---:|------------|--------|
| 1 | Bahrain | VER |
| 2 | Saudi Arabia | VER |
| 3 | Australia | SAI |
| 4 | Japan | VER |
| 5 | China | VER |
| 6 | Miami | NOR |
| 7 | Emilia Romagna | VER |
| 8 | Monaco | LEC |
| 9 | Canada | VER |
| 10 | Spain | VER |
| 11 | Austria | RUS |
| 12 | Great Britain | HAM |
| 13 | Hungary | PIA |
| 14 | Belgium | HAM |
| 15 | Netherlands | NOR |
| 16 | Italy | LEC |
| 17 | Azerbaijan | PIA |
| 18 | Singapore | NOR |
| 19 | United States | LEC |
| 20 | Mexico | SAI |
| 21 | Brazil | VER |
| 22 | Las Vegas | RUS |
| 23 | Qatar | VER |
| 24 | Abu Dhabi | NOR |

### 2025 Season

| Rd | Grand Prix | Winner |
|---:|------------|--------|
| 1 | Australia | NOR |
| 2 | China | PIA |
| 3 | Japan | VER |
| 4 | Bahrain | PIA |
| 5 | Saudi Arabia | PIA |
| 6 | Miami | PIA |
| 7 | Emilia Romagna | VER |
| 8 | Monaco | NOR |
| 9 | Spain | PIA |
| 10 | Canada | RUS |
| 11 | Austria | NOR |
| 12 | Great Britain | NOR |
| 13 | Belgium | PIA |
| 14 | Hungary | NOR |
| 15 | Netherlands | PIA |
| 16 | Italy | VER |
| 17 | Azerbaijan | VER |
| 18 | Singapore | RUS |
| 19 | United States | VER |
| 20 | Mexico | NOR |
| 21 | Brazil | NOR |
| 22 | Las Vegas | VER |
| 23 | Qatar | VER |
| 24 | Abu Dhabi | VER |

---

## 🔧 Algorithm Details

### Configuration Constants

```python
MONTE_CARLO_RUNS = 5000
RACE_START_FUEL = 100.0
```

### Safety Car Probabilities

| Track | SC Probability |
|-------|---------------|
| Singapore | 100% |
| Monaco | 80% |
| Great Britain | 60% |
| Italy | 50% |
| Default | 30% |

### Track Lap Counts

| Track | Laps |
|-------|------|
| Monaco | 78 |
| Singapore | 62 |
| Great Britain | 52 |
| Belgium | 44 |
| Default | 58 |

---

## 📁 Project Structure

```
formula1-prediction/
├── f1_predictor_v11.py    # Main prediction engine (latest)
├── benchmark_2023.py      # 2023 season validation
├── benchmark_2024.py      # 2024 season validation
├── benchmark_2025.py      # 2025 season validation
├── README.md              # This file
└── f1_cache/              # FastF1 data cache
```

---

## ⚠️ Known Limitations

1. **Qualifying ≠ Race Pace:** Some cars (e.g., Red Bull) are setup for race pace, making them faster on Sunday than Saturday.
2. **Strategy Not Modeled:** Undercut/overcut pit strategies are not simulated.
3. **Crashes & DNFs:** Random incidents (Austria 2024 VER/NOR crash) cannot be predicted.
4. **DSQs:** Post-race disqualifications (Belgium 2024 RUS DSQ) change official results.

---

## 📄 License

MIT License


