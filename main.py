import telebot
from optimize_function import work_with_file

bot = telebot.TeleBot('6888214147:AAFqdtTiM6hEEdQqISUWkM2UYnXvUSJZAQQ')


@bot.message_handler(content_types=['document'])
def main(message):

    #скачиваем файл
    file_name = message.document.file_name
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)

    work_with_file(file_name)

    bot.send_document(message.chat.id, open(r'updated_data.csv', 'rb'))


bot.polling()
