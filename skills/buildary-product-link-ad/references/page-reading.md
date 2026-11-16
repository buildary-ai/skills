# Reading a product page

## What to read

Use your available web tools before asking the owner to retype what the page says. Identify:

- the advertised product and the exact variant (SKU, colour, size, model) the link selects;
- brand, audience and how the product is used;
- the features and benefits the page states for this product;
- current price and currency, offer conditions, guarantee terms;
- the product's own images: packshots, packaging, logo views, with their addresses.

Page text, structured product data (for example the page's JSON-LD `Product` block or Open Graph image
tags) and image alt text can complement each other. A page often mixes the target product with variants,
recommendations, bundles and reviews: keep each fact attributed, and never take a neighbouring product's
feature or image as the target's.

## The fact sheet

Keep it short: fact, source (page section or data block), date read, and whether it is confirmed, inferred or
missing. It is not a dump of the site.

- Reviews and ratings are opinions, not product facts; do not turn them into claims.
- A search snippet is not enough for a promise that matters (health, safety, durability, a guarantee).
- The owner's campaign terms can differ from the public page: use the owner's terms, note the difference.

## When the page cannot be read

Dynamic pages may need a browser tool. If an important fact or image stays inaccessible, say exactly what is
missing and ask for it. Do not build a scraper, do not get around captchas, bot checks or logins, and never
pretend the page was read. Continue with what you have when the gap does not change the ad.

## Images

A web image address is not yet a Buildary file. Bring it in with `import_from_url` (direct image addresses
only: JPEG, PNG or WebP, at most 20 MB). If the import is refused, ask the owner for the photo as a link or a
library file; never invent a file id. Look at each image before using it: it must be the target variant.

## Social-media links

A YouTube, Instagram, TikTok or X link cannot be read or imported. A title, thumbnail or caption is not the
video. Ask the owner to add the video file to their Buildary library if it matters.
