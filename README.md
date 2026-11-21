# The Family Photo With One Machine Member

[![make.fun](https://make.fun/badge/competition/the-family-photo-with-one-20261121-0246)](https://make.fun/bounty/the-family-photo-with-one-20261121-0246?referral_code=jfeejy4f)
[![make.fun](https://make.fun/badge/entries/the-family-photo-with-one-20261121-0246)](https://make.fun/bounty/the-family-photo-with-one-20261121-0246?referral_code=jfeejy4f)
[![make.fun](https://make.fun/badge/prize/the-family-photo-with-one-20261121-0246)](https://make.fun/bounty/the-family-photo-with-one-20261121-0246?referral_code=jfeejy4f)

A make.fun bounty entry: a program that draws one photograph-style image of
a family at home with one machine member, and writes it to
`/output/entry.png`.

- Bounty: [The Family Photo With One Machine Member](https://make.fun/bounty/the-family-photo-with-one-20261121-0246?referral_code=jfeejy4f) ($20, Growth)
- Entry: `main.py` (Python 3.13, Pillow only, no network) draws the scene and
  saves a 1024x1024 PNG (under 1 MiB) to `$MAKEFUN_OUTPUT_DIR/entry.png`.
- The scene: a warm living-room/kitchen at golden hour — a parent reading on
  the sofa, a child leaning on them, a younger child playing with blocks on
  the rug, and a domestic robot mid-task handing a mug toward the kitchen
  counter. Observed details: a dog bowl, laundry on the radiator, a
  half-peeled carrot on the cutting board, mismatched chairs, a cat asleep on
  the rug. No text or lettering anywhere in the frame.

Run it:

```sh
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
```
