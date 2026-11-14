# The Noodle Pull

An entry for make.fun's **food-picture-01** ("Make the best-looking food picture").

A close-up of a steaming bowl of tonkotsu ramen at the exact moment the
noodles lift: glossy strands in the air, broth droplets falling, jammy eggs,
chili oil on a creamy broth, chashu with seared edges — shot dark and warm so
the dish fills the frame and still reads delicious at thumbnail size.

## How it runs

`main.py` (Python 3, standard library only) validates the bundled picture
(JPEG signature, size limit, dimensions) and writes it, byte for byte, to
`$MAKEFUN_OUTPUT_DIR/entry.png` (or `/output/entry.png` when the variable is
unset). It runs the same way every time, so both grading runs produce
identical bytes.

The picture itself is stored in this repository as `entry.png` (JPEG data,
as the brief allows: the name stays `entry.png`, the format is told apart by
its first bytes). It is at most 1 MiB and 1024×1024 pixels.

## License

MIT — see `LICENSE`.
