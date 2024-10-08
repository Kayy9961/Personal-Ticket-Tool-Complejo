import discord
from discord.ext import commands
from discord.ui import Button, View, Select
import asyncio
import requests

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

canal_id = int(input("Por favor, ingresa el ID del canal donde deseas enviar el botón de crear ticket: "))
informacion_canal_id = 1271642274605961268  

ALLOWED_USER_ID = 1238471224510648412  

FOLLOWERS_IMAGE_URL = "https://raw.githubusercontent.com/Kayy9961/Data-Base-Personal/main/Seggg.png"

def realizar_pedido(url, seguidores, service_id, category, service_name, use_alternate_api=False):
    if category == "Instagram" and service_name == "Seguidores" and service_id == 9043:
        api_endpoint = "TU API DE TU PANEL PRINCIPAL" 
        api_key = "TU API KEY DE TU PANEL PRINCIPAL"  

    elif use_alternate_api or (category == "TikTok" or (category == "Instagram" and service_name != "Likes")):
        api_endpoint = "TU API DE TU PANEL 2 (NO OBLIGATORIO)"  
        api_key = "TU API KEY DE TU PANEL 2 (NO OBLIGATORIO)" 
    else:
        api_endpoint = "TU API DE TU PANEL 3 (NO OBLIGATORIO)"  
        api_key = "TU API KEY DE TU PANEL 3 (NO OBLIGATORIO)" 

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "key": api_key,
        "action": "add",
        "service": service_id,
        "link": url,
        "quantity": seguidores
    }

    try:
        response = requests.post(api_endpoint, headers=headers, json=data)
        response.raise_for_status()
        return "success"
    except requests.exceptions.ConnectionError as e:
        return f"Error de conexión: {e}"
    except requests.exceptions.HTTPError as e:
        return f"Error HTTP: {e}"
    except requests.exceptions.RequestException as e:
        return f"Error durante la solicitud HTTP: {e}"



class PersistentPlatformSelectView(View):
    def __init__(self):
        super().__init__(timeout=None)  
        self.instagram_button = Button(label="Instagram", style=discord.ButtonStyle.primary, custom_id="platform_instagram_unique")
        self.tiktok_button = Button(label="TikTok", style=discord.ButtonStyle.primary, custom_id="platform_tiktok_unique")
        self.cerrar_ticket_button = Button(label="Cerrar Ticket", style=discord.ButtonStyle.danger, custom_id="platform_cerrar_ticket_unique")

        self.instagram_button.callback = self.instagram
        self.tiktok_button.callback = self.tiktok
        self.cerrar_ticket_button.callback = self.cerrar_ticket

        self.add_item(self.instagram_button)
        self.add_item(self.tiktok_button)
        self.add_item(self.cerrar_ticket_button)

    async def instagram(self, interaction: discord.Interaction):
        try:
            print("Instagram button clicked!") 
            await interaction.response.defer()  
            await interaction.message.edit(content="Buena elección, ahora elige el servicio:", view=SocialMediaView(category="Instagram"))
        except Exception as e:
            print(f"Error in Instagram button: {e}")  

    async def tiktok(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await interaction.message.edit(content="Buena elección, ahora elige el servicio:", view=SocialMediaView(category="TikTok"))

    async def cerrar_ticket(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await interaction.channel.delete()

class SocialMediaView(View):
    def __init__(self, category):
        super().__init__(timeout=None)
        self.category = category

        if category == "Instagram":
            self.seguidores_button = Button(label="Seguidores Instagram", style=discord.ButtonStyle.primary, custom_id="insta_seguidores_unique")
            self.likes_button = Button(label="Likes Instagram", style=discord.ButtonStyle.primary, custom_id="insta_likes_unique")
            self.visitas_button = Button(label="Visitas Instagram", style=discord.ButtonStyle.primary, custom_id="insta_visitas_unique")

            self.seguidores_button.callback = self.select_service_quantity
            self.likes_button.callback = self.select_service_quantity
            self.visitas_button.callback = self.select_service_quantity

            self.add_item(self.seguidores_button)
            self.add_item(self.likes_button)
            self.add_item(self.visitas_button)

        elif category == "TikTok":
            self.seguidores_button = Button(label="Seguidores TikTok", style=discord.ButtonStyle.primary, custom_id="tiktok_seguidores_unique")
            self.likes_button = Button(label="Likes TikTok", style=discord.ButtonStyle.primary, custom_id="tiktok_likes_unique")
            self.visitas_button = Button(label="Visitas TikTok", style=discord.ButtonStyle.primary, custom_id="tiktok_visitas_unique")
            self.compartidos_button = Button(label="Compartidos TikTok", style=discord.ButtonStyle.primary, custom_id="tiktok_compartidos_unique")

            self.seguidores_button.callback = self.select_service_quantity
            self.likes_button.callback = self.select_service_quantity
            self.visitas_button.callback = self.select_service_quantity
            self.compartidos_button.callback = self.select_service_quantity

            self.add_item(self.seguidores_button)
            self.add_item(self.likes_button)
            self.add_item(self.visitas_button)
            self.add_item(self.compartidos_button)

        self.back_button = Button(label="Atrás", style=discord.ButtonStyle.secondary, custom_id="back_unique")
        self.cerrar_ticket_button = Button(label="Cerrar Ticket", style=discord.ButtonStyle.danger, custom_id="cerrar_ticket_service_unique")

        self.back_button.callback = self.back
        self.cerrar_ticket_button.callback = self.cerrar_ticket

        self.add_item(self.back_button)
        self.add_item(self.cerrar_ticket_button)

    async def select_service_quantity(self, interaction: discord.Interaction):
        if interaction.data['custom_id'].startswith("insta_seguidores"):
            quantities = [str(i * 1000) for i in range(1, 11)] + ["100000"]
            title = "Cantidad de Seguidores Instagram"
        elif interaction.data['custom_id'].startswith("insta_likes"):
            quantities = [str(i * 1000) for i in range(1, 11)] + ["100000"]
            title = "Cantidad de Likes Instagram"
        elif interaction.data['custom_id'].startswith("insta_visitas"):
            quantities = [str(i * 10000) for i in range(1, 11)] + ["500000"]
            title = "Cantidad de Visitas Instagram"
        elif interaction.data['custom_id'].startswith("tiktok_seguidores"):
            quantities = [str(i * 1000) for i in range(1, 11)] + ["1000000"]
            title = "Cantidad de Seguidores TikTok"
        elif interaction.data['custom_id'].startswith("tiktok_likes"):
            quantities = [str(i * 10000) for i in range(1, 11)] + ["1000000"]
            title = "Cantidad de Likes TikTok"
        elif interaction.data['custom_id'].startswith("tiktok_visitas"):
            quantities = [str(i * 100000) for i in range(1, 11)] + ["10000000"]
            title = "Cantidad de Visitas TikTok"
        elif interaction.data['custom_id'].startswith("tiktok_compartidos"):
            quantities = [str(i * 1000) for i in range(1, 11)] + ["100000"]
            title = "Cantidad de Compartidos TikTok"

        service_info = {
            "category": self.category,
            "service": title.split()[2],
            "title": title
        }

        quantity_view = QuantityView(service_info, quantities)
        await interaction.response.edit_message(content=f"Selecciona la cantidad para {title}:", view=quantity_view)

    async def back(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await interaction.message.edit(content="Selecciona la plataforma para seguidores:", view=PersistentPlatformSelectView())

    async def cerrar_ticket(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await interaction.channel.delete()

class QuantityView(View):
    def __init__(self, service_info, quantities):
        super().__init__(timeout=None)
        self.service_info = service_info
        for quantity in quantities:
            button = Button(label=quantity, style=discord.ButtonStyle.primary, custom_id=f"quantity_{quantity}")
            button.callback = self.quantity_selected
            self.add_item(button)
        
        self.back_button = Button(label="Atrás", style=discord.ButtonStyle.secondary, custom_id="back_to_services")
        self.cerrar_ticket_button = Button(label="Cerrar Ticket", style=discord.ButtonStyle.danger, custom_id="close_ticket_from_quantity")

        self.back_button.callback = self.back_to_services
        self.cerrar_ticket_button.callback = self.cerrar_ticket

        self.add_item(self.back_button)
        self.add_item(self.cerrar_ticket_button)

    async def quantity_selected(self, interaction: discord.Interaction):
        quantity = interaction.data['custom_id'].split('_')[1]
        self.service_info["quantity"] = quantity

        await interaction.response.send_message(
            f"Has seleccionado {quantity} {self.service_info['title']}. Por favor, envía el enlace para completar el pedido.",
            ephemeral=True
        )

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            mensaje = await bot.wait_for('message', check=check, timeout=120)
            self.service_info["link"] = mensaje.content
            await interaction.followup.send("Enlace recibido. Generando resumen de pedido...", ephemeral=True)

            embed = discord.Embed(
                title="Resumen del Pedido",
                description="A continuación se muestra la información que has proporcionado:",
                color=discord.Color.blue()
            )
            embed.add_field(name="Plataforma", value=self.service_info["category"], inline=False)
            embed.add_field(name="Servicio", value=self.service_info["service"], inline=False)
            embed.add_field(name="Cantidad", value=self.service_info["quantity"], inline=False)
            embed.add_field(name="Enlace", value=self.service_info["link"], inline=False)

            confirmation_view = ConfirmationView(self.service_info)
            await interaction.channel.purge(limit=100)  
            await interaction.channel.send(embed=embed, view=confirmation_view)

        except asyncio.TimeoutError:
            await interaction.followup.send("No se recibió ningún enlace. Inténtalo de nuevo más tarde.", ephemeral=True)

    async def back_to_services(self, interaction: discord.Interaction):
        category = self.service_info["category"]
        await interaction.response.defer()
        await interaction.message.edit(content="Buena elección, ahora elige el servicio:", view=SocialMediaView(category=category))

    async def cerrar_ticket(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await interaction.channel.delete()


price_list = {
    "TikTok": {
        "Seguidores": {
            1000: 0.7,
            2000: 1.4,
            3000: 2.1,
            4000: 2.8,
            5000: 3.5,
            6000: 4.2,
            7000: 4.9,
            8000: 5.6,
            9000: 6.3,
            10000: 7.0,
            100000: 70.0
        },
        "Likes": {
            10000: 1.50,
            20000: 3.0,
            30000: 4.50,
            40000: 6.0,
            50000: 7.50,
            60000: 9.0,
            70000: 10.5,
            80000: 12.0,
            90000: 13.5,
            100000: 15.0,
            1000000: 150.0
        },
        "Visitas": {
            100000: 0.25,
            200000: 0.50,
            300000: 0.75,
            400000: 1.0,
            500000: 1.25,
            600000: 1.50,
            700000: 1.75,
            800000: 2.0,
            900000: 2.25,
            1000000: 2.50,
            10000000: 100.0
        },
        "Compartidos": {
            1000: 0.50,
            2000: 1.00,
            3000: 1.50,
            4000: 2.00,
            5000: 2.50,
            6000: 3.00,
            7000: 3.50,
            8000: 4.00,
            9000: 4.50,
            10000: 5.00,
            100000: 20.00
        }
    },
    "Instagram": {
        "Seguidores": {
            1000: 1.2,
            2000: 2.4,
            3000: 3.6,
            4000: 4.8,
            5000: 6.0,
            6000: 7.2,
            7000: 8.4,
            8000: 9.6,
            9000: 10.8,
            10000: 12.0,
            50000: 50.0
        },
        "Likes": {
            1000: 0.15,
            2000: 0.30,
            3000: 0.45,
            4000: 0.60,
            5000: 0.75,
            6000: 0.90,
            7000: 1.05,
            8000: 1.20,
            9000: 1.35,
            10000: 1.50,
            100000: 15.0
        },
        "Visitas": {
            10000: 0.30,
            20000: 0.60,
            30000: 0.90,
            40000: 1.20,
            50000: 1.50,
            60000: 1.80,
            70000: 2.10,
            80000: 2.40,
            90000: 2.70,
            100000: 3.0,
            500000: 15.0
        }
    }
}

class ConfirmationView(View):
    def __init__(self, service_info):
        super().__init__(timeout=None)
        self.service_info = service_info
        self.confirm_button = Button(label="Sí, todo está correcto", style=discord.ButtonStyle.success, custom_id="confirm")
        self.retry_button = Button(label="No, empezar de nuevo", style=discord.ButtonStyle.danger, custom_id="retry")

        self.confirm_button.callback = self.confirm
        self.retry_button.callback = self.retry

        self.add_item(self.confirm_button)
        self.add_item(self.retry_button)

    async def confirm(self, interaction: discord.Interaction):
        await interaction.channel.purge(limit=100)  

        base_prices = price_list[self.service_info["category"]][self.service_info["service"]]
        total_price = base_prices[int(self.service_info["quantity"])]

        embed_payment = discord.Embed(
            title="Instrucciones de Pago",
            description=( 
                f"- Por favor, envía el dinero a: https://www.paypal.me/SoyKayy como amigos y familiares.\n"
                f"- Importe a pagar: {total_price:.2f}€\n"
                "- Recuerda que no hacemos reembolso pase lo que pase.\n"
                "- La cuenta debe de ser pública.\n"
                "- Hay un 0% de posibilidades de baneo.\n"
                "- Suele caer entre un 2%-4% por seguridad.\n"
                "- Si tienes algún problema envía un mensaje a <@1238471224510648412>"
            ),
            color=discord.Color.green()
        )

        if self.service_info["category"] == "Instagram" and self.service_info["service"] == "Seguidores":
            embed_warning = discord.Embed(
                title="Importante",
                description=(
                f"- Por favor, asegúrate de que la opción **'Marcar Para Revisión'** está desactivada antes de continuar.\n"
                "- Haz clic en el botón de abajo cuando estés listo para continuar con el pago."
            ),
                color=discord.Color.red()
            )
            embed_warning.set_image(url="https://raw.githubusercontent.com/Kayy9961/Data-Base-Personal/main/IMG_5466%20copia.png")

            await interaction.channel.send(embed=embed_warning)

        await interaction.channel.send(embed=embed_payment)

        await send_followers_image(interaction.channel) 

        payment_confirmation_view = PaymentConfirmationView(self.service_info, interaction.channel)
        await interaction.channel.send(
            "Una vez hayas hecho el pago, apreta el botón:",
            view=payment_confirmation_view
        )

    async def retry(self, interaction: discord.Interaction):
        await interaction.channel.purge(limit=100) 
        await send_followers_image(interaction.channel) 
        await interaction.channel.send("Vamos a empezar de nuevo. Selecciona la plataforma para seguidores:", view=PersistentPlatformSelectView())

async def cerrar_ticket(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await interaction.channel.delete()

async def send_followers_image(channel):
    """Helper function to send the followers image in an embed."""
    embed_image = discord.Embed(title="Precios", color=discord.Color.blue())
    embed_image.set_image(url=FOLLOWERS_IMAGE_URL)
    await channel.send(embed=embed_image)

class PaymentConfirmationView(View):
    def __init__(self, service_info, ticket_channel):
        super().__init__(timeout=None)
        self.service_info = service_info
        self.ticket_channel = ticket_channel
        self.payment_done_button = Button(label="Pago hecho correctamente", style=discord.ButtonStyle.success, custom_id="payment_done")
        self.payment_done_button.callback = self.payment_done
        self.add_item(self.payment_done_button)

    async def payment_done(self, interaction: discord.Interaction):
        await interaction.channel.purge(limit=100)  
        embed_thanks = discord.Embed(
            title="¡Gracias por tu pago!",
            description="Un administrador lo revisará pronto.",
            color=discord.Color.blue()
        )
        await interaction.channel.send(embed=embed_thanks)

        embed_order = discord.Embed(
            title="Pago Confirmado",
            description="Un usuario ha confirmado el pago para el siguiente pedido:",
            color=discord.Color.blue()
        )
        embed_order.add_field(name="Usuario", value=interaction.user.mention, inline=False)
        embed_order.add_field(name="Plataforma", value=self.service_info["category"], inline=False)
        embed_order.add_field(name="Servicio", value=self.service_info["service"], inline=False)
        embed_order.add_field(name="Cantidad", value=self.service_info["quantity"], inline=False)
        embed_order.add_field(name="Enlace", value=self.service_info["link"], inline=False)

        canal_informacion = bot.get_channel(informacion_canal_id)
        if canal_informacion is not None:
            confirmation_buttons = PaymentActionView(self.service_info, interaction.user, self.ticket_channel)
            message = await canal_informacion.send(embed=embed_order, view=confirmation_buttons)
            confirmation_buttons.message = message  
        else:
            await interaction.response.send_message("Error: No se pudo encontrar el canal de información para enviar el resumen del pedido.", ephemeral=True)

class PaymentActionView(View):
    def __init__(self, service_info, user, ticket_channel):
        super().__init__(timeout=None)
        self.service_info = service_info
        self.user = user
        self.ticket_channel = ticket_channel
        self.message = None  

        self.approve_button = Button(label="Confirmar Pago", style=discord.ButtonStyle.success, custom_id="approve_payment")
        self.reject_button = Button(label="Rechazar Pago", style=discord.ButtonStyle.danger, custom_id="reject_payment")

        self.approve_button.callback = self.approve_payment
        self.reject_button.callback = self.reject_payment

        self.add_item(self.approve_button)
        self.add_item(self.reject_button)

    async def approve_payment(self, interaction: discord.Interaction):
        if interaction.user.id != ALLOWED_USER_ID:
            await interaction.response.send_message("No tienes permiso para realizar esta acción.", ephemeral=True)
            return

        service_ids = {
            "Instagram": {
                "Seguidores": 9043,
                "Likes": 6770,
                "Visitas": 5463
            },
            "TikTok": {
                "Seguidores": 5809,
                "Likes": 5779,
                "Visitas": 1184,
                "Compartidos": 5783
            }
        }

        service_id = service_ids.get(self.service_info["category"], {}).get(self.service_info["service"])
        if service_id is None:
            await interaction.response.send_message("Servicio no válido.", ephemeral=True)
            return

        use_alternate_api = (self.service_info["category"] == "TikTok" or
                             (self.service_info["category"] == "Instagram" and self.service_info["service"] != "Likes"))
        resultado = realizar_pedido(
            url=self.service_info["link"],
            seguidores=int(self.service_info["quantity"]),
            service_id=service_id,
            category=self.service_info["category"],
            service_name=self.service_info["service"],
            use_alternate_api=use_alternate_api
        )

        if resultado == "success":
            embed_success = discord.Embed(
                title="Pedido Realizado Exitosamente",
                description=f"El pedido ha sido procesado para {self.user.mention}.",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed_success, ephemeral=True)

            embed_accepted = discord.Embed(
                title="¡Solicitud Aceptada!",
                description="Tu pedido ha sido aceptado y procesado. Aquí están los detalles:",
                color=discord.Color.green()
            )
            embed_accepted.add_field(name="Plataforma", value=self.service_info["category"], inline=False)
            embed_accepted.add_field(name="Servicio", value=self.service_info["service"], inline=False)
            embed_accepted.add_field(name="Cantidad", value=self.service_info["quantity"], inline=False)
            embed_accepted.add_field(name="Enlace", value=self.service_info["link"], inline=False)
            
            buy_again_view = BuyAgainView(self.ticket_channel)
            await self.ticket_channel.send(embed=embed_accepted, view=buy_again_view)
            await self.ticket_channel.send(f"{self.user.mention}, una vez que se haya entregado tu pedido, por favor deja tu reseña en <#1263936105213067437>.")

            if self.message:
                await self.message.delete()

        else:
            await interaction.response.send_message(f"Error al realizar el pedido: {resultado}", ephemeral=True)

    async def reject_payment(self, interaction: discord.Interaction):
        if interaction.user.id != ALLOWED_USER_ID:
            await interaction.response.send_message("No tienes permiso para realizar esta acción.", ephemeral=True)
            return

        await interaction.response.send_message(f"Pago rechazado para {self.user.mention}.", ephemeral=True)

        embed_rejected = discord.Embed(
            title="¡Solicitud Rechazada!",
            description="Asegúrate de enviar el pago correctamente.",
            color=discord.Color.red()
        )
        
        buy_again_view = BuyAgainView(self.ticket_channel)
        await self.ticket_channel.send(embed=embed_rejected, view=buy_again_view)

        if self.message:
            await self.message.delete()

class BuyAgainView(View):
    def __init__(self, ticket_channel):
        super().__init__(timeout=None)
        self.ticket_channel = ticket_channel
        self.buy_again_button = Button(label="Comprar de nuevo", style=discord.ButtonStyle.primary, custom_id="buy_again")
        self.close_ticket_button = Button(label="Cerrar Ticket", style=discord.ButtonStyle.danger, custom_id="close_ticket")

        self.buy_again_button.callback = self.buy_again
        self.close_ticket_button.callback = self.close_ticket

        self.add_item(self.buy_again_button)
        self.add_item(self.close_ticket_button)

    async def buy_again(self, interaction: discord.Interaction):
        await interaction.response.defer() 
        await self.ticket_channel.purge(limit=100) 
        await send_followers_image(self.ticket_channel) 
        await self.ticket_channel.send("Vamos a empezar de nuevo. Selecciona la plataforma para seguidores:", view=PersistentPlatformSelectView())

    async def close_ticket(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await self.ticket_channel.delete()

class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())

class TicketSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="💰 Comprar Cuenta", value="buy_account"),
            discord.SelectOption(label="👤 Comprar Seguidores", value="buy_followers"),
            discord.SelectOption(label="💸 Discord Nitro Barato", value="buy_nitro"),
            discord.SelectOption(label="❓ Otra cosa", value="other")
        ]
        super().__init__(placeholder='Selecciona una opción', min_values=1, max_values=1, options=options, custom_id="ticket_select")

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        member = interaction.user
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=True)
        }
        ticket_channel = await guild.create_text_channel(f"ticket-{member.name}", overwrites=overwrites)

        embed_ticket = discord.Embed(
            title="Kayy Shop",
            description=f"Holaa {member.mention}, este es tu ticket.",
            color=discord.Color.green()
        )
        await ticket_channel.send(embed=embed_ticket) 

        if self.values[0] == "buy_followers":
            await send_followers_image(ticket_channel)  
            await ticket_channel.send("Selecciona la plataforma para seguidores:", view=PersistentPlatformSelectView())
        else:
            close_ticket_button = Button(label="Cerrar Ticket", style=discord.ButtonStyle.danger, custom_id="cerrar_ticket_general")
            close_ticket_view = View(timeout=None)
            close_ticket_view.add_item(close_ticket_button)

            async def close_ticket(interaction: discord.Interaction):
                await interaction.response.defer()
                await ticket_channel.delete()

            close_ticket_button.callback = close_ticket
            await ticket_channel.send("Un moderador atenderá su ticket lo más rapido posible")
            await ticket_channel.send("Usa este botón para cerrar el ticket cuando hayas terminado o necesites ayuda.", view=close_ticket_view)

        await interaction.response.send_message(f"Ticket creado: {ticket_channel.mention}", ephemeral=True)

        

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    canal = bot.get_channel(canal_id)
    if canal is None:
        print("Canal no encontrado. Asegúrate de que el ID es correcto.")
        return

    embed_intro = discord.Embed(
        title="Kayy Shop | Tickets",
        description="Abre ticket si deseas comprar una cuenta o tienes cualquier duda.",
        color=discord.Color.green()
    )
    embed_intro.set_footer(text="Ticket Tool Created By Kayy")

    view = TicketView()
    bot.add_view(view)  

    await canal.send(embed=embed_intro, view=view)
    print(f"Botón de creación de ticket enviado al canal: {canal.name}")


bot.run('EL TOKEN DE TU BOT DE DISCORD')
