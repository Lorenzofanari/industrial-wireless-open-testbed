# Common student mistakes

Watch for these recurring errors and address them during the session.

- **Assuming synthetic data are real measurements.** Demo-mode traces verify the
  software pipeline only; they do not measure real Wi-Fi, BLE, IEEE 802.15.4,
  Zigbee, LoRa, or SDR behaviour.
- **Confusing global inter-arrival time with the per-node interval.** The
  inter-arrival mean is computed over globally-ordered packets from multiple
  nodes, so it is typically smaller than any single node's configured interval.
- **Ignoring sequence identifiers.** Missing and duplicate counts and capture
  completeness depend on per-node `sequence_id`; skipping them hides key
  observations.
- **Ignoring manifests.** The `manifest.json` ties outputs to inputs (config,
  seed, git commit, hashes) and is the basis for reproducibility.
- **Changing seeds without documenting it.** A different seed produces a
  different trace; always record the seed used.
- **Interpreting `rssi_dbm` / `channel` labels as real RF measurements.** In demo
  mode these are synthetic labels, not measurements.
- **Running optional capture without authorisation.** The owned-device and
  receive-only tiers must only be used on equipment you own or are explicitly
  authorised to use.
