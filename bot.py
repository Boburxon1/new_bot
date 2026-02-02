import telebot
from telebot.types import BotCommand
from keyboards import general_classes, inline_hafta_kunlari
from jadval import jadval

TOKEN = "8534971100:AAE-2WMAmChjufLZ_87-QcyfSF-8NI9v8Zc"
bot = telebot.TeleBot(TOKEN)



user_data = {}

print("🤖 Bot ishga tushdi!")

def set_bot_commands():
    commands = [BotCommand("start", "Boshidan boshlash")]
    bot.set_my_commands(commands)

set_bot_commands()

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Salom! Maktab dars jadvali botiga xush kelibsiz! 📚\n\n"
        "📌 Sinfingizni quyidagi tugmalardan tanlang:",
        reply_markup=general_classes()
    )

@bot.message_handler(func=lambda m: m.text and m.text.endswith("-sinf"))
def sinf_tanlandi(message):
    sinf = message.text[:-5]
    
    if sinf not in jadval:
        bot.send_message(message.chat.id, "❌ Kechirasiz, bu sinf uchun jadval mavjud emas.")
        return
    
    user_data[message.chat.id] = sinf
    
    # Hafta kunlari xabari
    bot.send_message(
        message.chat.id,
        f"✅ <b>{sinf}-sinf</b> muvaffaqiyatli tanlandi!\n\n"
        f"📅 Endi hafta kunini tanlang:",
        parse_mode="HTML",
        reply_markup=inline_hafta_kunlari()
    )
    
    # Pastdagi tugmalarni 100% yo‘qotish – bitta nuqta bilan (deyarli ko‘rinmaydi)
    bot.send_message(
        message.chat.id,
        ".",  # Faqat bitta nuqta – chatda deyarli sezilmaydi
        reply_markup=telebot.types.ReplyKeyboardRemove()
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.message.chat.id
    sinf = user_data.get(user_id)
    
    if call.data.startswith("kun_"):
        kun = call.data[4:]
        
        if not sinf:
            bot.answer_callback_query(call.id, "❗ Avval sinf tanlang!", show_alert=True)
            return
        
        darslar = jadval[sinf].get(kun, "❌ Bu kunga dars jadvali mavjud emas.")
        
        # Takroriy bosishni tekshirish
        current_text = (call.message.text or "").strip()
        new_text = (
            f"📚 <b>{sinf}-sinf</b>\n"
            f"📅 <b>{kun}</b>\n\n"
            f"{darslar}\n\n"
            f"🔄 Boshqa kunni tanlashingiz mumkin:"
        ).strip()
        
        if current_text == new_text:
            bot.answer_callback_query(call.id, f"📅 {kun} jadvali allaqachon ko‘rsatilgan ✓", show_alert=True)
            return
        
        try:
            bot.edit_message_text(
                chat_id=user_id,
                message_id=call.message.message_id,
                text=new_text,
                parse_mode="HTML",
                reply_markup=inline_hafta_kunlari()
            )
            bot.answer_callback_query(call.id, f"{kun} jadvali ochildi ✓")
        except telebot.apihelper.ApiTelegramException as e:
            if "message is not modified" in str(e):
                bot.answer_callback_query(call.id, f"📅 {kun} jadvali allaqachon ko‘rsatilgan ✓", show_alert=True)
    
    elif call.data == "back_to_classes":
        if user_id in user_data:
            del user_data[user_id]
        
        try:
            bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
        except:
            pass
        
        bot.send_message(
            chat_id=user_id,
            text="🔙 Sinf tanlash menyusiga qaytdik!\n\n📌 Sinfingizni quyidagi tugmalardan tanlang:",
            reply_markup=general_classes()
        )
        bot.answer_callback_query(call.id, "Sinf tanlashga qaytdik 🔄")

@bot.message_handler(func=lambda m: m.text in ["Dushanba","Seshanba","Chorshanba","Payshanba","Juma","Shanba"])
def eski_kun(message):
    sinf = user_data.get(message.chat.id)
    if not sinf:
        bot.send_message(message.chat.id, "❗ Iltimos, avval sinf tanlang: /start")
        return
    
    kun = message.text
    darslar = jadval[sinf].get(kun, "❌ Bu kunga dars yo‘q.")
    
    bot.send_message(
        message.chat.id,
        f"📚 <b>{sinf}-sinf</b>\n📅 <b>{kun}</b>\n\n{darslar}",
        parse_mode="HTML",
        reply_markup=inline_hafta_kunlari()
    )
 


bot.polling(none_stop=True)