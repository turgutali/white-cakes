/* White Cakes
   Edit contact details and the form endpoint here only. */
const SITE = {
  whatsappDisplay: "+63 9XX XXX XXXX",
  whatsappUrl: "https://wa.me/639XXXXXXXXX",
  formUrl: "https://formspree.io/f/YOUR_FORM_ID",
  email: "info@thewhitecakes.com",
  instagram: "https://instagram.com/thewhitecakes",
  facebook: "https://facebook.com/thewhitecakes"
};

(function () {
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  document.querySelectorAll("[data-wa]").forEach(function (link) {
    link.href = SITE.whatsappUrl;
  });

  document.querySelectorAll("[data-wa-label]").forEach(function (node) {
    node.textContent = SITE.whatsappDisplay;
  });

  document.querySelectorAll("[data-ig]").forEach(function (link) {
    link.href = SITE.instagram;
  });

  document.querySelectorAll("[data-fb]").forEach(function (link) {
    link.href = SITE.facebook;
  });

  const cake = document.querySelector("[data-parallax]");
  if (cake && !reduceMotion) {
    let ticking = false;
    window.addEventListener("scroll", function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        const shift = Math.min(window.scrollY * 0.12, 36);
        cake.style.transform = "translate3d(0," + shift.toFixed(2) + "px,0)";
        ticking = false;
      });
    }, { passive: true });
  }

  const dock = document.querySelector(".dock");
  const order = document.querySelector("#order");
  if (dock && order && "IntersectionObserver" in window) {
    const watcher = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        dock.classList.toggle("is-hidden", entry.isIntersecting);
      });
    }, { threshold: 0, rootMargin: "0px 0px -64px 0px" });
    watcher.observe(order);
  }

  const form = document.getElementById("order-form");
  if (!form) return;

  form.action = SITE.formUrl;

  const cakeSelect = document.getElementById("cake");
  const sizeSelect = document.getElementById("size");

  function setSelect(select, value) {
    if (!select || !value) return;
    for (let i = 0; i < select.options.length; i++) {
      const option = select.options[i];
      if (option.value === value || option.text === value) {
        select.value = option.value;
        return;
      }
    }
  }

  function preselect(cake, size) {
    setSelect(cakeSelect, cake);
    if (size) setSelect(sizeSelect, size);
    else if (sizeSelect) sizeSelect.value = "";
  }

  document.querySelectorAll("[data-order-cake]").forEach(function (link) {
    link.addEventListener("click", function () {
      preselect(link.getAttribute("data-order-cake"), link.getAttribute("data-order-size"));
    });
  });

  const params = new URLSearchParams(window.location.search);
  if (params.get("cake") || params.get("size")) {
    preselect(params.get("cake"), params.get("size"));
  }

  const dateInput = document.getElementById("date-needed");
  const addressWrap = document.getElementById("address-field");
  const addressInput = document.getElementById("address");
  const status = document.getElementById("form-status");
  const submitBtn = form.querySelector('button[type="submit"]');
  let sending = false;

  function isoDate(date) {
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");
    return date.getFullYear() + "-" + month + "-" + day;
  }

  function applyMinDate() {
    const min = new Date();
    min.setHours(12, 0, 0, 0);
    min.setDate(min.getDate() + 3);
    dateInput.min = isoDate(min);
  }

  function syncDateValidity() {
    if (dateInput.value && dateInput.value < dateInput.min) {
      dateInput.setCustomValidity("Please choose a date at least 3 days from today.");
    } else {
      dateInput.setCustomValidity("");
    }
  }

  function syncFulfillment() {
    const selected = form.querySelector('input[name="fulfillment"]:checked');
    const delivery = selected && selected.value === "delivery";
    addressWrap.hidden = !delivery;
    addressInput.required = delivery;
    addressInput.disabled = !delivery;
  }

  applyMinDate();
  syncDateValidity();
  syncFulfillment();

  dateInput.addEventListener("input", syncDateValidity);
  dateInput.addEventListener("change", syncDateValidity);
  form.querySelectorAll('input[name="fulfillment"]').forEach(function (radio) {
    radio.addEventListener("change", syncFulfillment);
  });

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    if (sending) return;

    applyMinDate();
    syncDateValidity();
    syncFulfillment();

    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }

    sending = true;
    submitBtn.disabled = true;
    submitBtn.textContent = "Sending…";
    status.textContent = "";
    status.className = "form-status";

    fetch(SITE.formUrl, {
      method: "POST",
      body: new FormData(form),
      headers: { Accept: "application/json" }
    })
      .then(function (response) {
        if (!response.ok) throw new Error("Form was not accepted");
        form.classList.add("is-sent");
        status.className = "form-status is-ok";
        status.textContent = "Thank you — we'll confirm your order within 24 hours.";
        status.tabIndex = -1;
        status.focus();
      })
      .catch(function () {
        sending = false;
        submitBtn.disabled = false;
        submitBtn.textContent = "Send order";
        status.className = "form-status is-error";
        status.textContent = "We couldn’t send your order. Your details are still here — please try again, or message us on WhatsApp.";
      });
  });
})();
