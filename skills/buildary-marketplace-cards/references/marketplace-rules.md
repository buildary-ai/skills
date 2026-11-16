# Marketplace image rules (sourced)

Every rule below comes from the marketplace's own seller documentation, read on 15 November 2026. A rule
that has no official source is not listed. Marketplaces change their rules: when the owner reports a
rejection or the source page has changed, re-read the source and update this file.

## Trendyol

Source: Trendyol Satıcı Bilgi Merkezi, "Ürün Görseli Seçimi ve Yükleme",
https://akademi.trendyol.com/satici-bilgi-merkezi/detay/urun-gorseli-secimi-ve-yukleme

Image requirements:
- The whole product is clearly visible and covers most of the image area.
- Only the variant on sale (colour / model / size); other colours or models of the product are not in the
  main images.
- A plain white or light background is preferred.
- The photo is sharp, clear and well lit.
- The main image shows the product straight on and plainly. Other angles, size or package contents, and
  usage go in the helper (yardımcı) images.

Technical: JPEG, JPG, PNG or WEBP; 1 KB to 10 MB; resolution at least 860 × 574 px and at most
2000 × 2000 px.

Not accepted:
- low-resolution, blurry, dark or cropped images;
- images with excessive text;
- a logo or watermark unrelated to the product;
- images heavily edited in Photoshop or that look artificial;
- shipping, return, campaign, price, discount or gift information on the image;
- images that contradict the brand entered for the product;
- products or accessories not in the package (allowed for clarity only if clearly marked as not included);
- links to other sites or seller information.

Also: representative (temsili) images may not be used to open a product and then be swapped for another
product's images.

## Hepsiburada

Source: Hepsiburada Developer Portal, "Katalog Ürün Giriş Önemli Bilgiler" → "Gönderilecek Olan Görsellerde
Dikkat Edilmesi Gereken Kurallar" (updated 4 June 2026),
https://developers.hepsiburada.com/tr/companies/hepsiburada?product=katalog-urun-entegrasyonu&guide=katalog-onemli-bilgiler&view=guide

- The background is white or a light colour.
- No text (such as "kargo bedava", "aynı gün kargo"), logo or watermark in the image.
- Not a graphic drawing; not low quality or blurry.
- The first image usually shows the product out of its packaging, with all its features distinguishable.
- Not several views or angles in one image so that the product gets small.
- Not inside a frame.
- The product covers 80% of the image.
- Usually no items that are not part of the product (lifestyle images excepted).
- After the white background is removed, at least one side of what remains is 250 px or more.
- Only the product on sale; no other colours or patterns unless they are part of the product.

Same source, "Ürün Bilgisi Gönderme": images are sent as `Image1`…`Image5`; formats PNG and JPG.

## Amazon Türkiye

Source: Amazon Seller Central Türkiye, "Product image guide",
https://sellercentral.amazon.com.tr/help/hub/reference/external/G1881

Technical: JPEG (recommended), TIFF, PNG or non-animated GIF; at least 500 px and at most 10,000 px on the
longest side (1,000 px or more recommended; it enables zoom); at least 72 dpi; RGB preferred. Amazon
recommends at least six additional images and one video.

Main (MAIN) image:
- A realistic, professional image that shows the real scale, quantity and colour.
- The product fills 85% of the image, entirely inside the frame, shown once (not front and back together).
- One unit of the product plus the accessories included with it.
- Pure white background (RGB 255, 255, 255). Only some product types may use a lifestyle main image.
- No packaging unless it is an important product feature; no props that are not included; no mannequin.
- Footwear: a single shoe facing left at 45 degrees. Adult clothing: on a standing model.

All images:
- Accurately represent the product and match its title.
- No customer reviews, star imagery, claims such as free shipping, or seller-specific information.
- "No text or pricing details (swatch image only)."
- No Amazon logos, trademarks or badges (for example "Amazon's Choice", "Best seller").

Photorealistic AI-generated people: tag the image file with the keyword `contains-synthetic-performer` in the
XMP `dc:subject` field before uploading. Not needed for real people (even AI-edited), non-photorealistic
people, or images without people.

## What follows for the card types

| Card | Trendyol | Hepsiburada | Amazon TR |
|---|---|---|---|
| Main image | Straight-on, plain, white or light background, no text | White or light background, product 80%, no text or logo, out of packaging | Pure white, product 85%, no text, one unit |
| Multi-angle (one angle per image) | Helper image | Allowed; never several angles in one image | Allowed (angle shots) |
| Detail / close-up | Helper image | Allowed | Allowed |
| Package contents | Helper image; mark anything not included | Only items that are part of the product | Allowed; no props that are not included |
| Size / measurements with labels | Helper image; keep text short | Not with text (no text allowed) | Allowed; no claims |
| Lifestyle / in use | Helper image | Allowed (the source exempts lifestyle images from the extra-items rule) | Allowed as an additional image |
| Feature card with Turkish text | Only short text; no campaign, price, shipping or discount | Not allowed (no text) | No claims, reviews, ratings or seller information |

Rows "Allowed" mean the source names no prohibition for that card; the marketplace's own review decides.
