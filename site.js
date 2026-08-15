(function () {
  var root = document.documentElement;
  var savedLang = localStorage.getItem("rj-lang") || "both";
  root.dataset.lang = savedLang;

  function syncLangButtons() {
    document.querySelectorAll("[data-lang]").forEach(function (btn) {
      var on = btn.dataset.lang === root.dataset.lang;
      btn.classList.toggle("is-active", on);
      btn.setAttribute("aria-pressed", on ? "true" : "false");
    });
  }

  document.querySelectorAll("[data-lang]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      root.dataset.lang = btn.dataset.lang;
      localStorage.setItem("rj-lang", btn.dataset.lang);
      syncLangButtons();
    });
  });
  syncLangButtons();

  document.querySelectorAll("[data-filter]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var filter = btn.dataset.filter;
      document.querySelectorAll("[data-filter]").forEach(function (other) {
        var on = other === btn;
        other.classList.toggle("is-active", on);
        other.setAttribute("aria-pressed", on ? "true" : "false");
      });
      document.querySelectorAll(".tea-list .tea").forEach(function (tea) {
        tea.hidden = filter !== "all" && tea.dataset.category !== filter;
      });
    });
  });
})();
