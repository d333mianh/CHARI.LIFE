# Tea catalogue

Edit any column. When you're done, tell Claude "apply teas.md" and the HTML will be regenerated to match.

- **№** — position in the list, don't change unless you want to reorder
- **Name** — heading shown on the page
- **Description** — short line under the name (1–2 short sentences works best)
- **Tags** — pipe-separated. Prefix one with `*` to make it the clay-red "accent" pill (e.g. `*Single Origin \| China \| 75°`). Escape pipes inside cells as `\|`.
- **Photo** — filename inside `webtea/photos/` (or leave blank for the kanji placeholder)
- **Price** — set the **100g** price; the three smaller weights are *derived* by the tiering rule and should match it. Each step down to a smaller weight adds **+10% to the per-gram cost** (compounding), so: **50g = 100g ÷2 ×1.10**, **25g = 100g ÷4 ×1.21**, **10g = 100g ÷10 ×1.331** — rounded to the nearest 5k. Format `Xg · Yk ₫` per weight, separated by `/`; line breaks rendered automatically.


| №  | Name                            | Description                                                                                          | Tags       | Photo                   | Price                                                      |
| -- | ------------------------------- | ---------------------------------------------------------------------------------------------------- | ---------- | ----------------------- | ---------------------------------------------------------- |
| 01 | Baihao Yinzhen                  | Silver down and moonlit hay; the hush of dawn in a cup.                                              | WHITE      | baihao-yinzhen.jpeg     | 100g · 1.3m ₫ / 50g · 715k ₫ / 25g · 395k ₫ / 10g · 175k ₫ |
| 02 | DMFR Oriental Beauty Black      | Leafhopper-bitten leaves, slow-oxidised dark. Wild honey, muscat grape, and a thread of cedar smoke. | GABA       | DMFR-black.jpeg         | 100g · 800k ₫ / 50g · 440k ₫ / 25g · 240k ₫ / 10g · 105k ₫ |
| 03 | GABA DMFR Oriental Beauty Green | Jade pear and warm beeswax, weightless and calm.                                                     | GABA       | gaba-dmfr.jpeg          | 100g · 520k ₫ / 50g · 285k ₫ / 25g · 155k ₫ / 10g · 70k ₫  |
| 04 | GABA Ruby                       | Garnet velvet: dark cherry, cocoa, sandalwood.                                                       | GABA       | gaba-ruby.jpeg          | 100g · 400k ₫ / 50g · 220k ₫ / 25g · 120k ₫ / 10g · 55k ₫  |
| 05 | Elephant Thai shu               |                                                                                                      | PUERH SHOU | puerhelephantshu02.jpeg | 100g · 350k ₫ / 50g · 195k ₫ / 25g · 105k ₫ / 10g · 45k ₫  |
| 06 | Elephant Thai shen              |                                                                                                      | PUERH SHEN | elephan-thai-shen.jpeg  | 100g · 350k ₫ / 50g · 195k ₫ / 25g · 105k ₫ / 10g · 45k ₫  |
| 07 | Yuan Xiang Bu Lang              |                                                                                                      | PUERH SHOU | yuanxian.jpeg           | 100g · 350k ₫ / 50g · 195k ₫ / 25g · 105k ₫ / 10g · 45k ₫  |
| 08 | Puerh Pincha                    |                                                                                                      | PUERH SHOU | pincha.jpeg             | 100g · 550k ₫ / 50g · 300k ₫ / 25g · 165k ₫ / 10g · 75k ₫  |
| 09 | Oolong 12                       | Steamed milk and vanilla cream — a soft white cloud.                                                 | OOLONG     | oolong12.jpeg           | 100g · 400k ₫ / 50g · 220k ₫ / 25g · 120k ₫ / 10g · 55k ₫  |
| 10 | Myanmar shen puerh              | 800 years old trees                                                                                  | PUERH SHEN | myanmar-shen.jpeg       | 100g · 700k ₫ / 50g · 385k ₫ / 25g · 210k ₫ / 10g · 95k ₫  |
| 11 | Laos 400yo                      | 400 years old trees                                                                                  | PUERH SHEN | lao-shen-puerh.jpeg     | 100g · 700k ₫ / 50g · 385k ₫ / 25g · 210k ₫ / 10g · 95k ₫  |
