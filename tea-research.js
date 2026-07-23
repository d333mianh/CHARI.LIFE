const teas = [
  {
    id: "01",
    photo: "photos/baihao-yinzhen.jpeg",
    currentName: "Baihao Yinzhen",
    currentDescription: "Silver down and moonlit hay; the hush of dawn in a cup.",
    status: "confirmed",
    statusLabel: "Owner confirmed",
    targetName: "2025 Bai Hao Yin Zhen",
    evidence: "The owner confirms the Bai Hao Yin Zhen identity and the 2025 year. Public references support the standard Silver Needle style; the exact origin and batch still need provenance.",
    missing: ["Country and province", "Original packaging or supplier", "Harvest season or batch code"],
    guardrail: "Use standard Silver Needle context only where it fits this batch, and do not infer a Fujian origin without evidence.",
    draftEn: "A 2025 Silver Needle white tea with the quiet clarity of a bud-led style. Meadow flowers, fresh hay and a touch of melon sweetness rest on a smooth, lightly creamy body.",
    draftRu: "Белый чай «Серебряные иглы» урожая 2025 года с тихим, прозрачным характером почечного белого чая. Ноты луговых цветов, свежего сена и лёгкой дынной сладости раскрываются на гладкой, чуть кремовой текстуре.",
    sources: [
      ["Silver Needle reference", "https://www.chineseteagroup.com/products/silver-needle-white-tea-bai-hao-yin-zhen"],
      ["Tea Guardian", "https://www.teaguardian.com/quality-varieties/tea-varieties/silver-needles-white-tea/"],
      ["Origin-neutral style guide", "https://www.teacurious.com/guide-silver-needle/"]
    ]
  },
  {
    id: "02",
    photo: "photos/DMFR-black.jpeg",
    currentName: "DMFR Oriental Beauty Black",
    currentDescription: "Leafhopper-bitten leaves, slow-oxidised dark. Wild honey, muscat grape, and a thread of cedar smoke.",
    status: "confirmed",
    statusLabel: "Owner confirmed",
    targetName: "Dong Fang Mei Ren (Oriental Beauty) Black Tea",
    evidence: "The owner accepts Dong Fang Mei Ren and supplied a matching Thai black-tea reference from Yoshi En. It describes Qing Xin, leafhopper-bitten material and strong oxidation; those batch facts still need confirmation for our tea.",
    missing: ["Country, farm and producer", "Cultivar", "Confirm that “Black” is the producer's processing label", "Leafhopper-bitten material confirmation"],
    guardrail: "The name family is identified; origin, leafhopper action and processing details still belong to this specific batch and must not be assumed.",
    draftEn: "A Thai black tea in the Dong Fang Mei Ren tradition, with the honeyed fruit and generous oxidation associated with this style. Ripe peach and nectar meet a gentle malty depth, while a soft floral lift keeps the cup clear. The finish is creamy, sweet and quietly persistent across later infusions.",
    draftRu: "Тайский чёрный чай в стиле Дун Фан Мэй Жэнь — с медовой фруктовостью и глубокой ферментацией, характерными для этого направления. Спелый персик и нектар соединяются с мягким солодовым тоном, а лёгкая цветочность сохраняет чистоту вкуса. Послевкусие кремовое, сладкое и долгое.",
    sources: [
      ["Owner-selected Yoshi En source", "https://www.yoshien.com/en/thai-oriental-beauty-black-tea-organic.html"],
      ["Thai Oriental Beauty context", "https://siamteas.com/thai-teas/overview-teas-from-north-thailand/dms-cha-nang-ngam-oriental-beauty-oolong-tea-north-thailands-dong-fang-mei-ren/"]
    ]
  },
  {
    id: "03",
    photo: "photos/gaba-dmfr.jpeg",
    currentName: "GABA DMFR Oriental Beauty Green",
    currentDescription: "Jade pear and warm beeswax, weightless and calm.",
    status: "confirmed",
    statusLabel: "Owner confirmed",
    targetName: "GABA Dong Fang Mei Ren (Oriental Beauty) — “Green” version",
    evidence: "The owner supplied a Thai Oriental Beauty oolong reference and a separate GABA Dong Fang Mei Ren listing confirms the GABA combination. The exact meaning of “Green” and the processing of our batch remain supplier-specific.",
    missing: ["Country, farm and producer", "Origin and cultivar", "What “Green” means in the producer's range", "Leafhopper and GABA-process confirmation"],
    guardrail: "Use the decoded name, but do not call this conventional green tea or invent an oxidation level until the supplier explains “Green.”",
    draftEn: "A lighter expression of GABA Dong Fang Mei Ren, pairing honeyed fruit with a brighter floral line. Peach and white grape unfold over orchid, citrus peel and a trace of warm spice. Smooth in texture and gently rounded, it leaves a long, clean sweetness without becoming heavy.",
    draftRu: "Более лёгкая версия ГАБА-улуна Дун Фан Мэй Жэнь, где медовая фруктовость сочетается с яркой цветочной линией. Персик и белый виноград раскрываются оттенками орхидеи, цитрусовой цедры и тёплых специй. Текстура мягкая и округлая, а чистая сладость долго остаётся в послевкусии.",
    sources: [
      ["Owner-selected Yoshi En source", "https://www.yoshien.com/en/thailand-oriental-beauty-oolong.html"],
      ["GABA Dong Fang Mei Ren example", "https://miychay.com/en/ulun-bez-dobavok/gaba-dun-fan-mey-zhen-skhidna-krasunya-vid-maystra-khao-2379/"],
      ["Oriental Beauty production context", "https://eco-cha.com/blogs/news/12643165-the-quest-for-oriental-beauty"]
    ]
  },
  {
    id: "04",
    photo: "photos/gaba-ruby.jpeg",
    currentName: "GABA Ruby",
    currentDescription: "Garnet velvet: dark cherry, cocoa, sandalwood.",
    status: "confirmed",
    statusLabel: "Owner confirmed",
    targetName: "2026 GABA Ruby — Qing Xin cultivar",
    evidence: "The owner confirms 2026 and Qing Xin, and supplied Yoshi En's Thai Ruby Oolong as a flavour reference. A second GABA Ruby source supports the jammy berry side of the style; neither page is treated as our batch record.",
    missing: ["Country and growing region", "Producer", "Harvest season and processing details"],
    guardrail: "Build the profile around this Qing Xin batch; do not borrow Ruby №18 / Red Jade cultivar facts.",
    draftEn: "A fruit-forward GABA oolong made from Qing Xin, with the warmth of a more deeply oxidised style. Apricot and peach lead into berry preserve and a faint pastry sweetness. The finish is juicy and rounded, with a gentle tart edge that keeps the ripe fruit lively.",
    draftRu: "Фруктовый ГАБА-улун из сорта Цин Синь, тёплый и насыщенный благодаря более глубокой ферментации. Абрикос и персик переходят в оттенки ягодного варенья и лёгкой выпечки. Послевкусие сочное и округлое, с мягкой кислинкой, которая оживляет спелую фруктовость.",
    sources: [
      ["Owner-selected Yoshi En source", "https://www.yoshien.com/en/thai-ruby-oolong-organic.html"],
      ["Qing Xin example", "https://teagallery.eu/products/gaba-ruby"]
    ]
  },
  {
    id: "05",
    photo: "photos/puerhelephantshu02.jpeg",
    currentName: "Elephant Thai shu",
    currentDescription: "",
    status: "confirmed",
    statusLabel: "Owner confirmed",
    targetName: "Thailand Pu-erh SHOU Tea “Elephant”",
    evidence: "The owner confirms the product name; the front wrapper independently supports shou/ripe processing and Product of Thailand. The back has been checked and contains no additional identifying details.",
    missing: ["Any inner ticket or purchase record", "Producer, growing region, year and weight"],
    guardrail: "Keep “Elephant” as the confirmed catalogue product name, while separating it from producer and factory facts that are still unknown.",
    draftEn: "A Thai shou with the dark, rounded character of ripe processing. Clean wood and toasted grain lead into caramelised sweetness, while the body stays smooth and dense rather than heavy.",
    draftRu: "Тайский шу с тёмным, округлым настоем и мягкой плотностью, характерными для зрелой ферментации. Чистые древесные ноты и поджаренное зерно переходят в карамельную сладость, а вкус остаётся гладким и насыщенным, но не тяжёлым.",
    sources: [
      ["Thai craft shou production", "https://tea-side.com/blog/craft-shu-puerh-tea-interview/"],
      ["Thai shou market context", "https://tea-village.com/en/4-pu-erh"]
    ]
  },
  {
    id: "06",
    photo: "photos/elephan-thai-shen.jpeg",
    currentName: "Elephant Thai shen",
    currentDescription: "",
    status: "confirmed",
    statusLabel: "Owner confirmed",
    targetName: "Thailand Pu-erh SHENG Tea “Elephant”",
    evidence: "The owner confirms the product name; the front wrapper independently supports sheng/raw processing and Product of Thailand. The back has been checked and contains no additional identifying details.",
    missing: ["Any inner ticket or purchase record", "Producer, growing region, year and weight"],
    guardrail: "Use “sheng” in the final English and Russian names, and do not infer a region, producer or vintage from the front wrapper.",
    draftEn: "A Thai sheng made in the raw, slowly evolving style. Comparable northern Thai teas move between herbaceous freshness, dry wood and gentle dried-fruit sweetness, with light astringency giving the cup structure.",
    draftRu: "Тайский шэн, выполненный в сыром стиле и рассчитанный на постепенное развитие. У близких северотаиландских чаёв травянистая свежесть сочетается с сухим деревом и мягкой сладостью сухофруктов, а лёгкая терпкость собирает вкус.",
    sources: [
      ["Northern Thai sheng example", "https://www.siam-teas.com/product/wild-thai-sheng-hei-cha-pu-er-style/"],
      ["Northern Thai pu-erh context", "https://www.hoyumtea.com/en/post/doi-wawee"]
    ]
  },
  {
    id: "07",
    photo: "photos/yuanxian.jpeg",
    currentName: "Yuan Xiang Bu Lang",
    currentDescription: "",
    status: "matched",
    statusLabel: "Strong match",
    targetName: "2011 Ye Zhuang Shuang Li “Yuan Xiang Bu Lang” ripe pu-erh",
    evidence: "The wrapper reads 原香布朗, identifies ripe pu-erh and 357 g, and matches a public 2011 product record.",
    missing: ["Back-wrapper or inner-ticket photo to confirm year and factory"],
    guardrail: "Research-ready flavour direction: smooth, sweet, dense and dark-chocolate-like. Confirm against our actual cup before final copy.",
    draftEn: "A mature 2011 Bulang ripe pu-erh with a clear red-brown liquor and a dense, polished body. It begins smooth and sweet, then gathers weight into a silky texture with dark-chocolate depth. Later infusions grow lighter without turning thin, returning to a clean and persistent sweetness.",
    draftRu: "Выдержанный буланский шу-пуэр 2011 года с прозрачным красно-коричневым настоем и плотной, отполированной текстурой. Сначала он мягкий и сладкий, затем набирает вес, становится шелковистым и уходит в глубину тёмного шоколада. В поздних проливах вкус светлеет, но не пустеет, возвращаясь к чистой и долгой сладости.",
    sources: [
      ["Archived product", "https://steepster.com/teas/yunnan-sourcing/49416-2011-ye-zhuang-shuang-li-red-label-yuan-xiang-bu-lang-ripe-puerh"],
      ["2011 tasting article", "https://m.guchaju.com/cha/4271.html"]
    ]
  },
  {
    id: "08",
    photo: "photos/pincha.jpeg",
    currentName: "Puerh Pincha",
    currentDescription: "",
    status: "confirmed",
    statusLabel: "Owner confirmed",
    targetName: "TAI GUO CHI TSE PIN CHA · 泰國七子餅茶 · 泰國普洱茶 · ชาผู่เอ๋อร์ ประเทศไทย — Thai shou pu-erh, 200 g",
    catalogueName: "Tai Guo Chi Tse Pin Cha",
    catalogueMeta: "Thai Qizi Bingcha · 泰國七子餅茶 · 泰國普洱茶 · ชาผู่เอ๋อร์ ประเทศไทย · NET: 200g",
    evidence: "The wrapper prints TAI GUO CHI TSE PIN CHA, 泰國七子餅茶, 泰國普洱茶, ชาผู่เอ๋อร์ ประเทศไทย and NET: 200g. The owner confirms that this cake is shou pu-erh and identifies an interesting sour note in the cup.",
    missing: ["Any inner ticket or purchase record", "Producer, growing region within Thailand and year"],
    guardrail: "Treat the shou process and sour taste as owner-confirmed. Preserve the wrapper's names, but do not infer a factory, region or vintage that the packaging does not provide.",
    draftEn: "Tai Guo Chi Tse Pin Cha is a 200 g Thai shou pu-erh cake. Its dark, smooth body carries an intriguing sour note that cuts through the earthy, gently sweet depth and keeps the cup lively.",
    draftRu: "Tai Guo Chi Tse Pin Cha — тайский шу-пуэр в 200-граммовом блине. Тёмный, мягкий вкус оживляет необычная кислинка: она проходит сквозь землистую сладость и делает настой более выразительным.",
    sources: [
      ["Qizi Bingcha format reference", "https://chamart.jp/en/archives/learn_kinds/yunnanqizibingcha_china/"]
    ]
  },
  {
    id: "09",
    photo: "photos/oolong12.jpeg",
    currentName: "Oolong 12",
    currentDescription: "Steamed milk and vanilla cream — a soft white cloud.",
    status: "confirmed",
    statusLabel: "Owner confirmed",
    targetName: "2026 Jin Xuan Oolong #12",
    evidence: "The owner confirms Jin Xuan Oolong №12 and the 2026 year, and directs us to use the broad taste profile from Yoshi En's Soft Stem / Ruan Zhi №17 page. The identity remains Jin Xuan №12.",
    missing: ["Country and producer", "Confirm natural aroma versus added flavouring", "Harvest season or batch code", "Actual-cup check against the borrowed flavour direction"],
    guardrail: "Use only the broad No.17 flavour direction at the owner's request. Do not transfer its cultivar, award, oxidation, organic certification, farm or harvest facts to Jin Xuan №12.",
    draftEn: "A balanced, easy-drinking oolong with a clean vegetal sweetness. Fresh green notes and soft meadow florals rest on a smooth, lightly rounded body. The finish is calm and gently sweet, making the tea refreshing without sharpness and comfortable across repeated infusions.",
    draftRu: "Сбалансированный улун для лёгкого повседневного чаепития, с чистой растительной сладостью. Свежие зелёные ноты и мягкие луговые цветы раскрываются на гладкой, слегка округлой текстуре. Послевкусие спокойное и деликатно-сладкое; чай освежает без резкости и сохраняет ровный характер в последующих проливах.",
    sources: [
      ["Owner-directed flavour reference: Soft Stem №17", "https://www.yoshien.com/en/thai-soft-stem-oolong-organic.html"],
      ["Jin Xuan №12", "https://www.teafromtaiwan.com/blog/6_jinxuan-milk-oolong-tea.html"],
      ["Cultivar reference", "https://www.fda.gov.tw/tc/includes/GetFile.ashx?id=f636696667060389430"]
    ]
  },
  {
    id: "10",
    photo: "photos/myanmar-shen.jpeg",
    currentName: "Myanmar shen puerh",
    currentDescription: "800 years old trees",
    status: "matched",
    statusLabel: "Exact wrapper match",
    targetName: "2024 Yeren Shan “Myanmar Ancient Tree” sheng, 500 g",
    evidence: "The wrapper and public listing align on Yeren Shan, Myanmar, raw tea, 500 g and the same ancient-tree presentation.",
    missing: ["Back-wrapper confirmation of the 2024 date"],
    guardrail: "Present “single tree” and “800 years” as wrapper or producer claims, not independently verified facts.",
    draftEn: "A 500 g Myanmar sheng sold under the Yeren Shan “Ancient Tree” name. The cup is rich, strong and full-bodied, opening with clear bitterness and astringency that soften quickly into a fresh, coherent finish. The wrapper's “single tree” and “800 years” language remains a producer claim, not an independently verified fact.",
    draftRu: "Пятисотграммовый мьянманский шэн под названием Yeren Shan «Древнее дерево». Настой насыщенный, крепкий и полнотелый: заметные горечь и терпкость быстро смягчаются, оставляя свежий, цельный финал. Указания «одно дерево» и «800 лет» остаются заявлениями на обёртке или со стороны производителя, а не независимо подтверждёнными фактами.",
    sources: [
      ["Matching product", "https://puermarket.ru/product/2024-yeren-shan-drevnie-derevya-shen-puer-500g"]
    ]
  },
  {
    id: "11",
    photo: "photos/lao-shen-puerh.jpeg",
    currentName: "Laos 400yo",
    currentDescription: "400 years old trees",
    status: "confirmed",
    statusLabel: "Owner confirmed",
    targetName: "Phongsali Village, Laos — 400-Year-Old-Tree SHENG-Style Tea",
    evidence: "The owner identifies the cake as coming from Phongsali village in Laos. Old-tree sheng-style tea from northern Laos is a real category, but this unwrapped cake still cannot be matched to a producer or year.",
    missing: ["Original wrapper or purchase record", "Producer or tea garden in Phongsali village", "Year and cake weight", "Evidence behind the 400-year claim"],
    guardrail: "Use Phongsali village as owner-supplied provenance. Present “400-year-old tree” as a supplier or product claim, not an independently verified age.",
    draftEn: "A sheng-style tea from Phongsali village in northern Laos, a region where tea is gathered from tall old trees and brewed through many infusions. Comparable Phongsali cakes lean soft and sweet, with fresh green notes, light florals and a mineral, gently creamy finish.",
    draftRu: "Шэн в лаосском стиле из деревни Пхонгсали на севере страны, где чай собирают с высоких старых деревьев и заваривают многими проливами. Близкие по происхождению блины обычно мягкие и сладкие, со свежими зелёными нотами, лёгкой цветочностью, минеральностью и чуть кремовым финалом.",
    sources: [
      ["Comparable Laos tea", "https://onerivertea.com/collections/new-vintage/products/2022-spring-laos-gushu-sheng-puer"],
      ["Age-claim context", "https://www.helvetas.org/en/switzerland/how-you-can-help/follow-us/multimedia-stories-from-our-projects/laos-tea-tree"]
    ]
  }
];

globalThis.teaResearch = teas;

const board = document.querySelector("#tea-board");
const emptyState = document.querySelector("#empty-state");

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function sourceMarkup(sources) {
  if (!sources.length) {
    return '<div class="source-links"><span>No exact public listing found</span></div>';
  }

  return `<div class="source-links">${sources.map(([label, url]) => (
    `<a href="${escapeHtml(url)}" target="_blank" rel="noreferrer">${escapeHtml(label)} ↗</a>`
  )).join("")}</div>`;
}

function teaCard(tea) {
  const missingItems = tea.missing.map(item => `<li>${escapeHtml(item)}</li>`).join("");
  const currentDescription = escapeHtml(tea.currentDescription);
  const copyState = tea.draftEn && tea.draftRu ? "draft" : tea.copyConflictEn ? "conflict" : "pending";
  const copyEn = tea.draftEn || tea.copyConflictEn || "Pending batch facts, cross-source synthesis, and an actual-cup check.";
  const copyRu = tea.draftRu || tea.copyConflictRu || "Ждём данных о партии, сверки источников и дегустации этого чая.";
  const copyLabelEn = copyState === "draft"
    ? "English description · accepted copy"
    : copyState === "conflict" ? "English description · source conflict" : "English description · target";
  const copyLabelRu = copyState === "draft"
    ? "Описание на русском · принято"
    : copyState === "conflict" ? "Описание на русском · конфликт источников" : "Описание на русском · цель";

  return `
    <article class="research-card" data-status="${escapeHtml(tea.status)}" data-copy="${copyState}">
      <div class="card-visual">
        <span class="tea-index">Tea № ${escapeHtml(tea.id)}</span>
        <img src="${escapeHtml(tea.photo)}" alt="${escapeHtml(tea.currentName)}" />
      </div>
      <div class="card-body">
        <div class="card-title-row">
          <h3 class="card-title">${escapeHtml(tea.currentName)}</h3>
          <span class="status-pill">${escapeHtml(tea.statusLabel)}</span>
        </div>

        <div class="comparison">
          <div class="current">
            <span class="current-label">Previous catalogue</span>
            <p class="current-name">${escapeHtml(tea.currentName)}</p>
            <p class="current-description">${currentDescription}</p>
          </div>
          <div class="target">
            <span class="target-label">Applied verified identity</span>
            <p class="target-name">${escapeHtml(tea.targetName)}</p>
            <p class="evidence">${escapeHtml(tea.evidence)}</p>
          </div>
        </div>

        <div class="copy-preview" aria-label="Future bilingual description fields">
          <div class="copy-box">
            <span class="copy-label">${escapeHtml(copyLabelEn)}</span>
            <p>${escapeHtml(copyEn)}</p>
          </div>
          <div class="copy-box" lang="ru">
            <span class="copy-label">${escapeHtml(copyLabelRu)}</span>
            <p>${escapeHtml(copyRu)}</p>
          </div>
        </div>

        <div class="card-lower">
          <div>
            <span class="missing-title">Still needed</span>
            <ul class="missing-list">${missingItems}</ul>
          </div>
          <div class="guardrail"><strong>Truth guardrail:</strong> ${escapeHtml(tea.guardrail)}</div>
        </div>

        ${sourceMarkup(tea.sources)}
      </div>
    </article>`;
}

if (board) {
  board.innerHTML = teas.map(teaCard).join("");

  const counts = teas.reduce((acc, tea) => {
    acc[tea.status] = (acc[tea.status] || 0) + 1;
    return acc;
  }, {});

  document.querySelector("#confirmed-count").textContent = counts.confirmed || 0;
  document.querySelector("#matched-count").textContent = counts.matched || 0;
  document.querySelector("#identity-count").textContent = teas.length;
  document.querySelector("#draft-count").textContent = teas.filter(tea => tea.draftEn && tea.draftRu).length;

  document.querySelectorAll(".filter").forEach(button => {
    button.addEventListener("click", () => {
      const selected = button.dataset.filter;

      document.querySelectorAll(".filter").forEach(item => {
        const active = item === button;
        item.classList.toggle("is-active", active);
        item.setAttribute("aria-pressed", String(active));
      });

      let visible = 0;
      document.querySelectorAll(".research-card").forEach(card => {
        const show = selected === "all" || card.dataset.status === selected;
        card.hidden = !show;
        if (show) visible += 1;
      });

      emptyState.hidden = visible !== 0;
    });
  });
}
