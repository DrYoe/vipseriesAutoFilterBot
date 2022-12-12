#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @trojanzhex

from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

import re
import pyrogram

from pyrogram import (
    filters,
    Client
)

from pyrogram.types import (
    InlineKeyboardButton, 
    InlineKeyboardMarkup, 
    Message,
    CallbackQuery,
)

from bot import Bot
from script import script
from database.mdb import searchquery
from plugins.channel import deleteallfilters
from config import AUTH_USERS, IMDB_TEXT
from Omdb import get_posters

BUTTONS = {}

@Client.on_message(filters.group & filters.text)
async def filter(client: Bot, message: Message):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return

    if 2 < len(message.text) < 50:    
        btn = []

        group_id = message.chat.id
        name = message.text

        filenames, links = await searchquery(group_id, name)
        if filenames and links:
            for filename, link in zip(filenames, links):
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}",url=f"{link}")]
                )
        else:
            return

        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="🔰 Pages 1/1 🔰",callback_data="pages")]
            )
            buttons.append(
                [InlineKeyboardButton("⭐️ မန်ဘာဝင်လိုလျှင် ဒီမှာကြည့်ပါ ⭐️", url="https://t.me/YNVIPMEMBERBOT")]
            )
            buttons.append(
                [InlineKeyboardButton("💖 VIP Series List & Poster 💖", url="https://t.me/YN_VIP_Series_ListAndPoster")]
            )


            imdb=await get_posters(name)
            if imdb:
                cap = IMDB_TEXT.format(un=message.from_user.username, user=message.from_user.first_name, query=name, title=imdb['title'], trailer=imdb["trailer"], runtime=imdb["runtime"], languages=imdb["languages"], genres=imdb['genres'], year=imdb['year'], rating=imdb['rating'], url=imdb['url'])                                                  
            else:
            
                cap = f"<b> Hello [{message.from_user.first_name}]({message.from_user.username})</b>\n\n<b>သင်ရှာတဲ့ 👉🏻 {message.text} 👈🏻  ကို မင်မင်ရှာတွေ့တာလေးပြပေးထားပါတယ်နော် ☺️ ......</b>\n\n<b>ဇာတ်ကားရှာသူ : [{message.from_user.first_name}]({message.from_user.username})</b>\n\n<b>Join Main Channel \nMovie 👉🏻 @YNmovieone \nSeries👉🏻 @YoeNaungKSeriesChannel</b>",
                
            if imdb and imdb.get('poster'):
               try:                   
                   await message.reply_photo(photo=imdb.get('poster'), caption=cap, reply_markup=InlineKeyboardMarkup(buttons), parse_mode="md")                               
               except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
                   pic = imdb.get('poster')
                   poster = pic.replace('.jpg', "._V1_UX360.jpg")
                   await message.reply_photo(photo=poster, caption=cap[:1024], reply_markup=InlineKeyboardMarkup(buttons), parse_mode="md")
               except Exception as e:
                   logger.exception(e)
                   await message.reply_text(text=cap, reply_markup=InlineKeyboardMarkup(buttons), parse_mode="md") 
            else: 
               await message.reply_text(
                   text=f"Hello [{message.from_user.first_name}]({message.from_user.username}) </b>\n\n<b>သင်ရှာတဲ့ 👉🏻 {message.text} 👈🏻  ကို မင်မင်ရှာတွေ့တာလေးပြပေးထားပါတယ်နော် ☺️ ......\n\nဇာတ်ကားရှာသူ :[{message.from_user.first_name}]({message.from_user.username}) \n\nJoin Main Channel \nMovie 👉🏻 @YNmovieone \nSeries👉🏻 @YoeNaungKSeriesChannel",         
                   reply_markup=InlineKeyboardMarkup(buttons),
                   parse_mode="md"
                )
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="NEXT ⏩",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"🔰 Pages 1/{data['total']} 🔰",callback_data="pages")]
        )
        buttons.append(
            [InlineKeyboardButton("⭐️ မန်ဘာဝင်လိုလျှင် ဒီမှာကြည့်ပါ ⭐️", url="https://t.me/YNVIPMEMBERBOT")]
        )
        buttons.append(
            [InlineKeyboardButton("💖 VIP Series List & Poster 💖", url="https://t.me/YN_VIP_Series_ListAndPoster")]
        )
        
        imdb=await get_posters(name)
        if imdb:
            cap = IMDB_TEXT.format(un=message.from_user.username, user=message.from_user.first_name, query=name, title=imdb['title'], trailer=imdb["trailer"], runtime=imdb["runtime"], languages=imdb["languages"], genres=imdb['genres'], year=imdb['year'], rating=imdb['rating'], url=imdb['url'])                                                  
        else:

            cap = f"<b>Hello [{message.from_user.first_name}]({message.from_user.username}) </b>\n\n<b>သင်ရှာတဲ့ 👉🏻 {message.text} 👈🏻  ကို မင်မင်ရှာတွေ့တာလေးပြပေးထားပါတယ်နော် ☺️ ......</b>\n\n<b>ဇာတ်ကားရှာသူ :[{message.from_user.first_name}]({message.from_user.username}) </b>\n\n<b>Join Main Channel \nMovie 👉🏻 @YNmovieone \nSeries👉🏻 @YoeNaungKSeriesChannel</b>",
           
        if imdb and imdb.get('poster'):
            try:                   
                await message.reply_photo(photo=imdb.get('poster'), caption=cap, reply_markup=InlineKeyboardMarkup(buttons), parse_mode="md")                               
            except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
                pic = imdb.get('poster')
                poster = pic.replace('.jpg', "._V1_UX360.jpg")
                await message.reply_photo(photo=poster, caption=cap[:1024], reply_markup=InlineKeyboardMarkup(buttons), parse_mode="md")
            except Exception as e:
                logger.exception(e)
                await message.reply_text(text=cap, reply_markup=InlineKeyboardMarkup(buttons), parse_mode="md") 
        else: 
            await message.reply_text(
                text=f"Hello [{message.from_user.first_name}]({message.from_user.username}) \n\nသင်ရှာတဲ့ 👉🏻 {message.text} 👈🏻  ကို မင်မင်ရှာတွေ့တာလေးပြပေးထားပါတယ်နော် ☺️ ......\n\nဇာတ်ကားရှာသူ :[{message.from_user.first_name}]({message.from_user.username}) </b>\n\n<b>Join Main Channel \nMovie 👉🏻 @YNmovieone \nSeries👉🏻 @YoeNaungKSeriesChannel<",         
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode="md"
            ) 

@Client.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    clicked = query.from_user.id
    typed = query.message.reply_to_message.from_user.id

    if (clicked == typed) or (clicked in AUTH_USERS):

        if query.data.startswith("next"):
            await query.answer()
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("သင်သည် ကျွန်ုပ်၏ မက်ဆေ့ဂျ်ဟောင်းများထဲမှ တစ်ခုအတွက် ၎င်းကို အသုံးပြုနေသည်၊ ကျေးဇူးပြု၍ တောင်းဆိုချက်ကို ထပ်မံပေးပို့ပါ။",show_alert=True)
                return

            if int(index) == int(data["total"]) - 2:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("⏪ BACK", callback_data=f"back_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"🔰 Pages {int(index)+2}/{data['total']} 🔰", callback_data="pages")]
                )
                buttons.append(
                    [InlineKeyboardButton("⭐️ မန်ဘာဝင်လိုလျှင် ဒီမှာကြည့်ပါ ⭐️", url="https://t.me/YNVIPMEMBERBOT")]
                )
                buttons.append(
                    [InlineKeyboardButton("💖 VIP Series List & Poster 💖", url="https://t.me/YN_VIP_Series_ListAndPoster")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
            else:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("⏪ BACK", callback_data=f"back_{int(index)+1}_{keyword}"),InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"🔰 Pages {int(index)+2}/{data['total']} 🔰", callback_data="pages")]
                )
                buttons.append(
                    [InlineKeyboardButton("⭐️ မန်ဘာဝင်လိုလျှင် ဒီမှာကြည့်ပါ ⭐️", url="https://t.me/YNVIPMEMBERBOT")]
                )
                buttons.append(
                    [InlineKeyboardButton("💖 VIP Series List & Poster 💖", url="https://t.me/YN_VIP_Series_ListAndPoster")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return


        elif query.data.startswith("back"):
            await query.answer()
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("သင်သည် ကျွန်ုပ်၏ မက်ဆေ့ဂျ်ဟောင်းများထဲမှ တစ်ခုအတွက် ၎င်းကို အသုံးပြုနေသည်၊ ကျေးဇူးပြု၍ တောင်းဆိုချက်ကို ထပ်မံပေးပို့ပါ။.",show_alert=True)
                return

            if int(index) == 1:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"🔰 Pages {int(index)}/{data['total']} 🔰", callback_data="pages")]
                )
                buttons.append(
                    [InlineKeyboardButton("⭐️ မန်ဘာဝင်လိုလျှင် ဒီမှာကြည့်ပါ ⭐️", url="https://t.me/YNVIPMEMBERBOT")]
                )
                buttons.append(
                    [InlineKeyboardButton("💖 VIP Series List & Poster 💖", url="https://t.me/YN_VIP_Series_ListAndPoster")]
                )
  
                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return   
            else:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("⏪ BACK", callback_data=f"back_{int(index)-1}_{keyword}"),InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"🔰 Pages {int(index)}/{data['total']} 🔰", callback_data="pages")]
                )
                buttons.append(
                    [InlineKeyboardButton("⭐️ မန်ဘာဝင်လိုလျှင် ဒီမှာကြည့်ပါ ⭐️", url="https://t.me/YNVIPMEMBERBOT")]
                )
                buttons.append(
                    [InlineKeyboardButton("💖 VIP Series List & Poster 💖", url="https://t.me/YN_VIP_Series_ListAndPoster")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return


        elif query.data == "pages":
            await query.answer()


        elif query.data == "start_data":
            await query.answer()
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("HELP", callback_data="help_data"),
                    InlineKeyboardButton("ABOUT", callback_data="about_data")],
                [InlineKeyboardButton("❣️ JOIN MAIN CHANNEL ❣️ ", url="https://t.me/YNmovieone")]
            ])

            await query.message.edit_text(
                script.START_MSG.format(query.from_user.mention),
                reply_markup=keyboard,
                disable_web_page_preview=True
            )


        elif query.data == "help_data":
            await query.answer()
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("BACK", callback_data="start_data"),
                    InlineKeyboardButton("ABOUT ", callback_data="about_data")],
                [InlineKeyboardButton("❣️ SUPPORT ❣️", url="https://t.me/+XTScHquCH0A0ZTQ1")]
            ])

            await query.message.edit_text(
                script.HELP_MSG,
                reply_markup=keyboard,
                disable_web_page_preview=True
            )


        elif query.data == "about_data":
            await query.answer()
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("BACK", callback_data="help_data"),
                    InlineKeyboardButton("START", callback_data="start_data")],
                [InlineKeyboardButton(" ❣️ SOURCE CODE ❣️", url="https://t.me/YoeNaung")]
            ])

            await query.message.edit_text(
                script.ABOUT_MSG,
                reply_markup=keyboard,
                disable_web_page_preview=True
            )


        elif query.data == "delallconfirm":
            await query.message.delete()
            await deleteallfilters(client, query.message)
        
        elif query.data == "delallcancel":
            await query.message.reply_to_message.delete()
            await query.message.delete()

    else:
        await query.answer("အဲဒါ မင်းအတွက်မဟုတ်ဘူး။!!",show_alert=True)


def split_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]  
