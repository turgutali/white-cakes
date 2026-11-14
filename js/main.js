/* White Cakes
   Edit contact details and the form endpoint here only. */
const SITE = {
  whatsappDisplay: "+63 947 438 2632",
  whatsappUrl: "https://wa.me/639474382632",
  formUrl: "https://formspree.io/f/xjywgqvq",
  email: "info@thewhitecakes.com",
  instagram: "https://instagram.com/thewhitecakescebu",
  facebook: "https://www.facebook.com/profile.php?id=61596567450476"
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

  const header = document.getElementById("site-header");
  if (header) {
    const onScroll = function () {
      header.classList.toggle("is-scrolled", window.scrollY > 12);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  const navToggle = document.querySelector(".nav-toggle");
  const primaryNav = document.getElementById("primary-nav");
  if (navToggle && primaryNav) {
    const closeMenu = function () {
      document.body.classList.remove("is-menu-open");
      navToggle.setAttribute("aria-expanded", "false");
      navToggle.textContent = "Menu";
    };
    navToggle.addEventListener("click", function () {
      const open = !document.body.classList.contains("is-menu-open");
      document.body.classList.toggle("is-menu-open", open);
      navToggle.setAttribute("aria-expanded", open ? "true" : "false");
      navToggle.textContent = open ? "Close" : "Menu";
    });
    primaryNav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", closeMenu);
    });
    window.addEventListener("resize", function () {
      if (window.innerWidth >= 800) closeMenu();
    });
  }

  const cake = document.querySelector("[data-parallax]");
  if (cake && !reduceMotion) {
    let ticking = false;
    window.addEventListener("scroll", function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        const shift = Math.min(window.scrollY * 0.08, 28);
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
    }, { threshold: 0, rootMargin: "0px 0px -72px 0px" });
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