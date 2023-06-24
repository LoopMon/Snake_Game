def drawItem(font, game_menu):
    txt, pos, active = game_menu
    if active:
        font_menu = font.render(f'<< {txt.upper()} >>', True, ('yellow'))
        font_rect = font_menu.get_rect()
        font_rect.center = pos
        return font_menu, font_rect
    else:
        font_menu = font.render(f'{txt.upper()}', True, ('white'))
        font_rect = font_menu.get_rect()
        font_rect.center = pos
        return font_menu, font_rect


def drawText(font, txt, pos, center=False):
    font_txt = font.render(txt, True, ('white'))
    if center:
        font_rect = font_txt.get_rect()
        font_rect.center = pos

        return font_txt, font_rect
        
    return font_txt, pos