import discord
from discord.ext import commands
from discord.ui import View, Button
from discord import app_commands
import os

intents = discord.Intents.all()
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

@bot.tree.command(name="avatar", description="このbotのアイコンを貼ります。")
async def avatar(interaction: discord.Interaction):
    await interaction.response.send_message("https://i.imgur.com/dU9gpoh.jpeg")


class PaginatorView(View):
    def __init__(self, pages, next_pages_provider=None, is_final_view=False):
        """
        :param pages: List of strings for the current pagination.
        :param next_pages_provider: A function that takes the selected topic index and returns pages for the next view.
        :param is_final_view: Boolean indicating if this is the final view.
        """
        super().__init__(timeout=120)
        self.pages = pages
        self.current_page = 0
        self.message = None
        self.is_final_view = is_final_view
        self.next_pages_provider = next_pages_provider
        self.selected_topic = None

        # Remove the "OK" button if this is the final view
        if self.is_final_view:
            self.remove_item(self.ok)

    def create_embed(self):
        """Create an embed for the current page."""
        page_content = self.pages[self.current_page]
        # Split content into text and image URL
        if "\nhttps://" in page_content:
            description, image_url = page_content.split("\nhttps://", 1)
            image_url = "https://" + image_url  # Re-add the protocol
        else:
            description = page_content
            image_url = None

        embed = discord.Embed(
            title=f"{self.current_page + 1}/{len(self.pages)} ページ",
            description=description,
            color=discord.Color.blurple()
        )
        if image_url:
            embed.set_image(url=image_url)

        return embed

    async def update_message(self, interaction):
        """Update the embed and the view when changing pages."""
        embed = self.create_embed()
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="前のページ", style=discord.ButtonStyle.blurple, disabled=True)
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page -= 1
        if self.current_page == 0:
            button.disabled = True
        self.next_page.disabled = False
        await self.update_message(interaction)

    @discord.ui.button(label="次のページ", style=discord.ButtonStyle.blurple)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page += 1
        if self.current_page == len(self.pages) - 1:
            button.disabled = True
        self.previous_page.disabled = False
        await self.update_message(interaction)

    @discord.ui.button(label="OK", style=discord.ButtonStyle.green, row=1)
    async def ok(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.selected_topic = self.current_page
        if self.next_pages_provider:
            # Generate the next view based on the selected topic
            next_pages = self.next_pages_provider(self.selected_topic)
            next_view = PaginatorView(next_pages, is_final_view=True)
            embed = next_view.create_embed()
            await interaction.response.edit_message(embed=embed, view=next_view)
        else:
            await interaction.response.defer()  # No action for the final view
        self.stop()  # Stop the current view



@bot.event
async def on_ready():
    await tree.sync()
    print("Botが正常にログインしました")


@tree.command(name="shakehelp", description="アライトの基礎的なシェイクのやり方を教えます")
async def book(interaction: discord.Interaction):
    pages = [
        "**ピンチ・バルジを使った波紋みたいなシェイク**\nイメージGIF\nhttps://i.ibb.co/x6hYY4d/1130-2-Trim.gif",
        "**ピンチ・バルジを使った吸い込まれるようなシェイク**\nイメージGIF\nhttps://i.ibb.co/NnjkvcW/youtube-lfm0-FX17-WDw-Trim.gif",
        "**スイングを使った回転シェイク**\nイメージGIF\nhttps://i.ibb.co/BZk7RPz/youtube-Nb-sq-SM8n8-Trim-Trim.gif",
        "**スイングを使った回転シェイク(その2)**\nイメージGIF\nhttps://i.ibb.co/ChKyKF7/youtube-lfm0-FX17-WDw-Trim-Trim-1.gif",
        "**横から来るシェイク**\nイメージGIF\nhttps://i.ibb.co/mTZMFRS/6-Trim.gif",
        "**横から来て吸い込まれるシェイク**\nイメージGIF\nhttps://i.ibb.co/wrDzftz/youtube-K1-Ja-WKV5-FL4-Trim.gif"
    ]

    def get_next_pages(selected_index):
        """Return the next set of pages based on the selected topic."""
        topic_details = {
            0: [
                "**1：タイルを表示させるを用意する。**\nミラーをONにすることを忘れないように。",
                "**2：オートシェイクを用意する。**\nキーフレームは頻度とマグニチュードにつけ、画像のように4つ等間隔に置く。ただし頻度のところでは最後1つにはつけない\nマグニチュード：500 > 0 > 0 > 500\n頻度：15 > 0 > 15\nたるみ：100\nhttps://i.ibb.co/TwCcg2w/2024-12-08-100555.png",
                "**3：1のキーフレームにイージングをつける。**\nこれをマグニチュード、頻度のところにつける。ただし頻度のところでは最初のグラフをつけるだけでOK。\nhttps://i.ibb.co/7YKjfdV/2024-12-08-100038.png",
                "**4：ピンチ&バルジを用意する。**\nキーフレームを強度のみ画像のようにつける。\n強度：1 > 0\n半径：2.5\nイージングは以下のようにグラフをつける。\nhttps://i.ibb.co/ftvKqxQ/2024-12-08-100752.png",
                "**5：円形リップルを用意する。**\nキーフレームを強度のみ画像のようにつける。\n頻度：1\n強度：0.4 > 0\n半径：0.8\nイージングは以下のようにグラフをつける。\nhttps://i.ibb.co/ftvKqxQ/2024-12-08-100752.png",
                "**6：最後にモーションブラーをつけて完成！**\nhttps://i.ibb.co/x6hYY4d/1130-2-Trim.gif"
            ],
            1: [
                "**1：タイルを表示させるを用意する。**\nミラーをONにすることを忘れないように。",
                "**2：ピンチ&バルジを用意する。**\nキーフレームを強度のみ画像のようににつける。\n強度：1 > 0\n半径：2.5\nイージングは以下のようにグラフをつける。\nhttps://i.ibb.co/PMZjdP7/2024-12-09-074336.png",
                "**3：円形リップルを用意する。**\nキーフレームを強度のみ画像のようにつける。\n頻度：1\n強度：0.4 > 0\n半径：0.8\nイージングは以下のようにグラフをつける。\nhttps://i.ibb.co/PMZjdP7/2024-12-09-074336.png",
                "**4：ピンチ&バルジをもう1個用意する。**\nキーフレームを強度のみ画像のようににつける。\n強度：0 > 0.8\n半径：2.5\nイージングは以下のようにグラフをつける。\nhttps://i.ibb.co/jLqygcg/2024-12-09-074156.png",
                "**5：完成！**\nhttps://i.ibb.co/NnjkvcW/youtube-lfm0-FX17-WDw-Trim.gif"
            ],  
            2: [
                "**1：タイルを表示させるを用意する。**\nミラーをONにすることを忘れないように。",
                "**2：スイングを用意する。**\n角度1、角度2両方にキーフレームを画像のようつける。\n頻度：0.1\n角度1、角度2の両方：-90 > 90\nイージングは以下のようにグラフをつける。\nhttps://i.ibb.co/N6LtHCL/2024-12-08-104836.png",
                "**3：ピンチ&バルジを用意する。**\nキーフレームを強度のみ画像のようにつける。\n強度：0.5 > 0\n半径：2.5\nイージングは以下のようにグラフをつける。\nhttps://i.ibb.co/ftvKqxQ/2024-12-08-100752.png",
                "**4：ランダム変位を用意する。**\nキーフレームをエボリューションのみ画像のようにつける。\nマグニチュード：50\nエボリューション：0 > 1.5\nイージングはつけない。\nhttps://i.ibb.co/NYZvNPC/2024-12-08-100705.png",
                "**5：スワールを用意する。**\nキーフレームを強度のみ画像のようにつける。\n強度：0.05 > 0\n半径：0.8\nイージングは以下のようにグラフをつける。\nhttps://i.ibb.co/ftvKqxQ/2024-12-08-100752.png",
                "**6：最後にモーションブラーをつけて値を0.50にいじれば完成！**\nhttps://i.ibb.co/BZk7RPz/youtube-Nb-sq-SM8n8-Trim-Trim.gif"
            ],
            3: [
                "**1：タイルを表示させるを用意する。**\nミラーをONにすることを忘れないように。",
                "**2：スイングを用意する。**\n角度1、角度2両方にキーフレームを画像のようつける。\n頻度：0.1\n角度1、角度2の両方：-25 > 25\nイージングは以下のようにグラフをつける。\nhttps://i.ibb.co/N6LtHCL/2024-12-08-104836.png",
                "**3：ピンチ&バルジを用意する。**\nキーフレームを強度のみ画像のようにつける。\n強度：0.25 > 0\n半径：2.5\nイージングはつけない。\nhttps://i.ibb.co/NYZvNPC/2024-12-08-100705.png",
                "**4：完成！**\nhttps://i.ibb.co/ChKyKF7/youtube-lfm0-FX17-WDw-Trim-Trim-1.gif"
            ],
            4: [
                "**1：タイルを表示させるを用意する。**\nミラーをONにすることを忘れないように。",
                "**2：スイングを用意する。**\n角度1、角度2両方にキーフレームを画像のようつける。\n頻度：0.1\n角度1、角度2の両方：-20 > 0\nイージングは以下のようにグラフをつける。\nhttps://i.ibb.co/NjMf4XB/2024-12-08-113350.png",
                "**3：ピンチ&バルジを用意する。**\nキーフレームを強度のみ画像のようにつける。\n強度：0 > 0.25\n半径：2.5\nイージングはつけない。\nhttps://i.ibb.co/NYZvNPC/2024-12-08-100705.png",
                "**4：振動を用意する。**\nキーフレームをマグニチュードのみ画像のようにつける。\n角度：180\n頻度：0\nマグニチュード：350 > 0\n位相：0.25\nイージングは以下のようにグラフをつける。\nhttps://i.ibb.co/ftvKqxQ/2024-12-08-100752.png",
                "**5：モーションブラーを用意する。**\n見にくかったら値を0.75くらいにいじると良い。",
                "**6：方向ブラーを用意する。**キーフレームは強度につけ、4つ等間隔に画像のようつける。\n強度：0.25 > 0 > 0 > 0.25\n角度：0\nイージングは以下のようにグラフをつける。\nhttps://i.ibb.co/7YKjfdV/2024-12-08-100038.png",
                "**7：レイヤーを複製する。**\n複製したレイヤーはさっきのレイヤーの出番が終わるタイミングで始まるように開始位置を長押しでずらす。",
                "**8：スイングと振動の数値をいじる。**\n複製したレイヤーに移動し、スイングの角度1と角度2を20 > 0に、振動の角度を0にする。",
                "**9：完成！**\nhttps://i.ibb.co/mTZMFRS/6-Trim.gif",
            ],
            5: [
                "**1：タイルを表示させるを用意する。**\nミラーをONにすることを忘れないように。",
                "**2：スイングを用意する。**\n角度1、角度2両方の数字をいじる。キーフレームはつけない。\n頻度：0.1\n角度1、角度2の両方：-10",
                "**3：ピンチ&バルジを用意する。**\nキーフレームを強度のみ画像のようにつける。\n強度：0.75 > 0 > 0.75\n半径：1.5\nイージングはつけない。\nhttps://i.ibb.co/C14snwY/2025-01-06-095508.png",
                "**4：振動を用意する。**\nキーフレームをマグニチュードのみ画像のようにつける。\n角度：180\n頻度：0\nマグニチュード：350 > 0\n位相：0.25\nイージングは以下のようにグラフをつける。\nhttps://i.ibb.co/ftvKqxQ/2024-12-08-100752.png",
                "**5：モーションブラーを用意する。**\n見にくかったら値を0.75くらいにいじると良い。",
                "**6：方向ブラーを用意する。**キーフレームは強度につけ、4つ等間隔に画像のようつける。\n強度：0.25 > 0 > 0 > 0.25\n角度：0\nイージングは以下のようにグラフをつける。\nhttps://i.ibb.co/7YKjfdV/2024-12-08-100038.png",
                "**7：レイヤーを複製する。**\n複製したレイヤーはさっきのレイヤーの出番が終わるタイミングで始まるように開始位置を長押しでずらす。",
                "**8：スイングと振動の数値をいじる。**\n複製したレイヤーに移動し、スイングの角度1と角度2を10に、振動の角度を0にする。",
                "**9：完成！**\nhttps://i.ibb.co/n8hLFpL/youtube-K1-Ja-WKV5-FL4-Trim.gif",
            ]
        }
        return topic_details.get(selected_index, ["No follow-up details available."])


    view = PaginatorView(pages, next_pages_provider=get_next_pages)
    embed = view.create_embed()
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

bot.run(os.getenv("TOKEN"))