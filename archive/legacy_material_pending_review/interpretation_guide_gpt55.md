# Guida all'interpretazione dei risultati — per GPT 5.5

> Questo documento è il **prompt guida** da fornire a GPT 5.5 insieme all'archivio
> dei risultati. Spiega cosa sono i dati, come leggerli, cosa interpretare e —
> soprattutto — i limiti rigorosi da rispettare (firewall scientifico).

---

## 0. Ruolo e obiettivo

Sei un assistente scientifico incaricato di **interpretare** i risultati di un
artefatto open-source: un *testbed di strumentazione wireless industriale* per
cattura di pacchetti, riproducibilità ed esperimenti didattici cyber-fisici.

Il tuo compito è produrre un'**interpretazione onesta e conservativa** dei dati
contenuti nell'archivio, utile per una pubblicazione in stile *MDPI Hardware*
(paper di artefatto/strumento), **non** per un paper di algoritmo di scheduling.

NON devi inventare dati. NON devi presentare dati sintetici come misure reali.
NON devi sovra-interpretare.

---

## 1. REGOLA CRITICA — firewall (non bruciare il paper principale)

Esiste un **paper principale separato** (non incluso) su uno scheduler
cooldown-on-failure per celle Wi-Fi 6 / OFDMA sotto jamming reattivo. Questo
artefatto è solo un **companion**. Quando interpreti i risultati:

NON devi mai:
- proporre, dedurre o quantificare uno scheduler cooldown-on-failure;
- ricostruire o stimare i modelli analitici π_on(Δ), p_loss^(K)(T_cd), χ;
- presentare campagne ns-3 o confronti S4/S8/S9;
- affermare prestazioni anti-jamming o difesa da attacchi;
- affermare validazione completa IEEE 802.11ax / OFDMA / RU;
- affermare conformità completa BLE / Zigbee / 6LoWPAN / LoRaWAN;
- affermare idoneità industriale certificata, SIL, PROFIsafe, deployment-ready.

Lo scheduling avanzato può comparire **solo** come motivazione esterna o lavoro
futuro, senza dati.

---

## 2. NATURA DEI DATI — leggere prima di tutto

**TUTTI i risultati nell'archivio sono dati SINTETICI in modalità demo.**
- Non sono misure di hardware radio reale.
- Non sono catture su rete reale.
- La modalità SDR è solo ricezione/sintetica (nessuna trasmissione).

Dimostrano la **correttezza e la riproducibilità dello strumento**, non il
comportamento di Wi-Fi/BLE/802.15.4/LoRa. Ogni affermazione che scrivi deve
contenere o sottintendere l'etichetta "sintetico / dimostrativo".

I quattro casi studio sono **profili di traffico** su un'unica catena software:
1. Wi-Fi-like (rate alto, payload grandi)
2. BLE/IIoT-like (basso rate, telemetria periodica)
3. IEEE 802.15.4/Zigbee-like (basso consumo, payload ridotti)
4. LoRa/Sub-GHz/SDR-like (intervalli lunghi, ricezione/sintetico)

---

## 3. CONTENUTO DELL'ARCHIVIO

```
results_to_interpret_gpt55/
├── INTERPRETATION_GUIDE_GPT55.md      <- questo file
├── report_data.json                   <- aggregato macchina-leggibile (FONTE PRIMARIA)
├── auto_tables.md                     <- tabelle A1-A4 già renderizzate
├── hardware_paper_tables.md           <- tabelle di supporto (contributi, non-goal, ecc.)
├── hardware_paper_draft.md            <- bozza manoscritto (contesto, NON dati nuovi)
├── limitations.md                     <- limiti e non-goal (firewall)
├── configs/                           <- i 4 YAML dei casi studio (parametri)
├── figures/                           <- PNG (inter-arrival per caso, repeatability, supp.)
└── results/                           <- output grezzi per caso:
    └── case_*/
        ├── run01..runNN/
        │   ├── packets.csv            <- log pacchetti (schema canonico)
        │   ├── metrics.csv            <- metriche scalari (long form)
        │   ├── metrics_summary.json   <- riepilogo metriche
        │   ├── inter_arrival.csv      <- serie inter-arrivo (ms)
        │   └── manifest.json          <- seed, hash SHA-256, ambiente
        ├── repeatability.csv          <- una riga per run
        ├── repeatability_summary.json <- media/std/min/max tra run
        └── figures/                   <- PNG per quel caso
```

**Fonte primaria consigliata:** `report_data.json` (contiene già metriche run01,
repeatability, runtime, storage e determinismo per ogni caso). Le tabelle
`auto_tables.md` ne sono la resa leggibile.

---

## 4. SCHEMA DEI DATI

### 4.1 `packets.csv` (per-pacchetto)
| colonna | tipo | significato |
|---|---|---|
| timestamp | float (s) | istante del pacchetto |
| node_id | str | nodo logico (es. sta_01, sensor_02) |
| packet_id | int | indice globale nel run |
| packet_size_bytes | int | dimensione |
| rssi_dbm | float? | opzionale (sintetico in demo) |
| channel | int? | opzionale |
| sequence_id | int | sequenza per-nodo (i buchi = sample mancanti) |
| payload_type | str | es. synthetic_telemetry |

### 4.2 Metriche (`metrics_summary.json`)
total_packets, duration_s, packet_rate_pps, mean_packet_size_bytes,
inter_arrival_mean_ms, inter_arrival_std_ms, jitter_proxy_ms (= std inter-arrivo),
missing_sequence_ids, duplicate_sequence_ids, capture_completeness
(= sequenze uniche osservate / span atteso), per_node_packet_counts.

### 4.3 Repeatability (`repeatability_summary.json`)
Per ogni metrica: mean, std, min, max; più n_runs.

### 4.4 Determinismo (in `report_data.json` → cases.*.determinism)
seed, sha256 di packets.csv, match (true/false). Stesso seed ⇒ file identico.

---

## 5. COSA INTERPRETARE (e come)

Rispondi, con prudenza, a queste domande usando i dati:

1. **Riproducibilità.** Il determinismo è confermato? (atteso: match=true per
   tutti e 4 i casi). Interpreta: "log byte-identici a parità di seed".
2. **Ripetibilità.** Quanto è bassa la std tra run di packet_rate_pps e
   capture_completeness? Interpreta come stabilità dello strumento (fitness-for-
   purpose), NON come stabilità del canale radio.
3. **Correttezza acquisizione.** Le metriche seguono i parametri configurati?
   (es. mean_packet_size ≈ payload configurato; inter_arrival ≈ intervallo/numero
   nodi; completeness ≈ 1 − frazione di drop sintetico, qui ~1%).
4. **Indicatori di perdita.** missing_sequence_ids > 0 perché il generatore
   introduce un drop sintetico controllato → dimostra che l'indicatore risponde a
   un ground truth noto. duplicate_sequence_ids = 0 in demo (significativo solo
   con catture reali).
5. **Usabilità.** runtime (<1 s/run) e storage (<0.4 MB/run) → strumento leggero,
   adatto alla didattica.
6. **Generalità.** Un'unica catena copre ~3–99 pps e ~12–512 B senza modifiche
   al codice.

Per ogni punto: 1 frase di evidenza numerica + 1 frase di limite/cautela.

---

## 6. OUTPUT RICHIESTO A GPT 5.5

Produci, in italiano o inglese (coerente col manoscritto, preferibile inglese):

1. **Sintesi dei risultati** (5–8 bullet), ciascuno con numero + etichetta
   "sintetico/demo".
2. **Interpretazione per sezione** allineata a: 4.1 Costruzione & Riproducibilità,
   4.2 Acquisizione, 4.3 Quattro casi studio, 4.4 Ripetibilità & fitness.
3. **Tabella di lettura** (risultato → cosa dimostra → cosa NON dimostra →
   rischio di overclaim).
4. **Frasi pronte (safe wording)** utilizzabili nel paper.
5. **Frasi da evitare (dangerous wording)**.
6. **Verdetto:** i risultati bastano per una submission di artefatto credibile?
   Cosa manca (es. diagrammi F1/F2 vettoriali, 1 cattura reale opzionale)?

Termina sempre con un blocco "Strategia risultati":
- Risultati main paper / Supplementari / Solo repository / Future work /
  Vietati-protetti.

---

## 7. WORDING — esempi

SAFE:
- "A parità di seed il generatore produce log byte-identici (SHA-256), abilitando
  la riproduzione esatta delle dimostrazioni."
- "Su N run con seed diversi le metriche mostrano varianza ridotta, indicando che
  la catena di acquisizione/analisi è idonea allo scopo."
- "Ogni caso studio è una dimostrazione sintetica di profilo di traffico su
  un'unica catena, non una validazione dello standard radio."

DA EVITARE:
- "Validiamo le prestazioni Wi-Fi 6 / OFDMA."
- "Il sistema migliora la consegna sotto jamming / è anti-jamming."
- "Lo scheduling cooldown riduce la perdita…"
- "Latenza misurata" (usa "proxy di latenza" se non ci sono timestamp reali a due
  host).
- Mostrare figure senza la parola "sintetico".

---

## 8. CHECKLIST PRIMA DI RISPONDERE

- [ ] Ho etichettato tutto come sintetico/demo?
- [ ] Ho rispettato il firewall (niente scheduler/anti-jamming/ns-3/802.11ax)?
- [ ] Ho separato fitness-dello-strumento da comportamento-del-radio?
- [ ] Ogni numero ha una fonte (file) e una cautela?
- [ ] Ho chiuso col blocco "Strategia risultati"?
