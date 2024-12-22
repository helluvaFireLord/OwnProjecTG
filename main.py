import telebot
from config import token
from work import get_genres, get_movies_by_genre, get_random_movie

bot = telebot.TeleBot(token)

def split_message(text, max_length=4096):
    parts = []
    while len(text) > max_length:
        split_index = text[:max_length].rfind('\n') 
        if split_index == -1:
            split_index = max_length
        parts.append(text[:split_index])
        text = text[split_index:]
    parts.append(text)
    return parts

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    commands = (
        "Добро пожаловать! Вот список доступных команд:\n"
        "/random_movie - Показать случайный фильм\n"
        "/genres - Выбрать жанр фильма"
    )
    bot.send_message(message.chat.id, commands)

@bot.message_handler(commands=['random_movie'])
def random_movie(message):
    movie = get_random_movie()
    if movie:
        bot.send_message(
            message.chat.id,
            f"Случайный фильм:\n\n"
            f"Название: {movie[1]}\nРейтинг: {movie[2]}\n"
        )
    else:
        bot.send_message(message.chat.id, "Не удалось найти фильмы в базе данных.")

@bot.message_handler(commands=['genres'])
def choose_genre(message):
    genres = get_genres()
    if not genres:
        bot.send_message(message.chat.id, "Жанры отсутствуют в базе данных.")
        return

    text = "\n".join(genres)
    bot.send_message(message.chat.id, "Доступные жанры:\n" + text, reply_markup=gen_inline_markup(genres))

def gen_inline_markup(items):
    markup = telebot.types.InlineKeyboardMarkup()
    for item in items:
        if item.strip(): 
            button = telebot.types.InlineKeyboardButton(text=item, callback_data=item)
            markup.add(button)
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    genre = call.data
    movies = get_movies_by_genre(genre)
    if not movies:
        bot.send_message(call.message.chat.id, f"Фильмы в жанре '{genre}' не найдены.")
        return

    movies = sorted(movies, key=lambda x: x[2], reverse=True)[:100]

    movie_list = "\n".join([f"{movie[1]} (рейтинг: {movie[2]})" for movie in movies])
    full_message = f"Фильмы в жанре '{genre}':\n{movie_list}"

    for part in split_message(full_message):
        bot.send_message(call.message.chat.id, part)

if __name__ == "__main__":
    bot.polling()