# Data: Tennessee Eastman Process (TEP)

- **Dataset:** Additional Tennessee Eastman Process Simulation Data for Anomaly Detection Evaluation
- **Authors:** Rieth, Amsel, Tran, Cook
- **Host:** Harvard Dataverse, DOI [10.7910/DVN/6C3JR1](https://doi.org/10.7910/DVN/6C3JR1)
- **Licence:** public domain dedication (the record states the owners waived their rights worldwide
  and that you may copy, modify and distribute the work for any lawful purpose).
  **Re-check the record yourself on the day you download and note the date here:** `YYYY-MM-DD`.
- **Citation:** Rieth et al. (2017), *Issues and Advances in Anomaly Detection Evaluation for
  Joint Human-Automated Systems*, Applied Human Factors and Ergonomics 2017.

## Layout

- 500 simulation runs per file; each run has its own random seed.
- Sampling every 3 minutes. Training runs: 25 h (500 samples). Testing runs: 48 h (960 samples).
- Faults start at 1 h (sample 20) in training and 8 h (sample 160) in testing.
- Columns: `faultNumber`, `simulationRun`, `sample`, 41 measurements `xmeas_1..41`,
  11 manipulated variables `xmv_1..11`.

## Fallback

If there is a licence or access problem, switch to UCI AI4I 2020 Predictive Maintenance.
