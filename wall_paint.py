import cv2
import numpy as np
import math


class Selection_Mode:

    def __init__(self, name, image, select_mode='Polygon'):
        self.name = name
        self.image = image
        self.color = None
        self.out_image = self.image.copy()
        self.flood_image = self.image.copy()
        self.height, self.width = self.image.shape[:2]
        self.mask = np.zeros((self.height, self.width), np.uint8)
        self.contour_mask = np.zeros((self.height, self.width), np.uint8)
        self.flooded_mask = np.zeros((self.height + 2, self.width + 2), np.uint8)
        self.px = None
        self.first_px = None
        self.temp_px = None
        self.draw = False
        self.points = []
        self.tolerance = (20,) * 3
        self.selection = self.image.copy()
        self.select_mode = select_mode

    def set_tolerance(self, tol):
        self.tolerance = (tol,) * 3
        self.magic_hand()

    def mouse_location(self, event, x, y, flag, param):
        if self.select_mode == 'MagicTool':
            if event == cv2.EVENT_LBUTTONDOWN:
                self.px = x, y
                self.mask = cv2.bitwise_or(self.mask, self.flooded_mask[1:-1, 1:-1].copy())
                self.magic_hand()
        elif self.select_mode == 'Polygon':
            if self.draw is False and event == cv2.EVENT_LBUTTONDOWN:
                self.px = x, y
                self.first_px = x, y
                self.temp_px = x, y
                self.draw = True
                self.points.append(self.px)
            elif self.draw is True and event == cv2.EVENT_LBUTTONDOWN:
                self.px = x, y
                self.points.append(self.px)
                cv2.line(self.selection, self.temp_px, self.px, (0, 0, 255), thickness=1)
                self.temp_px = x, y
                cv2.imshow(self.name, self.selection)
            elif self.draw is True and event == cv2.EVENT_RBUTTONDOWN:
                cv2.line(self.selection, self.temp_px, self.first_px, (0, 0, 255), thickness=1)
                cv2.imshow(self.name, self.selection)
                self.draw = False
                self.polygon()

    def magic_hand(self):
        self.flooded_mask[:] = 0
        self.flood_image = self.image.copy()
        cv2.floodFill(self.flood_image, self.flooded_mask, self.px, 0, self.tolerance, self.tolerance,
                      cv2.FLOODFILL_FIXED_RANGE)
        self.contour_mask = cv2.bitwise_or(self.mask, self.flooded_mask[1:-1, 1:-1].copy())
        self.draw_contours()

    def polygon(self):
        poly = np.array([self.points])
        del self.points[:]
        cv2.fillPoly(self.mask, poly, 1)
        self.draw_contours()

    def draw_contours(self):
        self.out_image = self.image.copy()
        if self.select_mode == 'MagicTool':
            temp_mask = self.contour_mask
        elif self.select_mode == 'Polygon':
            temp_mask = self.mask
        contours, hierarchy = cv2.findContours(temp_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(self.out_image, contours, -1, color=(0, 0, 255))
        self.out_image = cv2.addWeighted(self.image, 0.75, self.out_image, 0.25, 0)
        cv2.drawContours(self.out_image, contours, -1, color=(0, 0, 255))
        cv2.imshow(self.name, self.out_image)

    def show_image(self):
        cv2.namedWindow(self.name)
        cv2.setMouseCallback(self.name, self.mouse_location)
        cv2.imshow(self.name, self.out_image)
        if self.select_mode == 'MagicTool':
            cv2.createTrackbar('Tolerance', self.name, 10, 255, self.set_tolerance)

    def set_select_mode(self, select_mode):
        self.select_mode = select_mode
        self.refresh()
        cv2.destroyWindow(self.name)
        self.show_image()

    def get_out_image(self):
        return self.out_image

    def get_mask(self):
        return self.mask

    def refresh(self):
        self.mask = cv2.bitwise_or(self.mask, self.flooded_mask[1:-1, 1:-1].copy())

    def change_mode(self, mode):
        self.select_mode = mode
        cv2.destroyAllWindows()
        self.show_image()


class Blending_Mode:

    def __init__(self, name, image, mask, blend=None, blend_mode='Normal', blend_type='Color'):
        self.name = name
        self.image = image
        self.height, self.width = self.image.shape[:2]
        self.mask = mask
        self.blend = blend
        self.blend_mode = blend_mode
        self.blend_type = blend_type
        self.out_image = self.image.copy()
        self.final_image = self.out_image.copy()
        self.opacity = 100
        self.blend_image = np.full((self.height, self.width, 3), 0, np.uint8)

    def set_blend(self, blend):
        self.blend = blend
        if self.blend_type == 'Color':
            self.blend_image[:] = self.blend
        elif self.blend_type == 'Texture':
            self.fix_texture()

    def update_mask(self, mask):
        self.mask = mask

    def set_blend_mode(self, mode):
        print(mode)
        self.blend_mode = mode

    def start_blending(self):
        if self.blend_mode == 'Normal':
            self.normal_blend()
        elif self.blend_mode == 'Addition':
            self.addition_blend()
        elif self.blend_mode == 'Divide':
            self.divide_blend()
        elif self.blend_mode == 'Subtract':
            self.subtract_blend()
        elif self.blend_mode == 'Multiply':
            self.multiply_blend()
        elif self.blend_mode == 'Darken':
            self.darken_blend()
        elif self.blend_mode == 'Screen':
            self.screen_blend()
        elif self.blend_mode == 'Lighten':
            self.lighten_blend()
        elif self.blend_mode == 'Overlay':
            self.overlay_blend()
        elif self.blend_mode == 'Soft Light':
            self.soft_light_blend()
        elif self.blend_mode == 'Hard Light':
            self.hard_light_blend()
        self.final_image = self.out_image

    def show_out_image(self):
        cv2.namedWindow(self.name)
        cv2.imshow(self.name, self.final_image)
        cv2.createTrackbar('Opacity', self.name, self.opacity, 100, self.set_opacity)

    def get_out_image(self):
        return self.final_image

    def set_opacity(self, opacity):
        self.opacity = opacity
        self.final_image = cv2.addWeighted(self.out_image, self.opacity / 100, self.image, 1 - self.opacity / 100, 0)
        self.show_out_image()

    def fix_texture(self):
        out_texture = self.blend.copy()
        blend_height, blend_width = self.blend.shape[:2]
        self.height, self.width = self.image.shape[:2]
        height_ratio = self.height / blend_height
        width_ratio = self.width / blend_width
        fixed_height_ratio = math.ceil(height_ratio)
        fixed_width_ratio = math.ceil(width_ratio)
        if blend_height >= self.height:
            fixed_height_ratio = 0
        if blend_width >= self.width:
            fixed_width_ratio = 0
        q = 0
        while q < fixed_width_ratio - 1:
            out_texture = cv2.hconcat([out_texture, self.blend])
            q += 1
        q = 0
        while q < fixed_height_ratio - 1:
            out_texture = cv2.vconcat([out_texture, out_texture])
            q += 1
        out_texture = out_texture[0:self.height, 0:self.width]
        self.blend_image = out_texture.copy()

    def paint_texture_with(self, texture_color):
        Y = cv2.cvtColor(self.blend_image, cv2.COLOR_BGR2GRAY)
        color = np.full((self.height, self.width, 3), 0, np.uint8)
        color[:] = texture_color
        color = cv2.cvtColor(color, cv2.COLOR_BGR2YCR_CB)
        Cr = color[:, :, 1]
        Cb = color[:, :, 2]
        self.blend_image = cv2.cvtColor(self.blend_image, cv2.COLOR_BGR2YCR_CB)
        self.blend_image = cv2.merge([Y, Cr, Cb])
        self.blend_image = cv2.cvtColor(self.blend_image, cv2.COLOR_YCR_CB2BGR)


    def normal_blend(self):
        self.out_image = self.image.copy()
        for x in range(self.width):
            for y in range(self.height):
                if self.mask[y, x] == 1:
                    self.out_image[y, x] = self.blend_image[y, x]

    def addition_blend(self):
        self.out_image = self.image.copy()
        for x in range(self.width):
            for y in range(self.height):
                if self.mask[y, x] == 1:
                    for c in range(3):
                        if np.add(self.image[y, x, c], self.blend_image[y, x, c], dtype=np.uint16) > 255:
                            self.out_image[y, x, c] = 255
                        else:
                            self.out_image[y, x, c] = np.add(self.image[y, x, c], self.blend_image[y, x, c], casting='unsafe')

    def divide_blend(self):
        self.out_image = self.image.copy()
        for x in range(self.width):
            for y in range(self.height):
                if self.mask[y, x] == 1:
                    for c in range(3):
                        if self.image[y, x, c] > self.blend_image[y, x, c]:
                            self.out_image[y, x, c] = 255
                        else:
                            self.out_image[y, x, c] = np.divide(255 * self.image[y, x, c], self.blend_image[y, x, c], casting='unsafe')

    def subtract_blend(self):
        self.out_image = self.image.copy()
        for x in range(self.width):
            for y in range(self.height):
                if self.mask[y, x] == 1:
                    for c in range(3):
                        if self.image[y, x, c] < self.blend_image[y, x, c]:
                            self.out_image[y, x, c] = 0
                        else:
                            self.out_image[y, x, c] = np.subtract(self.image[y, x, c], self.blend_image[y, x, c], casting='unsafe')

    def multiply_blend(self):
        self.out_image = self.image.copy()
        for x in range(self.width):
            for y in range(self.height):
                if self.mask[y, x] == 1:
                    for c in range(3):
                        self.out_image[y, x, c] = np.multiply(self.image[y, x, c], self.blend_image[y, x, c]/255, casting='unsafe')

    def darken_blend(self):
        self.out_image = self.image.copy()
        print(self.blend_mode)
        for x in range(self.width):
            for y in range(self.height):
                if self.mask[y, x] == 1:
                    for c in range(3):
                        if self.image[y, x, c] < self.blend_image[y, x, c]:
                            self.out_image[y, x, c] = self.image[y, x, c]
                        else:
                            self.out_image[y, x, c] = self.blend_image[y, x, c]

    def screen_blend(self):
        self.out_image = self.image.copy()
        for x in range(self.width):
            for y in range(self.height):
                if self.mask[y, x] == 1:
                    self.out_image[y, x, 0] = 255 - (255 - self.image[y, x, 0]) * (
                            255 - self.blend_image[y, x, 0]) / 255
                    self.out_image[y, x, 1] = 255 - (255 - self.image[y, x, 1]) * (
                            255 - self.blend_image[y, x, 1]) / 255
                    self.out_image[y, x, 2] = 255 - (255 - self.image[y, x, 2]) * (
                            255 - self.blend_image[y, x, 2]) / 255

    def lighten_blend(self):
        self.out_image = self.image.copy()
        for x in range(self.width):
            for y in range(self.height):
                if self.mask[y, x] == 1:
                    for c in range(3):
                        if self.image[y, x, c] > self.blend_image[y, x, c]:
                            self.out_image[y, x, c] = self.image[y, x, c]
                        else:
                            self.out_image[y, x, c] = self.blend_image[y, x, c]

    def overlay_blend(self):
        self.out_image = self.image.copy()
        for x in range(self.width):
            for y in range(self.height):
                if self.mask[y, x] == 1:
                    for c in range(3):
                        if self.image[y, x, c] < 128:
                            self.out_image[y, x, c] = 2 * (self.image[y, x, c]) * (self.blend_image[y, x, c]) / 255
                        else:
                            self.out_image[y, x, c] = 255 - 2 * (255 - self.image[y, x, c]) * (
                                    255 - self.blend_image[y, x, c]) / 255

    def soft_light_blend(self):
        self.out_image = self.image.copy()
        for x in range(self.width):
            for y in range(self.height):
                if self.mask[y, x] == 1:
                    for c in range(3):
                        if self.blend_image[y, x, c] < 127:
                            self.out_image[y, x, c] = (2 * self.image[y, x, c] * self.blend_image[y, x, c]) / 255 + (((self.image[y, x, c] ** 2)/255) * (255 - 2 * self.blend_image[y, x, c]))/255
                        else:
                            self.out_image[y, x, c] = 2 * (self.image[y, x, c] * (255 - self.blend_image[y, x, c]))/255 + (math.sqrt(self.image[y, x, c]) * (2 * self.blend_image[y, x, c] - 255)) / (math.sqrt(255))

    def hard_light_blend(self):
        self.out_image = self.image.copy()
        for x in range(self.width):
            for y in range(self.height):
                if self.mask[y, x] == 1:
                    for c in range(3):
                        if self.blend_image[y, x, c] < 127:
                            self.out_image[y, x, c] = 2 * (self.image[y, x, c]) * (self.blend_image[y, x, c]) / 255
                        else:
                            self.out_image[y, x, c] = 255 - 2 * (255 - self.image[y, x, c]) * (
                                    255 - self.blend_image[y, x, c]) / 255
