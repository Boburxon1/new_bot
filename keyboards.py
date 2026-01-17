from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def general_classes():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    
    sinflar = [
        "5-A", "5-B", "5-D",
        "6-A", "6-B", "6-D", "6-E", "6-F",
        "7-A", "7-D", "7-E",
        "8-A", "8-B", "8-D", "8-E", "8-F",
        "9-A", "9-B", "9-D", "9-E", "9-F",
        "10-A", "10-B", "10-D", "10-G",
        "11-A", "11-D", "11-E"
    ]
    
    for i in range(0, len(sinflar), 3):
        row = sinflar[i:i+3]
        kb.row(*(KeyboardButton(f"{s}-sinf") for s in row))
    
    return kb


def inline_hafta_kunlari():
    kb = InlineKeyboardMarkup()
    
    kb.row(
        InlineKeyboardButton("📅 Dushanba", callback_data="kun_Dushanba"),
        InlineKeyboardButton("📅 Seshanba", callback_data="kun_Seshanba"),
        InlineKeyboardButton("📅 Chorshanba", callback_data="kun_Chorshanba")
    )
    
    kb.row(
        InlineKeyboardButton("📅 Payshanba", callback_data="kun_Payshanba"),
        InlineKeyboardButton("📅 Juma", callback_data="kun_Juma"),
        InlineKeyboardButton("📅 Shanba", callback_data="kun_Shanba")
    )
    
    kb.row(
        InlineKeyboardButton("🔙 Sinf tanlashga qaytish", callback_data="back_to_classes")
    )
    
    return kb