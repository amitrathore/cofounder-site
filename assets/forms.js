window.CofounderForms = {
  founderEnroll: "https://tally.so/r/D4Wv5X",
  ventureApply: "https://tally.so/r/44GNLd",
  interest: "https://tally.so/r/2ERxLg",
  withParams(baseUrl, params) {
    const url = new URL(baseUrl, window.location.href);
    Object.entries(params).forEach(([key, value]) => {
      if (value) url.searchParams.set(key, value);
    });
    return url.toString();
  }
};

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-tally-form]").forEach((link) => {
    const formKey = link.getAttribute("data-tally-form");
    const baseUrl = window.CofounderForms[formKey];
    if (!baseUrl) return;

    link.href = window.CofounderForms.withParams(baseUrl, {
      source: link.getAttribute("data-source"),
      track: link.getAttribute("data-track"),
      payment_plan: link.getAttribute("data-payment-plan")
    });
  });

  document.querySelectorAll("[data-tally-embed]").forEach((frame) => {
    const formKey = frame.getAttribute("data-tally-embed");
    const baseUrl = window.CofounderForms[formKey];
    if (!baseUrl) return;

    frame.setAttribute("data-tally-src", window.CofounderForms.withParams(baseUrl, {
      source: frame.getAttribute("data-source"),
      track: frame.getAttribute("data-track"),
      hideTitle: "1",
      transparentBackground: "1",
      dynamicHeight: "1"
    }));
  });

  if (window.Tally && typeof window.Tally.loadEmbeds === "function") {
    window.Tally.loadEmbeds();
  }
});
