import re
import tkinter as tk
from tkinter import font

class CssParser:
    def __init__(self):
        self.styles = {}
        self.color_names = {
            'red': '#FF0000',
            'green': '#00FF00',
            'blue': '#0000FF',
            'black': '#000000',
            'white': '#FFFFFF',
            'yellow': '#FFFF00',
            'cyan': '#00FFFF',
            'magenta': '#FF00FF',
        }
        self.css_to_tkinter = {
            'background-color': 'bg',
            'color': 'fg',
            'font-size': self.set_font_size,
            'font-family': self.set_font_family,
            'font-weight': self.set_font_weight,
            'padding': self.set_padding,
            'margin': self.set_padding,
            'width': self.set_width,
            'height': self.set_height,
            'text-align': self.set_text_align,
            'line-height': self.set_line_height,
            'border': self.set_border,
        }

    def parse_file(self, css_filename):
        try:
            with open(css_filename, 'r') as file:
                css_content = file.read()
            self.parse_css(css_content)
            return self.styles
        except Exception as e:
            print(f"Failed to read CSS file: {e}")
            return ""

    def parse_css(self, css_content):
        pattern = r'(?P<selector>\.[\w-]+)\s*\{\s*(?P<properties>[^}]+)\s*\}'
        matches = re.finditer(pattern, css_content)

        for match in matches:
            selector = match.group('selector')
            properties = match.group('properties')
            prop_dict = {}
            for prop in properties.split(';'):
                if ':' in prop:
                    key, value = prop.split(':', 1)
                    prop_dict[key.strip()] = value.strip()
            self.styles[selector] = prop_dict

    def convert_color(self, color):
        if color in self.color_names:
            return self.color_names[color]
        return color

    def apply_style(self, widget, style_name):
        if style_name in self.styles:
            style = self.styles[style_name]
            for prop, value in style.items():
                if prop in self.css_to_tkinter:
                    tk_property = self.css_to_tkinter[prop]
                    if callable(tk_property):
                        tk_property(widget, value)
                    else:
                        widget[tk_property] = self.convert_color(value)

    def set_font_size(self, widget, value):
        widget_font = font.Font(widget, widget['font'])
        widget_font['size'] = int(value.replace('px', ''))
        widget['font'] = widget_font

    def set_font_family(self, widget, value):
        widget_font = font.Font(widget, widget['font'])
        widget_font['family'] = value
        widget['font'] = widget_font

    def set_font_weight(self, widget, value):
        widget_font = font.Font(widget, widget['font'])
        widget_font['weight'] = 'bold' if value == 'bold' else 'normal'
        widget['font'] = widget_font

    def set_padding(self, widget, value):
        padding = tuple(int(x.strip().replace('px', '')) for x in value.split())
        widget['padx'], widget['pady'] = padding

    def set_width(self, widget, value):
        widget['width'] = int(value.replace('px', ''))

    def set_height(self, widget, value):
        widget['height'] = int(value.replace('px', ''))

    def set_text_align(self, widget, value):
        if value == 'center':
            widget['anchor'] = 'center'
        elif value == 'left':
            widget['anchor'] = 'w'
        elif value == 'right':
            widget['anchor'] = 'e'

    def set_line_height(self, widget, value):
        widget_font = font.Font(widget, widget['font'])
        line_height = int(value.replace('px', ''))
        widget_font['linespace'] = line_height
        widget['font'] = widget_font

    def set_border(self, widget, value):
        parts = value.split()
        if len(parts) >= 3:
            thickness = int(parts[0].replace('px', ''))
            widget['highlightthickness'] = thickness
            widget['highlightbackground'] = self.convert_color(parts[2])
