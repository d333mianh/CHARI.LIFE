// Progressive enhancement: append a per-tea "Order on Telegram" action to each
// catalogue card. This lives in JS (rather than in the hand-maintained
// teas.md -> index.html rows) so it stays DRY and survives row regeneration.
// It degrades gracefully: the global nav Telegram link and the bottom
// "open Telegram" CTA still work if JS is disabled.
(function () {
  "use strict";
  var CHANNEL = "https://t.me/chariteas";

  var cards = document.querySelectorAll(".catalogue-section .tea");
  Array.prototype.forEach.call(cards, function (card) {
    var nameRow = card.querySelector(".tea-name-row");
    if (!nameRow) return;

    var container = nameRow.parentElement;
    if (!container || container.querySelector(".tea-order")) return;

    var nameEl = card.querySelector(".tea-name");
    var name = nameEl ? nameEl.textContent.trim() : "this tea";

    var link = document.createElement("a");
    link.className = "tea-order";
    link.href = CHANNEL;
    link.target = "_blank";
    link.rel = "noopener";
    link.setAttribute("aria-label", "Order " + name + " on Telegram");
    link.textContent = "Order on Telegram \u2197";

    container.appendChild(link);
  });
})();
