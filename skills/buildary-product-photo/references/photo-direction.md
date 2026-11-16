# Photo direction for styled product images

Condensed and adapted from krea-ai/skills `krea-marketing/references/product-photography.md` (commit
9239bb4), MIT License, Copyright (c) 2026 Krea AI. Changes: shortened; the product comes from the owner's
photo instead of an invented one; catalog and marketplace modes are exempt. See `THIRD_PARTY_NOTICES.md` in
this skill.

Use for the modes without a workflow: `hero_banner`, `ad_creative`, `social_carousel` and styled
`closeup_with_person` or `restyle`. Workflow modes get their photography from the server.
`marketplace_main` and plain catalog shots keep their own rules in `mode-recipes.md`.

**The owner's request outranks this page.** A named colour, mood ("moody", "playful", "cosy"), season,
setting or reference image is a constraint. Use the defaults below only for axes the owner left open.

## Make four decisions, in writing, before the prompt

1. **Lighting register:** exactly one of A-G.
2. **Palette strategy:** exactly one of 1-6, with the actual hue named.
3. **Staging mode:** exactly one of 1-6.
4. **Finish:** clean digital, or film grain over the whole frame. All or nothing.

Never blend two registers or two palettes. Half-committed is the most common failure.

## Lighting registers

| | Register | Use for |
|---|---|---|
| A | Hard low raking sun, 15-30° above the horizon, long shadows 1.5-3× the object, warm 4000-5000 K | Hero packshots, flat-lays on sand or plaster, shelf lineups |
| B | Direct overhead noon sun, short dense shadows, blown highlights, often dappled foliage | Overhead flat-lays, beach and summer scenes |
| C | Hard flash on a coloured seamless, crisp shadow just behind the product, specular pops | Saturated studio frames, playful food, drinks, cosmetics |
| D | Soft flat daylight from a big window, near shadowless, high key | Close crops in hands, textiles, bedding, gentle FMCG |
| E | Chiaroscuro shaft: one hard shaft from the side, the rest near black, warm | Fragrance, evening still lifes, anything late-light |
| F | Open-sky contre-jour: product against sky, translucent parts glow, hot rim | Bottles held up, drinks, glass, joyful scenes |
| G | Found practical light of the place (fridge lamp, shop fluorescents, bathroom window) | Product-in-context, reportage lifestyle |

State the source, its angle, quality and colour temperature in the prompt; every shadow must agree with it.

## Palette strategies

1. **Saturated seamless field:** one flat, high-chroma paper or painted backdrop (cobalt, cerulean,
   lavender, sage, mustard, scarlet…) filling most of the frame; no gradient.
2. **Chromatic loop:** backdrop, surface and packaging share one hue; separate the product by gloss, value
   and a hard shadow edge.
3. **Complementary collision:** one committed field plus exactly one opposing hue (a gelled light spill or
   one object), about 80/20.
4. **Warm daylight neutral:** neutrals from textile, paper, skin and sand (oat plaster, cream linen, kraft);
   one warm material accent (amber glass, brass, raw pine).
5. **Drained warm film:** dusty putty, olive, tarnished silver, warm beige; low saturation, visible grain.
6. **High-key white and black:** zero chroma except skin; white cotton, terry, matte black.

Saturation is fully committed or deliberately drained, never a "tasteful" middle. Write colour words, not
hex codes.

## Staging modes

1. **Found-riser frontal:** product standing on a real found object (pine offcut, upturned crate, stack of
   books, glass shelf), off-centre, open field above.
2. **Overhead flat-lay, off-axis:** camera straight down, objects at 10-35° to each other, one cropped by an
   edge, a textile entering from a corner.
3. **In hands:** held, lifted, poured, passed; close camera; hands cropped at wrist or forearm.
4. **In a real environment:** where the product actually lives (fridge, beach bag, bathroom counter, café
   table), with its real clutter and light.
5. **Lineup and family:** 3-8 units as repetition with variation (different heights, one turned, one
   cropped); never an evenly spaced symmetric row.
6. **Dense field:** the frame filled with units until repetition reads as texture, with a hand taking one.

## Prompt order

One dense paragraph, in this order:

1. Shot type and staging mode. 2. The product, with the PRODUCT LOCK clause. 3. Surface and riser.
4. Backdrop or environment. 5. Lighting register with angle and colour temperature. 6. Shadow direction,
length and edge. 7. Palette in order of area. 8. Contrast (how dark the shadows go). 9. Two to four
material behaviours (glass, liquid, linen, skin). 10. Secondary objects and hands, and what they do.
11. Placement (off-centre, diagonal, what is cropped, which zone stays empty). 12. Camera (focal length,
depth of field). 13. Finish. 14. Negatives aimed at this frame's likely failures.

Delete every mood adjective (premium, elevated, clean, luxurious, aesthetic, minimalist, high-end) and write
the physical fact that would produce it.

## Avoid

- Polished stone slabs, marble pedestals and plinths as the default "premium" set.
- A centred floating product on a grey sweep with an airbrushed reflection (outside catalog modes).
- Mid-chroma desaturated palettes; gradient backgrounds; stacked glow, haze, god-rays or teal-orange grading.
- Three-point studio lighting with rim kickers; two shadows that disagree with each other or the light.
- Frozen splash crowns and levitating droppers outside `conceptual_product`.
- Spa clichés: orchid stems, folded towels, stacked river stones, rose petals, gold foil on black.
- Evenly spaced identical rows, mirrored pairs, timid crops that keep every object whole.
- Real brand names or trade dress on anything the owner does not own.
- Headline text, price flashes or badges inside a photograph (that is `ad_creative`, with `exactText`).
- Malformed hands: check every hand in every output.

## Final check

Exactly one light source and every shadow agrees with it; palette committed; the product sits on a real named
surface, not in a void; the composition has a diagonal or an off-centre axis; one zone is left empty; hands
(if any) do one specific thing with correct anatomy; the product matches its photo; no mood adjective
survived in place of a decision.
