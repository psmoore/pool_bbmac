# BBMAC (Brian Bent Memorial Aquatics Complex) — unofficial preview

A mock-up of [bbmac.org](https://bbmac.org/) (Home, Lap Swim, About the Aquatics Complex, Masters Swimming, Youth Water Polo,
Booking the Pool) with BBMAC's competition and instructional pools on one live [Pool Relay](https://www.poolrelay.com) schedule.
Not operated by or affiliated with Coronado Unified School District.

No schedule is typed into the pages. Lap swim hours, Masters workouts, CIF games and closures are filled by `finder.js` from the
live Pool Relay view; `build.py` holds only rates, temperatures, policies and facts about the water.

- `build.py`: generates the six pages.
- `finder.js`: `#today`, `#week`, and `data-live` elements (`hours`, `when`, `exceptions`, `dates`, `closures`).
- Pool Relay view: `vvrn1HWdluEYCLgwunF2nq` (BBMAC, lane by lane).
