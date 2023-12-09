from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, InputFile, BufferedInputFile
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
<<<<<<< HEAD
from aiogram import Bot, types
from PIL import Image
=======
from aiogram import Bot

from PIL import Image
from io import BytesIO

>>>>>>> 091577e08cb395d7c5ae2d89dd0162595912fb11
import app.keyboard as kb
import database.request as req
from app.keyboard import Title_search_cd, Episode_link, PaginationIntitle, PaginationInEpisode
from config import VIDEO_CHAT_ID
from .keyboard import inline_kbb_search, inline_kb_lvl_episode, inline_kb_episode
import base64

router = Router()

class SearchState(StatesGroup):
    WaitingForInput = State()


@router.message(CommandStart())
async def cmd_start(message: Message, bot: Bot):
    text = f'Тут нужно ввести приветственный текст'
    await message.answer(text='Привет.', reply_markup=kb.main)  # TODO: стартовое сообщение


@router.message(F.text == "Контакты")
async def cmd_contacts(message: Message):
    await message.answer('Бот был создан Долбаебами.')


@router.message(Command("find"))
@router.message(F.text.lower() == "🔍️поиск")
async def search_btn(message: Message, state=FSMContext):
    await message.answer(f"🔍️Введите запрос\n\n" \
                        f"Пример:\n<code>стоун</code>\n<code>Магическая 2</code>")
    await state.set_state(SearchState.WaitingForInput)



@router.message(SearchState.WaitingForInput)
async def search_input(message: Message, bot: Bot, state=FSMContext, ):
    await state.update_data(WaitingForInput=message.text)
    msg = await state.get_data()
    await bot.delete_message(chat_id=message.chat.id, message_id=int(message.message_id)-1)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    title = await req.AnimeDB.search_title(msg['WaitingForInput'])
    if len(title[0]) == 0:
        await message.answer(text=f'По вашему запросу <b>"{message.text}"</b> ничего не найдено'\
                                  f'\nПоиск заново /find')
        await state.clear()
    else:
        await message.answer(f"🤔Вот что я нашел по твоему запросу:"\
                             f"\n<b>Отменить выбор</b> /start, <b>поиск заново</b> /find",
                            reply_markup=inline_kbb_search(
                                text=title[0],
                                callback_data=title[1]
                                )
                            )
        await state.clear()


@router.callback_query(Title_search_cd.filter())
async def callback_title(call: CallbackQuery, bot: Bot):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    #TODO: call.data.split(':', 1)[1] это айди тайтла, по нему искать фулл инфу о тайтле
    title = await req.AnimeDB.get_title(int(call.data.split(':', 1)[1]))
    episode_list = await req.AnimeDB.get_episode_all(title.id)
    page_count = (len(episode_list[0]) - 1) // 12 + 1 

    # decode image
    decoded_image = base64.b64decode(title.image_url)
    image = BytesIO(decoded_image)
    image = Image.open(image, 'r')
    buf = BytesIO()
    image.save(buf, 'jpeg')
    buf.seek(0)
    # decode image

    if page_count > 1:
        episode_divided = []
        for page in range(page_count):
            start_index =  page * 12 
            end_index = (page+1) * 12
            current_page_episodes = episode_list[0][start_index:end_index]
            current_page_episodes_id = episode_list[1][start_index:end_index]
            episode_divided.append([current_page_episodes,current_page_episodes_id]) # 
    else:
        episode_divided = episode_list
    caption = f"<b>Название:</b> {title.name}\n\nВсего серий: <b>{title.match_episode}</b>\n\n<b>Описание:</b>{title.description}\n\nСмотреть на сайте {title.url}"
<<<<<<< HEAD
    await call.message.answer_photo(photo=types.FSInputFile(title.image_url),
=======
    await call.message.answer_photo(photo=BufferedInputFile(buf.getvalue(), 'poster.jpeg'),
>>>>>>> 091577e08cb395d7c5ae2d89dd0162595912fb11
                                    caption=caption,
                                    reply_markup=inline_kb_lvl_episode(title_id=int(title.id), 
                                                                    page_count=page_count,
                                                                    all_episode_info=episode_divided,
                                                                    current_page=page_count                                                              
                                                                    ))

@router.callback_query(PaginationIntitle.filter())
async def change_episode_title(call: CallbackQuery):
    id_msg = call.message.message_id
    data = call.data.split(':')
    if data[3] == 'next':
        current_page = int(data[4]) + 1
    if data[3] == 'back':
        current_page = int(data[4]) - 1
    episode_list = await req.AnimeDB.get_episode_all(int(data[1]))

    episode_divided = []
    page_count = int(data[2])
    for page in range(page_count):
        start_index =  page * 12 
        end_index = (page+1) * 12
        current_page_episodes = episode_list[0][start_index:end_index]
        current_page_episodes_id = episode_list[1][start_index:end_index]
        episode_divided.append([current_page_episodes,current_page_episodes_id]) # 
    print(current_page)
    await call.message.edit_reply_markup(inline_message_id=str(id_msg), 
                                         reply_markup=inline_kb_lvl_episode(title_id=int(data[1]), 
                                                                            page_count=page_count, 
                                                                            current_page=current_page,
                                                                            all_episode_info=episode_divided
                                                                            ))


@router.callback_query(Episode_link.filter())
async def callback_episode(call: CallbackQuery, bot: Bot):
    data = call.data.split(":")
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    episode = await req.AnimeDB.get_episode(int(data[1]))
    episode_list = await req.AnimeDB.get_episode_all(int(data[2]))
    title = await req.AnimeDB.get_title(int(data[2])) # TODO: Передать название тайтла в калбеках
    page_count = (len(episode_list[0]) - 1) // 24 + 1 # до 24 серий.
    if page_count > 1:
        episode_divided =[]
        for page in range(page_count):
            start_index =  page * 24 
            end_index = (page+1) * 24
            current_page_episodes = episode_list[0][start_index:end_index]
            current_page_episodes_id = episode_list[1][start_index:end_index]
            episode_divided.append([current_page_episodes,current_page_episodes_id])
    else:
        episode_divided = episode_list
    caption = f"{title.name} - {episode.caption}.\n\n"
    # await bot.copy_message(chat_id=message.chat.id, from_chat_id=VIDEO_CHAT_ID, message_id=49, caption="Серия такая, и то такое вот")
    # image = URLInputFile("https://fon.litrelax.ru/uploads/posts/2023-01/1673218763_foni-club-p-oboi-anime-dozhd-4k-1.jpg", filename="prev.jpg")
    
    await bot.copy_message(chat_id=call.message.chat.id, 
                           from_chat_id=VIDEO_CHAT_ID, 
                           caption=caption,
                           message_id=episode.video_msg_id, 
                           reply_markup=inline_kb_episode(page_count=page_count,
                                                            chose_episode=data[3],
                                                            all_episode_info=episode_divided,
                                                            from_title=True, 
                                                            title_id=int(data[2])))                                                                                  
    
@router.callback_query(PaginationInEpisode.filter())
async def change_episode_episode(call: CallbackQuery, bot: Bot):
    data = call.data.split(":")
    if data[2] == 'next':
        current_page = int(data[4]) + 1
    if data[2] == 'back':
        current_page = int(data[4]) - 1
    episode_list = await req.AnimeDB.get_episode_all(int(data[1]))
    episode_divided =[]
    for page in range(int(data[3])):
        start_index =  page * 24 
        end_index = (page+1) * 24
        current_page_episodes = episode_list[0][start_index:end_index]
        current_page_episodes_id = episode_list[1][start_index:end_index]
        episode_divided.append([current_page_episodes,current_page_episodes_id])
    await call.message.edit_reply_markup(inline_message_id=str(call.message.message_id),
                                         reply_markup=inline_kb_episode(page_count=int(data[3]),
                                                                        all_episode_info=episode_divided,
                                                                        title_id=int(data[1]),
                                                                        current_page=current_page))
    
