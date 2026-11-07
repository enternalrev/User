import asyncio
import random
import json
import os
import re
from pyrogram import Client, filters, idle, enums
from pyrogram.types import (
    Message, 
    CallbackQuery, 
    InlineKeyboardMarkup, 
    InlineKeyboardButton,
    ChatPermissions
)
from pyrogram.handlers import MessageHandler
from pyrogram.raw.functions.channels import EditTitle
from pyrogram.raw.functions.channels import InviteToChannel
from pyrogram.errors import FloodWait, PeerFlood

try:
    from pytgcalls import PyTgCalls
    from pytgcalls.types import MediaStream
    TGCALLS = True
except ImportError:
    TGCALLS = False

# ==========================================
# ⚙️ CONFIGURATION
# ==========================================
API_ID = 39958068                     # REPLACE WITH YOUR API ID
API_HASH = "b0eb07651d0870691d7b3dd44f550353"          # REPLACE WITH YOUR API HASH
BOT_TOKEN = "8259729023:AAHqZEuFGJ9kqewQS1eU5U-0iprNqq_dKxQ"        # REPLACE WITH YOUR BOT TOKEN

# ==========================================
# 💥 CUSTOM RAID TEXTS
# ==========================================
RAID_TEMPLATES = [
"{name} Are sun tu teri behen ke upar 150 kaale logo ka white 🤍 sperm gira duga human breeding kregi tri behen☺️",
"{name} AGAR ME APKI माँ KO NAMAZ PADHTE WAQT CHODUN TO CYA VO SUNNAT HOGA?🤪",
"{name} Teri mummy ko subah 5 baje uthake morning walk pe lejake break fast karake nahLake dholake lunch karake din me sulake raat me utha ke candle light date dinner krke phir Ghar pe lake dheere dheere pom pom krte krte chodunga 🤪🤏🏿 entry 🥵🥵🥵",
"{name} 𝙏𝙚𝙧𝙞 𝙢𝙖 𝙠𝙞 𝙘𝙝𝙪𝙩 𝙆𝙖 𝙗𝙞𝙧𝙮𝙖𝙣𝙞 𝙥𝙠𝙖 𝙠𝙚 𝙠𝙝𝙖 𝙟𝙖𝙪𝙣𝙜𝙖😁",
"{name} 𝙏𝙐 𝙏𝙊𝙃 𝙈𝙀𝙍𝘼 𝙒𝙊𝙃𝙄 𝙏𝘼𝙏𝙏𝘼 𝙃𝘼𝙄 𝙉𝘼 ? 𝙅𝙄𝙎𝙈𝙀 𝙍𝙊𝙕 𝙆𝙃𝙐𝙅𝙇𝙄 𝙃𝙊𝙏𝙄🤣",
"{name} 𝙆𝙞𝙩𝙣𝙖 𝙘𝙝𝙪𝙙𝙚𝙜𝙖 𝘼𝙗 𝙩𝙚𝙧𝙞 𝙢𝙖 𝙠𝙤 𝙗𝙝𝙞 𝙢𝙤𝙠𝙖 𝙙𝙚 𝙘𝙝𝙪𝙙𝙣𝙚 𝙠𝙖🤗",
"{name} Oye dost Teri randi maa ka 👙 aur 300 rupey reh gaye ake le ja Aur teri randi maa v yahi he Konsi maa Dharti maa Fatima Teri Ghar wali maa Ya teri dadi ki maa?",
"{name} Ye dekh Tmkc me camel 🐪 ",
"{name} Oho funny 🤣😂🤣😂🤣😂🤣😂🤣😂🤣😂🤣🤣😂🤣😂🤣😂🤣😂🤣😂🤣😂🤣😂🤣😂🤣😂🤣😂🤣😂🤣😂🤣 Ab trima chudegi😱",
"{name} Baune trima cute RND he tri behen ko to slave banake rkha he mene itna attitude kese aara tujhme😂😂😂😂😂💔😂😂💔😂💔😂💔😂💔😂💔💔😂🥀🥀🥀",
"{name} Apki mom itni RND kese he bina pese lie chud jaati😏🥀💔",
"{name} Trima pe atomic bomb gir jae jo tre sarr pe pankha he na vo tut ke tre goto pe gire jo tre ghar pe cylinder he na tre ma jab uspe khana banari ho tb vi fatt jae jo tra nall he na vo leak hojae or tra ghar bhass jae mc",
"{name} ＴＲＩＭＡ　ＣＨＵＤＧＹＩ　ＲＥ😜💜　        ほソがん       ˖ ᡣ𐭩 ⊹ ࣪  ౨ৎ˚₊",
"{name} Beta lund chus bada ho pese duga 😏🥀",
"{name} sun aukat anusar chud tu",
"{name} chl mc apni mom ki kali chut ki mms send kr"
]

# ==========================================
# 🩷🤍🩵 RS TEMPLATES
# ==========================================
RS_TEMPLATES = [
"{name} TERY MA CHUDGYI RE 💪🏿😎🩵🤍🩷\n彡彡彡彡彡彡彡彡彡彡彡彡♡♡♡♡♡♡♡♡♡♡♡♡♡\n\n\n{name} TERY MA CHUDGYI RE 💪🏿😎🩵🤍🩷\n彡彡彡彡彡彡彡彡彡彡彡彡♡♡♡♡♡♡♡♡♡♡♡♡♡\n\n\n{name} TERY MA CHUDGYI RE 💪🏿😎🩵🤍🩷\n彡彡彡彡彡彡彡彡彡彡彡彡♡♡♡♡♡♡♡♡♡♡♡♡♡\n\n\n{name} TERY MA CHUDGYI RE 💪🏿😎🩵🤍🩷\n彡彡彡彡彡彡彡彡彡彡彡彡♡♡♡♡♡♡♡♡♡♡♡♡♡\n\n\n{name} TERY MA CHUDGYI RE 💪🏿😎🩵🤍🩷\n彡彡彡彡彡彡彡彡彡彡彡彡♡♡♡♡♡♡♡♡♡♡♡♡♡\n\n\n{name} TERY MA CHUDGYI RE 💪🏿😎🩵🤍🩷\n彡彡彡彡彡彡彡彡彡彡彡彡♡♡♡♡♡♡♡♡♡♡♡♡♡\n\n\n{name} TERY MA CHUDGYI RE 💪🏿😎🩵🤍🩷\n彡彡彡彡彡彡彡彡彡彡彡彡♡♡♡♡♡♡♡♡♡♡♡♡♡\n\n\n{name} TERY MA CHUDGYI RE 💪🏿😎🩵🤍🩷\n彡彡彡彡彡彡彡彡彡彡彡彡♡♡♡♡♡♡♡♡♡♡♡♡♡"
]

# ==========================================
# 🗄️ LOCAL JSON DATABASE SETUP
# ==========================================
DB_FILE = "s1n_sessions.json"

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

db_data = load_db()

# ==========================================
# 🎨 STYLISH TEXT & EMOJIS
# ==========================================
def fancy(text):
    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    script = "ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ0123456789"
    trans = str.maketrans(normal, script)
    return text.translate(trans)

E1 = "🩵" # Success
E2 = "🤍" # Info
E3 = "🩷" # Error

# ==========================================
# 🏗️ BOT CLIENT & GLOBALS
# ==========================================
app = Client(
    "s1n_hoster_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

active_clients = {}  
user_login_data = {} 
worker_owners = {}   
spam_tasks = {}      
global_delays = {}   
raid_messages = {}   
rsall_tasks = {}     
user_calls = {}      

# Bot Globals
active_bots = {}     
bot_delays = {}      
bot_nc_tasks = {}    
bot_spam_tasks = {}  

# ==========================================
# 🛠️ HELPERS & ANIMATIONS
# ==========================================
async def spin(message, text):
    frames = ["◐", "◓", "◑", "◒"]
    for f in frames:
        try: await message.edit_text(f"{E2} **{fancy(text)}** {f}")
        except: pass
        await asyncio.sleep(0.1)
    try: await message.edit_text(f"{E1} **{fancy(text)}** ✅")
    except: pass
    await asyncio.sleep(1.5)
    try: await message.delete()
    except: pass

async def message_watcher(client: Client, message: Message):
    if not message.chat or message.chat.type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return
    
    # Ignore messages sent by the userbot itself
    if message.outgoing: return
    
    # Ignore messages from other bots to prevent infinite loops
    if message.from_user and message.from_user.is_bot: return
    
    if not message.text: return
    
    chat_id = message.chat.id
    
    # RSALL Feature
    if chat_id in rsall_tasks:
        try:
            await asyncio.wait_for(message.reply_text(rsall_tasks[chat_id]), timeout=10)
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except Exception as e:
            print(f"[RSALL ERROR] {e}")

# ==========================================
# 🚀 START HANDLER & MAIN MENU
# ==========================================
@app.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    caption = (
        f"**{fancy('S1N HOSTER')}**\n\n"
        f"{E2} **{fancy('PREMIUM USERBOT HOSTER')}**\n\n"
        f"{E1} {fancy('Deploy userbots with zero prefix.')}\n"
        f"{E3} {fancy('Manage workers & bots effortlessly.')}\n"
        f"{E2} {fancy('Fast. Stylish. Unstoppable.')}"
    )
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("𝑂𝑊𝑁𝐸𝑅♡", callback_data="owner_info")],
        [InlineKeyboardButton("𝐻𝑂𝑆𝑇 𝑈𝑆𝐸𝑅𝐵𝑂𝑇彡", callback_data="host_userbot")],
        [InlineKeyboardButton("𝐺𝑈𝐼𝐷𝐸", callback_data="guide_info")]
    ])
    try:
        await message.reply_photo(photo="https://i.ibb.co/3sXqXqX/s1n-hoster.jpg", caption=caption, reply_markup=buttons)
    except Exception:
        await message.reply_text(text=caption, reply_markup=buttons)

@app.on_callback_query()
async def callback_handler(client: Client, query: CallbackQuery):
    data = query.data
    if data == "owner_info":
        await query.message.edit_text(
            f"{E2} **{fancy('OWNER')}**\n\n"
            f"**{fancy('Name:')}** {fancy('S1N')}\n"
            f"**{fancy('Role:')}** {fancy('Lead Developer')}\n"
            f"**{fancy('Status:')}** {E1} {fancy('Online')}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("𝐵𝐴𝐶𝐾", callback_data="back_to_start")]])
        )
    elif data == "guide_info":
        guide_text = (
            f"{E2} **{fancy('GUIDE')}**\n\n"
            f"{E1} **{fancy('1. API Setup:')}**\n"
            f"{fancy('Get API_ID & API_HASH from my.telegram.org.')}\n\n"
            f"{E1} **{fancy('2. Host Userbot:')}**\n"
            f"{fancy('Click Host and follow the prompts.')}\n\n"
            f"{E1} **{fancy('3. Userbot Commands:')}**\n"
            f"{fancy('rreply, rs, rsall, rstop, rdelays, adduser, vjoin, vleave, group cmds, help')}\n\n"
            f"{E1} **{fancy('4. Bot Commands (.)')}**\n"
            f"{fancy('.sbots, .addbots, .nc, .delay, .rreply, .rsall, .stop')}"
        )
        await query.message.edit_text(guide_text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("𝐵𝐴𝐶𝐾", callback_data="back_to_start")]]))
    elif data == "host_userbot":
        await query.message.edit_text(f"{E2} **{fancy('CONNECTING')}** ◐")
        await asyncio.sleep(0.1)
        await query.message.edit_text(f"{E2} **{fancy('CONNECTING')}** ◓")
        await asyncio.sleep(0.1)
        await query.message.edit_text(
            f"{E3} **{fancy('HOSTING SETUP')}**\n\n"
            f"{E1} {fancy('Send your API ID (or type cancel):')}\n\n"
            f"{E2} {fancy('(Get it from my.telegram.org)')}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("𝐶𝐴𝑁𝐶𝐸𝐿", callback_data="back_to_start")]])
        )
        user_login_data[query.from_user.id] = {"step": "api_id", "is_worker": False}
    elif data == "back_to_start":
        caption = (
            f"**{fancy('S1N HOSTER')}**\n\n"
            f"{E2} **{fancy('PREMIUM USERBOT HOSTER')}**\n\n"
            f"{E1} {fancy('Deploy userbots with zero prefix.')}\n"
            f"{E3} {fancy('Manage workers & bots effortlessly.')}\n"
            f"{E2} {fancy('Fast. Stylish. Unstoppable.')}"
        )
        await query.message.edit_text(caption, reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("𝑂𝑊𝑁𝐸𝑅♡", callback_data="owner_info")],
            [InlineKeyboardButton("𝐻𝑂𝑆𝑇 𝑈𝑆𝐸𝑅𝐵𝑂𝑇彡", callback_data="host_userbot")],
            [InlineKeyboardButton("𝐺𝑈𝐼𝐷𝐸", callback_data="guide_info")]
        ]))
        if query.from_user.id in user_login_data:
            del user_login_data[query.from_user.id]

@app.on_message(filters.private & filters.text & ~filters.command("start"))
async def login_flow(client: Client, message: Message):
    uid = message.from_user.id
    if uid not in user_login_data:
        return

    data = user_login_data[uid]
    step = data.get("step")
    text = message.text.strip()

    if step == "api_id":
        if not text.isdigit():
            return await message.reply_text(f"{E3} **{fancy('INVALID API ID')}**")
        data["api_id"] = int(text)
        data["step"] = "api_hash"
        await message.reply_text(f"{E1} **{fancy('API ID SAVED')}**\n\n{E2} **{fancy('Send API HASH:')}**")
    elif step == "api_hash":
        data["api_hash"] = text
        data["step"] = "phone"
        await message.reply_text(f"{E1} **{fancy('API HASH SAVED')}**\n\n{E2} **{fancy('Send Phone Number (no +):')}**")
    elif step == "phone":
        phone = text.replace("+", "").replace(" ", "")
        data["phone"] = phone
        data["step"] = "code"
        try:
            temp_client = Client(f"temp_{uid}", api_id=data["api_id"], api_hash=data["api_hash"], in_memory=True)
            await temp_client.connect()
            sent_code = await temp_client.send_code(phone)
            data["phone_code_hash"] = sent_code.phone_code_hash
            data["temp_client"] = temp_client
            await message.reply_text(f"{E2} **{fancy('CODE SENT')}**\n\n{E1} **{fancy('Enter OTP:')}**")
        except Exception as e:
            await message.reply_text(f"{E3} **{fancy('ERROR:')}** `{e}`")
            del user_login_data[uid]
    elif step == "code":
        code = text
        temp_client = data.get("temp_client")
        phone = data["phone"]
        phone_hash = data["phone_code_hash"]
        try:
            await temp_client.sign_in(phone_number=phone, phone_code_hash=phone_hash, phone_code=code)
            me = await temp_client.get_me()
            target_id = str(me.id) 
            session_string = await temp_client.export_session_string()
            
            db_data[target_id] = {
                "session_string": session_string,
                "api_id": data["api_id"],
                "api_hash": data["api_hash"],
                "is_worker": data.get("is_worker", False),
                "bots": []
            }
            
            if data.get("is_worker") and data.get("owner_id"):
                worker_owners[me.id] = data["owner_id"]
                db_data[target_id]["owner_id"] = data["owner_id"]
                
            save_db(db_data)
            
            user_app = Client(f"user_{me.id}", session_string=session_string, api_id=data["api_id"], api_hash=data["api_hash"])
            await user_app.start()
            active_clients[me.id] = user_app
            global_delays[me.id] = 0.1
            
            if TGCALLS:
                try:
                    calls = PyTgCalls(user_app)
                    await calls.start()
                    user_calls[me.id] = calls
                except: pass
                
            user_app.add_handler(MessageHandler(command_processor, filters.text & ~filters.bot))
            user_app.add_handler(MessageHandler(message_watcher, filters.incoming))
            
            role = "Worker" if data.get("is_worker") else "Owner"
            await message.reply_text(
                f"{E1} **{fancy('USERBOT DEPLOYED')}**\n\n"
                f"**{fancy('Account:')}** {me.first_name}\n"
                f"**{fancy('ID:')}** `{me.id}`\n"
                f"**{fancy('Role:')}** {role}\n\n"
                f"{E2} {fancy('Type help in any chat.')}"
            )
        except Exception as e:
            await message.reply_text(f"{E3} **{fancy('LOGIN FAILED:')}** `{e}`")
        finally:
            del user_login_data[uid]
            if temp_client:
                try: await temp_client.disconnect()
                except: pass
    elif step == "waiting_bot_tokens":
        tokens = re.split(r"[\s,]+", text)
        valid_bots = []
        for t in tokens:
            if ":" in t:
                try:
                    test_bot = Client(f"bot_{uid}_{t[:10]}", api_id=data["api_id"], api_hash=data["api_hash"], bot_token=t, in_memory=True)
                    await test_bot.start()
                    await test_bot.stop()
                    valid_bots.append(t)
                except: pass
        
        if valid_bots:
            db_data[str(uid)]["bots"].extend(valid_bots)
            save_db(db_data)
            await message.reply_text(f"{E1} **{fancy('SAVED')} {len(valid_bots)} {fancy('BOTS')}**")
        else:
            await message.reply_text(f"{E3} **{fancy('NO VALID TOKENS')}**")
        del user_login_data[uid]

# ==========================================
# 🕹️ COMMANDS PROCESSOR
# ==========================================
async def handle_bot_commands(client: Client, message: Message):
    uid = client.me.id
    if uid not in active_clients: return
    if uid in worker_owners: return 
    
    parts = message.text.strip().split(maxsplit=1)
    cmd = parts[0].lower()
    arg = parts[1] if len(parts) > 1 else ""
    
    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        try: await message.delete()
        except: pass

    if cmd == ".sbots":
        if not arg.isdigit(): return await client.send_message(uid, f"{E3} **{fancy('Usage: .sbots 5')}**")
        await client.send_message(uid, f"{E1} **{fancy('SEND BOT TOKENS:')}**")
        user_login_data[uid] = {"step": "waiting_bot_tokens", "api_id": db_data[str(uid)]["api_id"], "api_hash": db_data[str(uid)]["api_hash"]}

    elif cmd == ".addbots":
        if uid not in active_bots or not active_bots[uid]:
            tokens = db_data.get(str(uid), {}).get("bots", [])
            if not tokens: return await client.send_message(uid, f"{E3} **{fancy('No bots saved.')}**")
            active_bots[uid] = []
            for t in tokens:
                b = Client(f"bot_{uid}_{t[:10]}", api_id=db_data[str(uid)]["api_id"], api_hash=db_data[str(uid)]["api_hash"], bot_token=t)
                try:
                    await b.start()
                    active_bots[uid].append(b)
                except: pass
        
        if not active_bots[uid]: return
        chat_id = message.chat.id
        ok = 0
        for b in active_bots[uid]:
            try:
                bot_user = await b.get_users("me")
                await client.invite_chat_members(chat_id, bot_user.id)
                ok += 1
                await asyncio.sleep(0.5)
            except: pass
        m = await client.send_message(chat_id, f"{E2} **{fancy('ADDING BOTS')}** ◐")
        await spin(m, f"Added {ok} bots")

    elif cmd == ".nc":
        if not arg: return
        chat_id = message.chat.id
        if chat_id in bot_nc_tasks: return await client.send_message(chat_id, f"{E3} **{fancy('Loop active.')}**")
        if uid not in active_bots: return
        
        delay = bot_delays.get(uid, 1.0)
        emojis = ["🩷", "🤍", "🩵"]
        
        async def nc_loop():
            i = 0
            while True:
                try:
                    for b in active_bots[uid]:
                        try:
                            await asyncio.wait_for(b.set_chat_title(chat_id, f"{arg} {emojis[i%3]}"), timeout=10)
                            break 
                        except: pass
                    i += 1
                    await asyncio.sleep(delay)
                except asyncio.CancelledError: break
                except: await asyncio.sleep(2)
                
        bot_nc_tasks[chat_id] = asyncio.create_task(nc_loop())
        m = await client.send_message(chat_id, f"{E2} **{fancy('STARTING NAME LOOP')}** ◐")
        await spin(m, "Name loop started")

    elif cmd == ".delay":
        try: 
            bot_delays[uid] = max(0.1, float(arg))
            m = await client.send_message(message.chat.id, f"{E2} **{fancy('SETTING DELAY')}** ◐")
            await spin(m, f"Bot delay set to {bot_delays[uid]}s")
        except: 
            await client.send_message(message.chat.id, f"{E3} **{fancy('Usage: .delay 1.5')}**")

    elif cmd == ".rreply":
        if not message.reply_to_message or not arg: return
        chat_id = message.chat.id
        if uid not in active_bots: return
        if (chat_id, "rreply") in bot_spam_tasks: return
        
        delay = bot_delays.get(uid, 1.0)
        target_msg_id = message.reply_to_message.id
        
        async def br_loop():
            while True:
                try:
                    for b in active_bots[uid]:
                        msg = random.choice(RAID_TEMPLATES).format(name=arg)
                        await asyncio.wait_for(b.send_message(chat_id, msg, reply_to_message_id=target_msg_id), timeout=10.0)
                        await asyncio.sleep(delay)
                except (asyncio.TimeoutError, FloodWait, PeerFlood): await asyncio.sleep(10)
                except asyncio.CancelledError: break
                except: await asyncio.sleep(2)
                
        bot_spam_tasks[(chat_id, "rreply")] = asyncio.create_task(br_loop())
        m = await client.send_message(chat_id, f"{E2} **{fancy('STARTING BOT RAID')}** ◐")
        await spin(m, "Bot reply-raid started")

    elif cmd == ".rsall":
        if not arg: return
        chat_id = message.chat.id
        if uid not in active_bots: return
        if (chat_id, "rsall") in bot_spam_tasks: return
        
        async def brs_loop():
            replied = set()
            while True:
                try:
                    async for msg in client.get_chat_history(chat_id, limit=5):
                        if msg.id not in replied and msg.text:
                            for b in active_bots[uid]:
                                try: await asyncio.wait_for(b.send_message(chat_id, arg, reply_to_message_id=msg.id), timeout=10.0)
                                except: pass
                                await asyncio.sleep(0.2)
                            replied.add(msg.id)
                    await asyncio.sleep(2)
                except asyncio.CancelledError: break
                except: await asyncio.sleep(2)
                
        bot_spam_tasks[(chat_id, "rsall")] = asyncio.create_task(brs_loop())
        m = await client.send_message(chat_id, f"{E2} **{fancy('STARTING BOT REPLY-ALL')}** ◐")
        await spin(m, "Bot reply-all started")

    elif cmd == ".stop":
        chat_id = message.chat.id
        stopped = 0
        if chat_id in bot_nc_tasks:
            bot_nc_tasks[chat_id].cancel()
            del bot_nc_tasks[chat_id]
            stopped += 1
        if (chat_id, "rreply") in bot_spam_tasks:
            bot_spam_tasks[(chat_id, "rreply")].cancel()
            del bot_spam_tasks[(chat_id, "rreply")]
            stopped += 1
        if (chat_id, "rsall") in bot_spam_tasks:
            bot_spam_tasks[(chat_id, "rsall")].cancel()
            del bot_spam_tasks[(chat_id, "rsall")]
            stopped += 1
        m = await client.send_message(chat_id, f"{E3} **{fancy('STOPPING TASKS')}** ◐")
        await spin(m, f"Stopped {stopped} tasks")


async def command_processor(client: Client, message: Message):
    if not message.text: return
    if not message.outgoing: return 
    
    text = message.text.strip()
    uid = client.me.id 
    
    if text.startswith("."):
        await handle_bot_commands(client, message)
        return
        
    parts = text.split(maxsplit=1)
    cmd = parts[0].lower()
    arg = parts[1] if len(parts) > 1 else ""
    
    valid_cmds = ["help", "rreply", "rs", "rsall", "rstop", "rdelays", "adduser", "vjoin", "vleave", 
                  "pin", "unpin", "kick", "ban", "unban", "mute", "unmute", "promote", "demote", "tagall", "purge"]
    if cmd not in valid_cmds: return

    is_owner = (uid in active_clients) and (uid not in worker_owners)
    is_worker = uid in worker_owners
    if not (is_owner or is_worker): return 

    if cmd == "help":
        help_text = (
            f"{E2} **{fancy('S1N COMMANDS')}**\n\n"
            f"{E3} **{fancy('USERBOT & VOICE (No Prefix):')}**\n"
            f"{E1} `rreply <name>` - {fancy('Reply to target & raid')}\n"
            f"{E1} `rs <name>` - {fancy('Spam custom RS texts')}\n"
            f"{E1} `rsall <text>` - {fancy('Reply to EVERY message')}\n"
            f"{E1} `rstop` - {fancy('Stop raids & delete texts')}\n"
            f"{E1} `rdelays <sec>` - {fancy('Set delay (min 0.1)')}\n"
            f"{E1} `adduser` - {fancy('Add a worker userbot')}\n"
            f"{E1} `vjoin` / `vleave` - {fancy('Join/Leave Voice Chat')}\n\n"
            f"{E3} **{fancy('GROUP MANAGEMENT (No Prefix):')}**\n"
            f"{E1} `pin` `unpin` `kick` `ban` `unban`\n"
            f"{E1} `mute` `unmute` `promote` `demote`\n"
            f"{E1} `purge` `tagall`\n\n"
            f"{E3} **{fancy('BOT NETWORK (. Prefix):')}**\n"
            f"{E1} `.sbots <amount>` - {fancy('Add bot tokens')}\n"
            f"{E1} `.addbots` - {fancy('Invite bots to group')}\n"
            f"{E1} `.nc <text>` - {fancy('Loop group name')}\n"
            f"{E1} `.delay <sec>` - {fancy('Set bot delay')}\n"
            f"{E1} `.rreply / .rsall / .stop`\n\n"
            f"**{fancy('Status:')}** {E1} {fancy('Ready')}"
        )
        try: await message.edit_text(help_text)
        except: await message.reply_text(help_text)
        return

    try: await message.delete()
    except: pass

    # ====== VOICE COMMANDS ======
    if cmd in ["vjoin", "vleave"]:
        if not TGCALLS: return await client.send_message(message.chat.id, f"{E3} **{fancy('Voice module not installed.')}**")
        if message.chat.type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            return await client.send_message(message.chat.id, f"{E3} **{fancy('Use in a group.')}**")
            
        if cmd == "vjoin":
            try:
                calls = user_calls.get(uid)
                if not calls: return await client.send_message(message.chat.id, f"{E3} **{fancy('VC module failed to start.')}**")
                await calls.play(message.chat.id, MediaStream("https://github.com/pytgcalls/pytgcalls/raw/master/tests/test.mp3"))
                m = await client.send_message(message.chat.id, f"{E2} **{fancy('JOINING VC')}** ◐")
                await spin(m, "Joined Voice Chat")
            except Exception as e:
                await client.send_message(message.chat.id, f"{E3} **{fancy('VC Error:')}** `{e}`")
                
        elif cmd == "vleave":
            try:
                calls = user_calls.get(uid)
                if calls:
                    await calls.leave_call(message.chat.id)
                m = await client.send_message(message.chat.id, f"{E2} **{fancy('LEAVING VC')}** ◐")
                await spin(m, "Left Voice Chat")
            except Exception as e:
                pass

    # ====== GROUP MANAGEMENT ======
    elif cmd in ["pin", "unpin", "kick", "ban", "unban", "mute", "unmute", "promote", "demote"]:
        if not is_owner: return await client.send_message(message.chat.id, f"{E3} **{fancy('Owner only.')}**")
        if not message.reply_to_message: return await client.send_message(message.chat.id, f"{E3} **{fancy('Reply to a user.')}**")
        target = message.reply_to_message.from_user.id
        try:
            if cmd == "pin": await message.reply_to_message.pin()
            elif cmd == "unpin": await client.unpin_all_chat_messages(message.chat.id)
            elif cmd == "kick":
                await client.ban_chat_member(message.chat.id, target)
                await client.unban_chat_member(message.chat.id, target)
            elif cmd == "ban": await client.ban_chat_member(message.chat.id, target)
            elif cmd == "unban": await client.unban_chat_member(message.chat.id, target)
            elif cmd == "mute": await client.restrict_chat_member(message.chat.id, target, ChatPermissions())
            elif cmd == "unmute": await client.restrict_chat_member(message.chat.id, target, ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True))
            elif cmd == "promote": await client.promote_chat_member(message.chat.id, target, can_change_info=True, can_delete_messages=True, can_ban_users=True, can_invite_users=True, can_pin_messages=True, can_manage_chat=True)
            elif cmd == "demote": await client.promote_chat_member(message.chat.id, target)
            m = await client.send_message(message.chat.id, f"{E2} **{fancy('PROCESSING')}** ◐")
            await spin(m, f"{cmd.capitalize()} successful")
        except Exception as e:
            await client.send_message(message.chat.id, f"{E3} **{fancy('Failed:')}** `{e}`")

    elif cmd == "tagall":
        if not is_owner: return
        members = []
        async for m in client.get_chat_members(message.chat.id):
            if not m.user.is_bot:
                members.append(f"[{m.user.first_name}](tg://user?id={m.user.id})")
        await client.send_message(message.chat.id, f"🔔 **{fancy('TAGGING ALL')}**\n\n{' '.join(members)}")
        
    elif cmd == "purge":
        if not is_owner: return
        if not message.reply_to_message: return await client.send_message(message.chat.id, f"{E3} **{fancy('Reply to start.')}**")
        msg_ids = list(range(message.reply_to_message.id, message.id))
        await client.delete_messages(message.chat.id, msg_ids)

    # ====== USERBOT RAID ======
    elif cmd == "rreply":
        if not is_owner or not arg or not message.reply_to_message: return
        target_name = arg
        chat_id = message.chat.id
        if (uid, chat_id) in spam_tasks: return
        
        delay = global_delays.get(uid, 0.1)
        raid_messages[(uid, chat_id)] = []
        
        async def raid_loop():
            while True:
                try:
                    msg = random.choice(RAID_TEMPLATES).format(name=target_name)
                    sent = await asyncio.wait_for(client.send_message(chat_id, msg, reply_to_message_id=message.reply_to_message.id), timeout=10.0)
                    raid_messages[(uid, chat_id)].append(sent.id)
                    await asyncio.sleep(delay)
                except (asyncio.TimeoutError, FloodWait, PeerFlood): await asyncio.sleep(5)
                except asyncio.CancelledError: break
                except: await asyncio.sleep(1)
        spam_tasks[(uid, chat_id)] = asyncio.create_task(raid_loop())
        m = await client.send_message(chat_id, f"{E2} **{fancy('STARTING RAID')}** ◐")
        await spin(m, f"Raid started on {target_name}")

    elif cmd == "rs":
        if not is_owner or not arg: return
        target_name = arg
        chat_id = message.chat.id
        if (uid, chat_id) in spam_tasks: return
        
        delay = global_delays.get(uid, 0.1)
        raid_messages[(uid, chat_id)] = []
        
        async def rs_loop():
            while True:
                try:
                    msg = random.choice(RS_TEMPLATES).format(name=target_name)
                    sent = await asyncio.wait_for(client.send_message(chat_id, msg), timeout=10.0)
                    raid_messages[(uid, chat_id)].append(sent.id)
                    await asyncio.sleep(delay)
                except (asyncio.TimeoutError, FloodWait, PeerFlood): await asyncio.sleep(10)
                except asyncio.CancelledError: break
                except Exception: await asyncio.sleep(2)
                
        spam_tasks[(uid, chat_id)] = asyncio.create_task(rs_loop())
        m = await client.send_message(chat_id, f"{E2} **{fancy('STARTING RS RAID')}** ◐")
        await spin(m, f"RS Raid started on {target_name}")

    elif cmd == "rsall":
        if not is_owner or not arg: return
        chat_id = message.chat.id
        rsall_tasks[chat_id] = arg
        m = await client.send_message(chat_id, f"{E2} **{fancy('ACTIVATING REPLY-ALL')}** ◐")
        await spin(m, "Reply-all activated")

    elif cmd == "rstop":
        if not is_owner: return
        chat_id = message.chat.id
        
        if (uid, chat_id) in spam_tasks:
            spam_tasks[(uid, chat_id)].cancel()
            del spam_tasks[(uid, chat_id)]
            msgs = raid_messages.get((uid, chat_id), [])
            for i in range(0, len(msgs), 100):
                try: await client.delete_messages(chat_id, msgs[i:i+100])
                except: pass
            raid_messages[(uid, chat_id)] = []
        
        if chat_id in rsall_tasks:
            del rsall_tasks[chat_id]
            
        m = await client.send_message(chat_id, f"{E3} **{fancy('STOPPING TASKS')}** ◐")
        await spin(m, "Raids stopped & cleaned")

    elif cmd == "rdelays":
        if not is_owner or not arg: return
        try:
            global_delays[uid] = max(0.1, float(arg))
            m = await client.send_message(message.chat.id, f"{E2} **{fancy('SETTING DELAY')}** ◐")
            await spin(m, f"Delay set to {global_delays[uid]}s")
        except: pass

    elif cmd == "adduser":
        if not is_owner: return
        try:
            await app.send_message(
                uid,
                f"{E2} **{fancy('ADD WORKER')}**\n\n{E1} Send API ID (or /cancel):",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("𝐶𝐴𝑁𝐶𝐸𝐿", callback_data="back_to_start")]])
            )
            user_login_data[uid] = {"step": "api_id", "is_worker": True, "owner_id": uid}
            m = await client.send_message(message.chat.id, f"{E1} **{fancy('CHECK YOUR PM TO ADD WORKER.')}**")
            await asyncio.sleep(3)
            await m.delete()
        except Exception:
            await client.send_message(message.chat.id, f"{E3} **{fancy('Start the hoster bot in PM first!')}**")

# ==========================================
# 🏃‍♂️ MAIN ENTRY POINT
# ==========================================
async def main():
    await app.start()
    print(f"{E1} {fancy('S1N HOSTER BOT is running...')}")
    
    for uid_str, info in db_data.items():
        uid = int(uid_str)
        try:
            user_app = Client(f"user_{uid}", session_string=info["session_string"], api_id=info["api_id"], api_hash=info["api_hash"])
            await user_app.start()
            active_clients[uid] = user_app
            global_delays[uid] = 0.1
            
            if info.get("is_worker") and info.get("owner_id"):
                worker_owners[uid] = info["owner_id"]
                
            if TGCALLS:
                try:
                    calls = PyTgCalls(user_app)
                    await calls.start()
                    user_calls[uid] = calls
                except: pass
                
            user_app.add_handler(MessageHandler(command_processor, filters.text & ~filters.bot))
            user_app.add_handler(MessageHandler(message_watcher, filters.incoming))
            
            tokens = info.get("bots", [])
            if tokens:
                active_bots[uid] = []
                for t in tokens:
                    try:
                        b = Client(f"bot_{uid}_{t[:10]}", api_id=info["api_id"], api_hash=info["api_hash"], bot_token=t)
                        await b.start()
                        active_bots[uid].append(b)
                    except: pass
            
            print(f"{E2} {fancy('Restarted userbot for')} {uid}")
        except Exception as e:
            print(f"{E3} {fancy('Failed to restart')} {uid}: {e}")
    
    await idle()

if __name__ == "__main__":
    app.run(main())