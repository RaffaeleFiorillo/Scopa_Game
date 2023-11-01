CARDS_COO = {"table": [(428, 250), (564, 250), (312, 250), (670, 250), (816, 250), (186, 250), (942, 250)],
             "player": [(x, 430) for x in range(300, 621, 160)]}

CARD_SCALES = {"table": (85, 147), "player": (150, 270), "player-ai": (42, 73)}

warning_yellow = (233, 213, 22)
valid_green = (50, 250, 120)
hover_blue = (0, 255, 255)
error_red = (255, 0, 0)
bg_black = (0, 0, 0)

CARD_COLORS = {None: bg_black,
               "valid": valid_green,
               "incomplete": warning_yellow,
               "invalid": error_red,
               "hover": hover_blue}

CARD_TYPE = "Piacentine"
