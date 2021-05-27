  
'''
using discord.py version 1.0.0a
'''
import discord
import asyncio
import re
import multiprocessing
import threading
import concurrent

#BOT_OWNER_ROLE = 'Runner' # change to what you need
#BOT_OWNER_ROLE_ID = "846601968758816778" 
  
g="https://discord.gg/eZWtQXUt2z" 

 
oot_channel_id_list = [
"738029551057109012","739816601712328794" #pride
]

answer_pattern = re.compile(r'(not|n)?([1-4]{1})(\?)?(cnf)?(\?)?$', re.IGNORECASE)

apgscore = 800
nomarkscore = 500
markscore = 400

async def update_scores(content, answer_scores):
    global answer_pattern

    m = answer_pattern.match(content)
    if m is None:
        return False

    ind = int(m[2])-1

    if m[1] is None:
        if m[3] is None:
            if m[4] is None:
                answer_scores[ind] += nomarkscore
            else: # apg
                if m[5] is None:
                    answer_scores[ind] += apgscore
                else:
                    answer_scores[ind] += markscore

        else: # 1? ...
            answer_scores[ind] += markscore

    else: # contains not or n
        if m[3] is None:
            answer_scores[ind] -= nomarkscore
        else:
            answer_scores[ind] -= markscore

    return True

class SelfBot(discord.Client):

    def __init__(self, update_event, answer_scores):
        super().__init__()
        global oot_channel_id_list
        self.oot_channel_id_list = oot_channel_id_list
        self.update_event = update_event
        self.answer_scores = answer_scores

    async def on_ready(self):
        print("======================")
        print("Nelson Trivia Self Bot")
        print("Connected to discord.")
        print("User: " + self.user.name)
        print("ID: " + str(self.user.id))

    # @bot.event
    # async def on_message(message):
    #    if message.content.startswith('-debug'):
    #         await message.channel.send('d')

        def is_scores_updated(message):
            if message.guild == None or \
                str(message.channel.id) not in self.oot_channel_id_list:
                return False

            content = message.content.replace(' ', '').replace("'", "")
            m = answer_pattern.match(content)
            if m is None:
                return False

            ind = int(m[2])-1

            if m[1] is None:
                if m[3] is None:
                    if m[4] is None:
                        self.answer_scores[ind] += nomarkscore
                    else: # apg
                        if m[5] is None:
                            self.answer_scores[ind] += apgscore
                        else:
                            self.answer_scores[ind] += markscore

                else: # 1? ...
                    self.answer_scores[ind] += markscore

            else: # contains not or n
                if m[3] is None:
                    self.answer_scores[ind] -= nomarkscore
                else:
                    self.answer_scores[ind] -= markscore

            return True

        while True:
            await self.wait_for('message', check=is_scores_updated)
            self.update_event.set()

class Bot(discord.Client):

    def __init__(self, answer_scores):
        super().__init__()
        self.bot_channel_id_list = []
        self.embed_msg = None
        self.embed_channel_id = None
        self.answer_scores = answer_scores

        # embed creation
        #don't edit here
        self.embed=discord.Embed(title="",description =f"MALL91 GOOGLE RESULTS",colour=0xFBC0AC)
        

        #await self.bot.add_reaction(embed,':spy:')


    async def clear_results(self):
        for i in range(len(self.answer_scores)):
            self.answer_scores[i]=0

    async def update_embeds(self):
      #  global wrong

         

        one_check = ""
        two_check = ""
        three_check = ""
        four_check = ""
        not_answer = "?"
        

        lst_scores = list(self.answer_scores)
        

        highest = max(lst_scores)
        gif_ans = 'https://cdn.discordapp.com/attachments/716879425655799858/726460742924107897/unnamed.gif'
        not_answer = ' '
        lowest = min(lst_scores)
        answer = lst_scores.index(highest)+1
        best_answer= "<a:go:827024394978983937>"
        #global wrong             

        if highest > 0:
            if answer == 1:
                one_check = "<a:gold:827024591439265792>"
                best_answer = ":one:"
                gif_ans = "https://cdn.discordapp.com/attachments/720850437041029181/743345493207154778/723415445167931452.png"
            else:
                one_check = "❌ "
                not_answer = " Option:- 1<:emoji_53:703553522943393792>  "
                

            if answer == 2:
                two_check = "<a:gold:827024591439265792>"
                best_answer = ":two:"
                gif_ans = "https://cdn.discordapp.com/attachments/720850437041029181/743345493966454885/723416002666299433.png"
            else:
                two_check = ""
                not_answer = " Option:- 2<:emoji_53:703553522943393792>  "
                

            if answer == 3:
                three_check = "<a:gold:827024591439265792>"
                best_answer = ":three:"
                gif_ans = "https://cdn.discordapp.com/attachments/720850437041029181/743345494142615612/723418348834258974.png"
            else:
                three_check = ""
                not_answer = " Option:- 3<:emoji_53:703553522943393792>  "
                
     
            if answer == 4:
                four_check = "<a:gold:827024591439265792>"
                best_answer = ":four:"
                gif_ans = "https://cdn.discordapp.com/attachments/720850437041029181/743345494280896562/723419217650647090.png"
            else:
                four_check = ""
                not_answer = " Option:- 4<:emoji_53:703553522943393792>  "
                

            

        #if lowest < 0:
           # if answer == 2:
             #   one_cheak = ":x:"
          #  if answer == 3:
         #       two_cheak = ":x:"
       #     if answer == 1:
         #       three_cheak = ":x:"
          #only edit here
        self.embed.set_field_at(0, name=f"**__𝙾𝚙𝚝𝚒𝚘𝚗❶__** {check_one}", value="**{0}.0**{1}".format(lst_scores[0], one_check))
        self.embed.set_field_at(1, name=f"**__𝙾𝚙𝚝𝚒𝚘𝚗❷__** {check_two}", value="**{0}.0**{1}".format(lst_scores[1], two_check))
        self.embed.set_field_at(2, name=f"**__𝙾𝚙𝚝𝚒𝚘𝚗❸__** {check_three}", value="**{0}.0**{1}".format(lst_scores[2], three_check))
        self.embed.set_field_at(3, name=f"**__𝙾𝚙𝚝𝚒𝚘𝚗❹__** {check_four}", value="**{0}.0**{1}".format(lst_scores[3], four_check))
        
        
        if self.embed_msg is not None:
            await self.embed_msg.edit(embed=self.embed)

    async def on_ready(self):
        print("==============")
        print("🎭Trivia H@çks||Official🎭")
        print("Connected to discord.")
        print("User: " + self.user.name)
        print("ID: " + str(self.user.id))
       #log=self.get_channel(743327232881197066)
       #await log.send("> **HQ Trivia Bot Is Updated** ✅")

        await self.clear_results()
        await self.update_embeds()
        #await self.change_presence(activity=discord.Game(name='with '+str(len(set(self.get_all_members())))+' users'))
        await self.change_presence(activity=discord.Activity(type=1,name="TECHNO KUMU"))

    async def on_message(self, message):


        # if message is private
        if message.author == self.user or message.guild == None:
            return

        if message.content.lower() == "m":
            await message.delete()
            
            self.embed_msg = None
            await self.clear_results()
            await self.update_embeds()
            self.embed_msg = \
                await message.channel.send('',embed=self.embed)
            #await self.embed_msg.add_reaction("<a:levelup:827049375566004274>")
            await self.embed_msg.add_reaction("<a:levelup:827049375566004274>")
            self.embed_channel_id = message.channel.id
       

          

        # process votes
        if message.channel.id == self.embed_channel_id:
            content = message.content.replace(' ', '').replace("'", "")
            updated = await update_scores(content, self.answer_scores)
            if updated:
                await self.update_embeds()

def bot_with_cyclic_update_process(update_event, answer_scores):

    def cyclic_update(bot, update_event):
        f = asyncio.run_coroutine_threadsafe(bot.update_embeds(), bot.loop)
        while True:
            update_event.wait()
            update_event.clear()
            f.cancel()
            f = asyncio.run_coroutine_threadsafe(bot.update_embeds(), bot.loop)
            #res = f.result()

    bot = Bot(answer_scores)

    upd_thread = threading.Thread(target=cyclic_update, args=(bot, update_event))
    upd_thread.start()

    loop = asyncio.get_event_loop()
    loop.create_task(bot.start('ODQ1MjQ2OTkzNDYyNDYwNDE2.YKeLmw.YIvJC_--23aJA3VGo5_jbaTOf5k'))
    loop.run_forever()


def selfbot_process(update_event, answer_scores):

    selfbot = SelfBot(update_event, answer_scores)

    loop = asyncio.get_event_loop()
    loop.create_task(selfbot.start('NzgyMjUwNjYzOTI1MTIxMDM0.YKohjQ.UqyELBtHlWo6EbWzeF02THBRaBU',
                                   bot=False))
    loop.run_forever()

if __name__ == '__main__':

    # running bot and selfbot in separate OS processes

    # shared event for embed update
    update_event = multiprocessing.Event()

    # shared array with answer results
    answer_scores = multiprocessing.Array(typecode_or_type='i', size_or_initializer=4)

    p_bot = multiprocessing.Process(target=bot_with_cyclic_update_process, args=(update_event, answer_scores))
    p_selfbot = multiprocessing.Process(target=selfbot_process, args=(update_event, answer_scores))

    p_bot.start()
    p_selfbot.start()

    p_bot.join()
    p_selfbot.join()




 
 
