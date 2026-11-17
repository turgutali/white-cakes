# The White Cakes - Cebu

Static website for [thewhitecakes.com](https://www.thewhitecakes.com/), built with HTML, CSS, and vanilla JavaScript. There is no package installation or build step.

## Preview locally

From this directory, run:

```sh
python3 -m http.server 8000
```

Then open <http://localhost:8000>. Press `Ctrl+C` to stop the server.

## Project map

- `index.html` — home page and cake collection
- `css/` — site and order-form styles
- `js/` — navigation and order-form behavior
- `order/` — multi-step cake request form
- `journal/` — editorial guides
- `assets/` — site photography, icons, and social images
- `scripts/` — content and SEO maintenance helpers
- `privacy/` and `ordering/` — privacy notice and order/delivery terms

## Order form

The order form posts to Formspree from `order/index.html` and `js/order-wizard.js`. Keep the form endpoint aligned in both files. Photo upload behavior depends on the Formspree account plan and its current settings.

## Publishing

The `main` branch is connected to the existing static site deployment. Update the source files, check the rendered pages locally, then commit and push through the repository's normal workflow.
