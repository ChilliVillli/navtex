from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Условия для поиска')
        ]
    ],
    resize_keyboard=True
)


types_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='A (Navigational warnings)'),
            KeyboardButton(text='B (Meteorological warnings)'),
            KeyboardButton(text='C (Ice reports)')
        ],
        [
            KeyboardButton(text='D (SAR)'),
            KeyboardButton(text='E (Meteorological forecasts)'),
            KeyboardButton(text='F (Pilot service messages)')
        ],
        [
            KeyboardButton(text='G (AIS)'),
            KeyboardButton(text='H (LORAN messages)'),
            KeyboardButton(text='L (Navigational warnings)')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
