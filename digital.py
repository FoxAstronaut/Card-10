import leds, utime, display, buttons, color, power

BATTERY_MAX = 4.2
BATTERY_MIN = 3.4
BATTERY_BAR_LEN = 20

def main():
  flash_status = False  
  while True:

    # Check if button is pressed
    button_left = buttons.read(buttons.BOTTOM_LEFT)
    button_right = buttons.read(buttons.BOTTOM_RIGHT)

    # Check what it was
    if button_left and button_right:
      flash_status = not flash_status
      flashlight(flash_status)
      while buttons.read(buttons.BOTTOM_LEFT) and buttons.read(buttons.BOTTOM_RIGHT):
        utime.sleep_ms(1)

    draw_display()

def draw_display():
  '''Draws the clock display'''
  # Start draw functions
  disp = display.open()
  disp.clear()
  display_battery_bars(disp, 0)
  display_time(disp, 18)
  display_date(disp, 50)
  disp.update()
    
def display_time(disp, pos_y):
  '''Draws digital time in hh:mm:ss AM/PM format
  
    Args:
      disp (display): The display to be drawn on
      pos_y (int): The y position to start drawing at
  '''

  time = utime.localtime()
  hours = time[3] if time[3] < 13 else time[3] - 12
  am_pm = 'AM' if time[3] < 13 else 'PM'
  time_string = "{:02d}:{:02d}:{:02d} {}".format(hours, time[4], time[5], am_pm)
  pos_x = 80 - round(len(time_string) / 2 * 14)
  disp = display.open()
  disp.print(time_string, posx=pos_x, posy=pos_y, font=display.FONT20)

def display_date(disp, pos_y):
  '''Draws date in dd/mm/yyyy format
  
    Args:
      disp (display): The display to be drawn on
      pos_y (int): The y position to start drawing at
  '''

  time = utime.localtime()
  date_string = "{:02d}/{:02d}/{:04d}".format(time[2], time[1], time[0])
  pos_x = 80 - round(len(date_string) / 2 * 16)
  disp.print(date_string, posx=pos_x, posy=pos_y, font=display.FONT20)

def display_battery_bars(disp, pos_y):
  '''Draws battery percentage as a bar
  
    Args:
      disp (display): The display to be drawn on
      pos_y (int): The y position to start drawing at
  '''

  no_of_bars = int(map_range(power.read_battery_voltage(), BATTERY_MIN, BATTERY_MAX, 0, BATTERY_BAR_LEN))
  bars = ''
  bars += '=' * no_of_bars
  bars += ' ' * (BATTERY_BAR_LEN - len(bars))
  pos_x = 80 - round(len(bars) / 2 * 8)
  disp.print('|' + bars + '|', posx=pos_x, posy=pos_y, font=display.FONT12)

def flashlight(status=True):
  '''Turns on or off the flashlight, which is all leds at bright white
  
    Args:
      status (boolean): The status of the flashlight, True for on, False for off. Defaults to True
  '''

  if status:
    leds.set_powersave(True)
    leds.set_all([color.WHITE] * 18)
    leds.dim_bottom(8)
    leds.dim_top(8)
  else:
    leds.dim_bottom(0)
    leds.dim_top(0)

  leds.update()

def map_range(old_value, old_min, old_max, new_min, new_max) -> float:
  '''Maps one value within in a range into another range
  
    Args:
      old_value (float): Old value within old range
      old_min (float): Minimum of the old range
      old_max (float): Maximum of the old range
      new_min (float): Minimum of the new range
      new_max (float): Maximum of the new range

    Returns:
      new_value (float): New value in the new range
  '''

  old_range = old_max - old_min
  new_range = new_max - new_min

  return ((old_value - old_min) * new_range / old_range) + new_min

if __name__ == '__main__': 
  main()
