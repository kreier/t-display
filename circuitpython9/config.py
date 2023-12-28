# configuration for different boards and setups
# 2023/12/28
# output: define LED
# input:  define two buttons BUTTON_NEXT and BUTTON_OK

import digitalio, board

pin_led = board.LED

if board.board_id == 'lilygo_t_display_rp2040':
    pin_button_next = board.BUTTON_L
    pin_button_ok   = board.BUTTON_R
