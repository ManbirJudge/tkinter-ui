import random
from typing import Tuple, List
import colorsys

RGB = Tuple[int, int, int]
HSL = Tuple[float, float, float]


def rgb_to_hex(rgb: RGB) -> str:
	return '#%02x%02x%02x' % rgb


def rgb_to_hsl(rgb: RGB) -> HSL:
	return colorsys.rgb_to_hls(rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0)


def hsl_to_rgb(hls: HSL) -> RGB:
	rgb = colorsys.hls_to_rgb(hls[0], hls[1], hls[2])

	return int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)


def gen_random_color() -> RGB:
	return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


def gen_gradient(start: RGB, end: RGB, count: int) -> List[RGB]:
	assert count > 1

	delta_r = (end[0] - start[0]) / count
	delta_g = (end[1] - start[1]) / count
	delta_b = (end[2] - start[2]) / count

	gradient = []

	for i in range(count):
		gradient.append(
			(
				start[0] + int(delta_r * i),
				start[1] + int(delta_g * i),
				start[2] + int(delta_b * i)
			)
		)

	return gradient


def adjust_brightness(rgb: RGB, factor: float):
	hls = list(rgb_to_hsl(rgb))

	hls[1] = max(min(hls[1] * (1 + factor), 1.0), 0.0)

	# Convert back to RGB
	return hsl_to_rgb(tuple(hls))


def darken(rgb: RGB, factor: float = 0.1):
	return adjust_brightness(rgb, -factor)


def lighten(rgb: RGB, factor: float = 0.1):
	return adjust_brightness(rgb, factor)


def is_dark(color: RGB) -> bool:
	luminance = 0.2126 * color[0] + 0.7152 * color[1] + 0.0722 * color[2]

	return luminance < 128
