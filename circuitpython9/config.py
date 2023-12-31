# configuration for different boards and setups
# 2023/12/31
# output: define LED
# input:  define one/two buttons BUTTON_NEXT, BUTTON_OK and BUTTON_EXIT

import board

pullup = False
has_button_ok = True

if board.board_id == 'lilygo_t_display_rp2040' or board.board_id == 'lilygo_t_picoc3':
    pin_led         = board.LED
    pin_button_next = board.BUTTON_L
    pin_button_ok   = board.BUTTON_R
    pin_button_exit = board.BUTTON_L
    disp            = board.DISPLAY

if board.board_id == 'vcc_gnd_yd_rp2040' or board.board_id == 'raspberry_pi_pico_w':
    pin_led         = board.LED
    pin_button_next = board.GP16
    pin_button_ok   = board.GP3
    pin_button_next = board.GP3
    pullup = True
    import busio, displayio, fourwire
    from adafruit_st7789 import ST7789
    displayio.release_displays()
    spi    = busio.SPI(clock=board.GP10, MOSI=board.GP11)
    tft_cs = board.GP9
    tft_dc = board.GP8
    display_bus = fourwire.FourWire(
        spi, command=tft_dc, chip_select=tft_cs, reset=board.GP12
    )
    disp = ST7789(display_bus, width=240, height=240, rowstart=80)

if board.board_id == 'lilygo_ttgo_tdisplay_esp32_4m':
    pin_led         = board.IO12     # it actually has no LED
    pin_button_next = board.BUTTON0
    pin_button_ok   = board.BUTTON1
    pin_button_exit = board.BUTTON0
    disp            = board.DISPLAY
    pullup = True

if board.board_id == 'lilygo_ttgo_t8_s2_st7789':
    has_button_ok   = False
    pin_led         = board.IO1  # it actually has no LED
    pin_button_next = board.IO0
    pin_button_exit = board.IO0
    disp            = board.DISPLAY
    pullup = True
