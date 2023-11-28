from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import Bot

import app.keyboard as kb
import database.request as req
from app.keyboard import Title_search_cd, Episode_link, PaginationIntitle, PaginationInEpisode
from config import VIDEO_CHAT_ID
from .keyboard import inline_kbb_search, inline_kb_lvl_episode, inline_kb_episode

router = Router()

class SearchState(StatesGroup):
    WaitingForInput = State()


@router.message(CommandStart())
async def cmd_start(message: Message, bot: Bot):
    await message.answer(text='Привет.', reply_markup=kb.main)  # TODO: стартовое сообщение


@router.message(F.text == "Контакты")
async def cmd_contacts(message: Message):
    await message.answer('Бот был создан Долбаебами.')

@router.message(F.text.lower() == "поиск")
async def search_btn(message: Message, state=FSMContext):
    await message.answer('Введите запрос')
    await state.set_state(SearchState.WaitingForInput)


@router.message(SearchState.WaitingForInput)
async def search_input(message: Message, state=FSMContext):
    await state.update_data(WaitingForInput=message.text)
    msg = await state.get_data()
    title = await req.AnimeDB.search_title(msg['WaitingForInput'])
    await message.answer("Результат:",
                         reply_markup=inline_kbb_search(
                             text=title[0],
                             callback_data=title[1]
                             )
                         )  # TODO reply_markup Переделать на то что было найдено
    await state.clear()


@router.callback_query(Title_search_cd.filter())
async def callback_title(call: CallbackQuery, bot: Bot):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    #TODO: call.data.split(':', 1)[1] это айди тайтла, по нему искать фулл инфу о тайтле
    title = await req.AnimeDB.get_title(int(call.data.split(':', 1)[1]))
    episode_list = await req.AnimeDB.get_episode_all(title.id)
    page_count = (len(episode_list[0]) - 1) // 12 + 1 
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
    caption = f"<b>Название:</b> {title.name}\n\nВсего серий: <b>{title.match_episode}</b>\n\n<b>Описание:</b> {title.description}\n\nСмотреть на сайте {title.url}"
    await call.message.answer_photo(photo=title.image_url,
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
    caption = f"Ты смотришь {title.name} - {episode.number} серию!\n\n"
    # await bot.copy_message(chat_id=message.chat.id, from_chat_id=VIDEO_CHAT_ID, message_id=49, caption="Серия такая, и то такое вот")
    # image = URLInputFile("https://fon.litrelax.ru/uploads/posts/2023-01/1673218763_foni-club-p-oboi-anime-dozhd-4k-1.jpg", filename="prev.jpg")
    
    await bot.copy_message(chat_id=call.message.chat.id, 
                           from_chat_id=VIDEO_CHAT_ID, 
                           caption=caption,
                           message_id=episode.video_msg_id, 
                           reply_markup=inline_kb_episode(page_count=page_count,
                                                            chose_episode=int(data[3]),
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
    