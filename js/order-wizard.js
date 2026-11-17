/* Mobile order wizard + live cake preview — White Cakes */
(function () {
  const WA_BASE = "https://wa.me/639474382632?text=";
  const FORM_URL = "https://formspree.io/f/xjywgqvq";

  const CAKES = {
    marble: {
      label: "Signature Marble",
      formValue: "Signature Marble",
      image: "/assets/signature-marble-cake-cebu.webp",
      w: 800,
      h: 800,
      sizes: ['6"', '8"'],
      defaultSize: '6"',
      messageTop: "34%",
      caption: "6-inch ivory marble · shell border · one rose",
    },
    bouquet: {
      label: "Bouquet Cake",
      formValue: "Bouquet Cake",
      image: "/assets/bouquet-cake-pink-wrapper-cebu.webp",
      w: 1200,
      h: 1607,
      sizes: ['6"', '8"'],
      defaultSize: '6"',
      messageTop: "28%",
      caption: "Piped rosettes · bouquet wrap",
    },
    bento: {
      label: "Bento",
      formValue: "Bento",
      image: "/assets/bento-cake-cebu.webp",
      w: 800,
      h: 800,
      sizes: ['Bento 4"'],
      defaultSize: 'Bento 4"',
      messageTop: "38%",
      caption: '4-inch · shells · ribbon · one rose',
    },
    custom: {
      label: "Custom",
      formValue: "Custom",
      image: "/assets/signature-marble-cake-cebu.webp",
      w: 800,
      h: 800,
      sizes: ['6"', '8"', 'Bento 4"'],
      defaultSize: '6"',
      messageTop: "34%",
      caption: "Your brief · send a reference photo",
    },
  };

  const FLAVOR_ACCENTS = {
    Chocolate: "#5c4033",
    Vanilla: "#f8f4ec",
    Ube: "#9b7bb8",
    Mango: "#e8a54b",
    "Red Velvet": "#a63d4a",
  };

  const ALIASES = {
    "signature marble": "marble",
    marble: "marble",
    "bouquet cake": "bouquet",
    bouquet: "bouquet",
    bento: "bento",
    custom: "custom",
  };

  const state = {
    step: 1,
    cakeKey: "",
    size: "",
    flavor: "",
    cakeMessage: "",
    date: "",
    name: "",
    phone: "",
    email: "",
    fulfillment: "pickup",
    address: "",
    notes: "",
    customPreviewUrl: "",
  };

  const root = document.getElementById("order-wizard");
  if (!root) return;

  const previewImg = document.getElementById("preview-img");
  const previewCaption = document.getElementById("preview-caption");
  const previewMessage = document.getElementById("preview-message");
  const previewFlavor = document.getElementById("preview-flavor");
  const previewSize = document.getElementById("preview-size");
  const progress = document.getElementById("order-progress");
  const stepCount = document.getElementById("order-step-count");
  const status = document.getElementById("wizard-status");
  const form = document.getElementById("order-wizard-form");
  const btnBack = document.getElementById("wizard-back");
  const btnNext = document.getElementById("wizard-next");
  const btnWa = document.getElementById("wizard-whatsapp");
  const stepPanels = root.querySelectorAll("[data-step-panel]");
  const photoInput = document.getElementById("wizard-photo");
  const dateInput = document.getElementById("wizard-date");
  const addressField = document.getElementById("wizard-address-field");
  const addressInput = document.getElementById("wizard-address");

  function cakeFromParam(raw) {
    if (!raw) return "";
    const key = ALIASES[String(raw).trim().toLowerCase()];
    return key && CAKES[key] ? key : "";
  }

  function isoDate(d) {
    const y = d.getFullYear();
    const m = String(d.getMonth() + 1).padStart(2, "0");
    const day = String(d.getDate()).padStart(2, "0");
    return y + "-" + m + "-" + day;
  }

  function minDate() {
    const d = new Date();
    d.setHours(12, 0, 0, 0);
    d.setDate(d.getDate() + 3);
    return isoDate(d);
  }

  function summaryText() {
    const c = CAKES[state.cakeKey];
    const lines = [
      "Hi White Cakes, I'd like to order a cake.",
      c ? "Cake: " + c.formValue : "",
      state.size ? "Size: " + state.size : "",
      state.flavor ? "Flavor: " + state.flavor : "",
      state.cakeMessage ? "Message on cake: " + state.cakeMessage : "",
      state.date ? "Date needed: " + state.date : "",
      "Fulfillment: " + state.fulfillment,
      state.fulfillment === "delivery" && state.address ? "Address: " + state.address : "",
      state.name ? "Name: " + state.name : "",
      state.phone ? "Phone: " + state.phone : "",
      state.notes ? "Notes: " + state.notes : "",
    ].filter(Boolean);
    return lines.join("\n");
  }

  function updatePreview() {
    const c = state.cakeKey ? CAKES[state.cakeKey] : null;
    const imgSrc =
      state.cakeKey === "custom" && state.customPreviewUrl
        ? state.customPreviewUrl
        : c
          ? c.image
          : "/assets/hero-celebration-cake-cebu.webp";

    if (previewImg) {
      previewImg.src = imgSrc;
      if (c) {
        previewImg.width = c.w;
        previewImg.height = c.h;
      }
    }
    if (previewCaption) {
      previewCaption.textContent = c
        ? c.caption + (state.size ? " · " + state.size : "")
        : "Pick a design to start";
    }
    if (previewMessage) {
      const text = state.cakeMessage.trim() || "Your message";
      previewMessage.textContent = text;
      previewMessage.hidden = !state.cakeKey;
      if (c) previewMessage.style.top = c.messageTop;
    }
    if (previewFlavor) {
      if (state.flavor) {
        previewFlavor.hidden = false;
        previewFlavor.textContent = state.flavor + " inside";
        previewFlavor.style.setProperty("--flavor-accent", FLAVOR_ACCENTS[state.flavor] || "var(--dust)");
      } else {
        previewFlavor.hidden = true;
      }
    }
    if (previewSize) {
      previewSize.textContent = state.size || "";
      previewSize.hidden = !state.size;
    }
    root.dataset.cake = state.cakeKey || "none";
    root.dataset.flavor = state.flavor ? state.flavor.toLowerCase().replace(/\s+/g, "-") : "";
  }

  function renderSizes() {
    const wrap = document.getElementById("size-options");
    if (!wrap || !state.cakeKey) return;
    const sizes = CAKES[state.cakeKey].sizes;
    wrap.innerHTML = "";
    sizes.forEach(function (sz) {
      const label = document.createElement("label");
      label.className = "pick-btn" + (state.size === sz ? " is-selected" : "");
      const input = document.createElement("input");
      input.type = "radio";
      input.name = "size_pick";
      input.value = sz;
      input.checked = state.size === sz;
      input.addEventListener("change", function () {
        state.size = sz;
        wrap.querySelectorAll(".pick-btn").forEach(function (el) {
          el.classList.toggle("is-selected", el.contains(input) && input.checked);
        });
        updatePreview();
        syncFormFields();
      });
      label.appendChild(input);
      label.appendChild(document.createTextNode(sz));
      wrap.appendChild(label);
    });
  }

  function setStep(n) {
    state.step = Math.max(1, Math.min(5, n));
    const stepNames = ["Design", "Size", "Flavor", "Message and date", "Details"];
    stepPanels.forEach(function (panel) {
      const s = Number(panel.getAttribute("data-step-panel"));
      panel.hidden = s !== state.step;
    });
    if (progress) {
      progress.querySelectorAll("[data-step-dot]").forEach(function (dot) {
        const s = Number(dot.getAttribute("data-step-dot"));
        dot.classList.toggle("is-active", s === state.step);
        dot.classList.toggle("is-done", s < state.step);
        dot.setAttribute("aria-label", "Step " + s + ": " + stepNames[s - 1]);
        if (s === state.step) dot.setAttribute("aria-current", "step");
        else dot.removeAttribute("aria-current");
      });
    }
    if (stepCount) stepCount.textContent = "Step " + state.step + " of 5 · " + stepNames[state.step - 1];
    btnBack.hidden = state.step === 1;
    btnNext.textContent = state.step === 5 ? "Send order" : "Continue";
    btnNext.type = state.step === 5 ? "submit" : "button";
    root.setAttribute("data-step", String(state.step));
    const scrollTarget = window.matchMedia("(max-width: 899px)").matches
      ? root.querySelector(".order-wizard-main")
      : root;
    const top = scrollTarget.getBoundingClientRect().top + window.scrollY - 76;
    window.scrollTo({ top: top, behavior: "smooth" });
  }

  function syncFormFields() {
    if (!form) return;
    const set = function (name, val) {
      const el = form.elements.namedItem(name);
      if (el && "value" in el) el.value = val || "";
    };
    const c = state.cakeKey ? CAKES[state.cakeKey] : null;
    set("cake", c ? c.formValue : "");
    set("size", state.size);
    set("flavor", state.flavor);
    set("message", state.cakeMessage);
    set("date", state.date);
    set("name", state.name);
    set("phone", state.phone);
    set("email", state.email);
    set("fulfillment", state.fulfillment);
    set("address", state.fulfillment === "delivery" ? state.address : "");
    set("notes", state.notes);
  }

  function validateStep() {
    if (state.step === 1 && !state.cakeKey) {
      status.textContent = "Choose a cake design to continue.";
      status.className = "form-status is-error";
      return false;
    }
    if (state.step === 2 && !state.size) {
      status.textContent = "Choose a size.";
      status.className = "form-status is-error";
      return false;
    }
    if (state.step === 3 && !state.flavor) {
      status.textContent = "Choose a flavor.";
      status.className = "form-status is-error";
      return false;
    }
    if (state.step === 4) {
      if (!state.date) {
        status.textContent = "Pick your cake date (at least 3 days ahead).";
        status.className = "form-status is-error";
        return false;
      }
      if (state.date < dateInput.min) {
        status.textContent = "Please choose a date at least 3 days from today.";
        status.className = "form-status is-error";
        return false;
      }
    }
    if (state.step === 5) {
      if (!state.name.trim() || !state.phone.trim()) {
        status.textContent = "Name and mobile number are required.";
        status.className = "form-status is-error";
        return false;
      }
      if (state.fulfillment === "delivery" && !state.address.trim()) {
        status.textContent = "Add a full delivery address.";
        status.className = "form-status is-error";
        return false;
      }
    }
    status.textContent = "";
    status.className = "form-status";
    return true;
  }

  /* Step 1: cake cards */
  root.querySelectorAll("[data-pick-cake]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      state.cakeKey = btn.getAttribute("data-pick-cake");
      const c = CAKES[state.cakeKey];
      state.size = c.defaultSize;
      root.querySelectorAll("[data-pick-cake]").forEach(function (b) {
        b.classList.toggle("is-selected", b === btn);
      });
      renderSizes();
      updatePreview();
      syncFormFields();
    });
  });

  /* Step 3: flavors */
  root.querySelectorAll("[data-pick-flavor]").forEach(function (el) {
    el.addEventListener("click", function () {
      state.flavor = el.getAttribute("data-pick-flavor");
      root.querySelectorAll("[data-pick-flavor]").forEach(function (b) {
        b.classList.toggle("is-selected", b === el);
      });
      updatePreview();
      syncFormFields();
    });
  });

  const msgInput = document.getElementById("wizard-cake-message");
  if (msgInput) {
    msgInput.addEventListener("input", function () {
      state.cakeMessage = msgInput.value.slice(0, 80);
      updatePreview();
      syncFormFields();
    });
  }

  if (dateInput) {
    dateInput.min = minDate();
    dateInput.addEventListener("change", function () {
      state.date = dateInput.value;
      syncFormFields();
    });
  }

  root.querySelectorAll('[name="fulfillment_pick"]').forEach(function (radio) {
    radio.addEventListener("change", function () {
      state.fulfillment = radio.value;
      addressField.hidden = radio.value !== "delivery";
      addressInput.required = radio.value === "delivery";
      syncFormFields();
    });
  });

  ["wizard-name", "wizard-phone", "wizard-email", "wizard-notes", "wizard-address"].forEach(
    function (id) {
      const el = document.getElementById(id);
      if (!el) return;
      el.addEventListener("input", function () {
        if (id === "wizard-name") state.name = el.value;
        if (id === "wizard-phone") state.phone = el.value;
        if (id === "wizard-email") state.email = el.value;
        if (id === "wizard-notes") state.notes = el.value;
        if (id === "wizard-address") state.address = el.value;
        syncFormFields();
      });
    }
  );

  if (photoInput) {
    photoInput.addEventListener("change", function () {
      const file = photoInput.files && photoInput.files[0];
      if (state.customPreviewUrl) URL.revokeObjectURL(state.customPreviewUrl);
      state.customPreviewUrl = file ? URL.createObjectURL(file) : "";
      updatePreview();
    });
  }

  btnBack.addEventListener("click", function () {
    validateStep();
    setStep(state.step - 1);
  });

  btnNext.addEventListener("click", function () {
    if (state.step === 5) return;
    if (!validateStep()) return;
    if (state.step === 1) renderSizes();
    setStep(state.step + 1);
  });

  if (btnWa) {
    const refreshWa = function () {
      btnWa.href = WA_BASE + encodeURIComponent(summaryText() || "Hi White Cakes, I'd like to order a cake");
    };
    refreshWa();
    ["input", "change", "click"].forEach(function (ev) {
      root.addEventListener(ev, refreshWa);
    });
  }

  let sending = false;
  form.addEventListener("submit", function (ev) {
    ev.preventDefault();
    if (state.step !== 5) {
      setStep(5);
      return;
    }
    if (!validateStep() || sending) return;
    state.name = document.getElementById("wizard-name").value.trim();
    state.phone = document.getElementById("wizard-phone").value.trim();
    state.email = document.getElementById("wizard-email").value.trim();
    state.notes = document.getElementById("wizard-notes").value.trim();
    state.address = document.getElementById("wizard-address").value.trim();
    syncFormFields();
    sending = true;
    btnNext.disabled = true;
    btnNext.textContent = "Sending…";
    status.textContent = "";
    fetch(FORM_URL, {
      method: "POST",
      body: new FormData(form),
      headers: { Accept: "application/json" },
    })
      .then(function (res) {
        if (!res.ok) throw new Error("fail");
        status.className = "form-status is-ok";
        status.textContent = "Thank you — we'll confirm within 24 hours.";
        form.classList.add("is-sent");
        setStep(5);
      })
      .catch(function () {
        sending = false;
        btnNext.disabled = false;
        btnNext.textContent = "Send order";
        status.className = "form-status is-error";
        status.textContent = "Couldn't send — try again or use WhatsApp.";
      });
  });

  const params = new URLSearchParams(window.location.search);
  const cakeParam = cakeFromParam(params.get("cake"));
  const sizeParam = params.get("size");
  if (cakeParam) {
    state.cakeKey = cakeParam;
    const c = CAKES[cakeParam];
    state.size = sizeParam || c.defaultSize;
    const btn = root.querySelector('[data-pick-cake="' + cakeParam + '"]');
    if (btn) btn.classList.add("is-selected");
    renderSizes();
  }

  updatePreview();
  syncFormFields();
  setStep(cakeParam ? 2 : 1);
})();
