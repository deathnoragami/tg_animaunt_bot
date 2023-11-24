from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
# keyboardbtn with callback "find"

import math


class Title_search_cd(CallbackData, prefix='title_search'):
    title_id: str


class Episode_link(CallbackData, prefix='episode_link'):
    episode_id: str
    title_id: int
    number_episode: int


class PaginationIntitle(CallbackData, prefix='pagination_in_title'):
    title_id: int
    page: int
    action: str
    current_page: int
    
class PaginationInEpisode(CallbackData, prefix='pagination_in_episode'):
    title_id: int
    action: str
    page: int
    current_page: int


main = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Поиск'),
        KeyboardButton(text='Контакты')
    ], 
    [
        KeyboardButton(text='О боте')
    ]
], resize_keyboard=True, one_time_keyboard=True)


def inline_kbb_search(
    text: str | list[str],
    callback_data: str | list[str],
    sizes: int | list[int] = 1,
    **kgargs
) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    
    if isinstance(text, str):
        text = [text]
    if isinstance(callback_data, str):
        callback_data = [callback_data]
    if isinstance(sizes, int):
        sizes = [sizes]
    
    [
        builder.button(text=t, callback_data=Title_search_cd(title_id=c))
        for t, c in zip(text, callback_data)

    ]
    builder.button(text='Отмена', callback_data='cansel')
    builder.adjust(*sizes)
    return builder.as_markup(**kgargs)


def inline_kb_lvl_episode(
    title_id: int,
    page_count: int,
    all_episode_info: list[str],
    current_page: int,
    **kgargs
    ) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    if page_count == 1:
        btn_text = all_episode_info[0]
        btn_episode_id = all_episode_info[1]
    else:
        episode_info = all_episode_info[current_page-1]
        btn_text = episode_info[0]
        btn_episode_id = episode_info[1]
        
    [
        builder.button(text=t, callback_data=Episode_link(episode_id=c, title_id=title_id, number_episode=int(t)))
        for t, c in zip(btn_text, btn_episode_id)
    ]
    
    
    if page_count > 1:
        if current_page == 1:
            builder.button(text='Вперед', callback_data=PaginationIntitle(page=page_count, title_id=title_id, action="next", current_page=current_page))
        elif current_page == page_count:
            builder.button(text='Назад', callback_data=PaginationIntitle(page=page_count, title_id=title_id, action="back", current_page=current_page))
        else:
            builder.button(text='Назад', callback_data=PaginationIntitle(page=page_count, title_id=title_id, action="back", current_page=current_page))
            builder.button(text='Вперед', callback_data=PaginationIntitle(page=page_count, title_id=title_id, action="next", current_page=current_page))
        

    if len(btn_text) > 6:
        builder.adjust(6, len(btn_text)-6, 2)
    else:
        builder.adjust(len(btn_text), 2)




    return builder.as_markup()


def inline_kb_episode(
    page_count: int,
    all_episode_info: list[str],
    title_id: int,
    chose_episode: int = 1,
    from_title: bool = False,
    current_page: int = 1, 
    **kgargs
    ) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    
    
    if from_title:
        current_page = math.floor(chose_episode/24) + 1
        all_episode_info = all_episode_info[current_page-1]
        btn_text = all_episode_info[0]
        btn_episode_id = all_episode_info[1]
    else:
        all_episode_info = all_episode_info[current_page-1]
        btn_text = all_episode_info[0]
        btn_episode_id = all_episode_info[1]
    
    [
        builder.button(text=t, callback_data=Episode_link(episode_id=c, title_id=title_id, number_episode=int(t)))
        for t, c in zip(btn_text, btn_episode_id)
    ]
    
    if page_count > 1:
        if current_page == 1:
            builder.button(text='Вперед', callback_data=PaginationInEpisode(page=page_count, title_id=title_id, action="next", current_page=current_page))
        elif current_page == page_count:
            builder.button(text='Назад', callback_data=PaginationInEpisode(page=page_count, title_id=title_id, action="back", current_page=current_page))
        else:
            builder.button(text='Назад', callback_data=PaginationInEpisode(page=page_count, title_id=title_id, action="back", current_page=current_page))
            builder.button(text='Вперед', callback_data=PaginationInEpisode(page=page_count, title_id=title_id, action="next", current_page=current_page))
      
    if len(btn_text) > 18:
        builder.adjust(6, 6, 6, len(btn_text)-18, 2)
    elif len(btn_text) > 12:
        builder.adjust(6, 6, len(btn_text)-12, 2)
    elif len(btn_text) > 6:
        builder.adjust(6, len(btn_text)-6, 2)
    else:
        builder.adjust(len(btn_text), 2)
        
    return builder.as_markup()