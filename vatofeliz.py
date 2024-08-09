import telebot
from telebot.types import LabeledPrice, ShippingOption

token = '7417229872:AAGsj0UYhZ_Hq1nlS6ed0KXNRF6LQzsBJQw'
provider_token = '350862534:LIVE:YjA0MGY0N2I3YjIx'  # @BotFather -> Bot Settings -> Payments
bot = telebot.TeleBot(token)

# More about Payments: https://core.telegram.org/bots/payments

prices = [LabeledPrice(label='Quiero ser feliz', amount=100), LabeledPrice('Impuesto Feliz', 25)]

shipping_options = [
    ShippingOption(id='instant', title='WorldWide Teleporter').add_price(LabeledPrice('Teleporter', 1000)),
    ShippingOption(id='pickup', title='Local pickup').add_price(LabeledPrice('Pickup', 300))]


@bot.message_handler(commands=['start'])
def command_start(message):
    bot.send_message(message.chat.id,
                     "¡Saludos, amigo! ¿Quiere verse tan feliz como yo? "
                     "Ah, pues tiene el poder dentro de usted ahora mismo, así que úselo."
                     "Envíe un dólar a Vato Feliz usando este bot. No tarde!! La felicidad eterna está a un dólar de distancia. usa el comando /buy para pagar un dolar, /terms para terminos y condiciones")


@bot.message_handler(commands=['terms'])
def command_terms(message):
    bot.send_message(message.chat.id,
                     'Terminos y Condiciones de la Tienda de Felicidad Eterna'
		     'Al hacer una compra aceptas los siguientes terminos y condiciones:'
                     '1. Ofrecemos "Felicidad" a cambio de un dolar. La naturaleza de la felicidad es abstracta y objetiva La felicidad comprada puede o no llegar a su destino.\n'
                     '2. Debido a la naturaleza del producto, no ofrecemos reembolsos, no guardamos ni tenemos acceso a tu informacion personal.'
                     '3. Nos reservamos el derecho de modificar estos terminos en cualquier momento\n'
                     '4. Cualquier duda contacta soporte mediante el canal de el bot en Telegram')


@bot.message_handler(commands=['buy'])
def command_pay(message):
    bot.send_message(message.chat.id,
                     "aceptamos todas las tarjetas y metodos de pago"
                     "\n\nEsta es su factura:", parse_mode='Markdown')
    bot.send_invoice(
                     message.chat.id,  #chat_id
                     'Felicidad Eterna', #title
                     '  No tarde!! La felicidad eterna está a un dólar de distancia.', #description
                     'HAPPY FRIDAYS COUPON', #invoice_payload
                     provider_token, #provider_token
                     'usd', #currency
                     prices, #prices
                     photo_url='https://github.com/christianisais88/Telebot/blob/master/examples/logo1.png?raw=true',
                     photo_height=512,  # !=0/None or picture won't be shown
                     photo_width=512,
                     photo_size=512,
                     is_flexible=False,  # True If you need to set up Shipping Fee
                     start_parameter='time-machine-example')


@bot.shipping_query_handler(func=lambda query: False)
def shipping(shipping_query):
    print(shipping_query)
    bot.answer_shipping_query(shipping_query.id, ok=True, shipping_options=shipping_options,
                              error_message='Oh, seems like our Dog couriers are having a lunch right now. Try again later!')


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message="Aliens tried to steal your card's CVV, but we successfully protected your credentials,"
                                                " try to pay again in a few minutes, we need a small rest.")


@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    bot.send_message(message.chat.id,
                     'Gracias por su donavito amigo! la felicidad esta en camino no desespere '
                     'Si gusta ser doblemente feliz, mande otro dolar, gracias!'.format(
                         message.successful_payment.total_amount / 100, message.successful_payment.currency),
                     parse_mode='Markdown')


bot.infinity_polling(skip_pending = True)
