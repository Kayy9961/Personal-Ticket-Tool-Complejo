import discord
from discord.ext import commands
from discord.ui import Button, View, Select
import asyncio
import requests

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True  

#CAMBIA TODO SEGÚN LO NECESITES, ID DE CANALES, DE PERFIL, FOTOS, PRECIOS, ETC

bot = commands.Bot(command_prefix='!', intents=intents)

canal_id = 1303931390114398228
informacion_canal_id = 1296755935418781717
ALLOWED_USER_ID = 399876603229896704  
PREMIUM_ROLE_ID = 1296736560359804969  

FOLLOWERS_IMAGE_URL = "https://raw.githubusercontent.com/Kayy9961/Data-Base-Personal/refs/heads/main/V4.png"
PREMIUM_FOLLOWERS_IMAGE_URL = "https://raw.githubusercontent.com/Kayy9961/Data-Base-Personal/refs/heads/main/V4Premiun.png"
LIVE_VIEWERS_IMAGE_URL = "https://raw.githubusercontent.com/Kayy9961/Data-Base-Personal/refs/heads/main/Lives.png"
EXCHANGE_IMAGE_URL = "https://raw.githubusercontent.com/Kayy9961/Data-Base-Personal/refs/heads/main/exchange.png"
BITS_IMAGE_URL = "https://raw.githubusercontent.com/Kayy9961/Data-Base-Personal/refs/heads/main/bitsfix.png"

bits_price_mapping = {
    "5000": 12.50,
    "6000": 15.00,
    "7000": 17.50,
    "8000": 20.00,
    "9000": 22.50,
    "10000": 25.00,
    "20000": 50.00,
    "30000": 75.00,
    "40000": 100.00,
    "50000": 125.00
}
bits_to_price = bits_price_mapping
price_to_bits = {v: k for k, v in bits_price_mapping.items()}


def realizar_pedido(url, seguidores, service_id, category, service_name, use_alternate_api=False):
    if category == "Instagram" and service_name == "Seguidores" and service_id == 6362:
        api_endpoint = "LA API DE TU PANE"
        api_key = "LA API KEY DE TU PANEL"
    elif use_alternate_api or (category == "TikTok" or (category == "Instagram" and service_name != "Likes")):
        api_endpoint = "LA API DE TU PANE"
        api_key = "LA API KEY DE TU PANEL"
    else:
        api_endpoint = "LA API DE TU PANEL"
        api_key = "LA API KEY DE TU PANEL"

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

async def cerrar_ticket(interaction: discord.Interaction):
    await interaction.response.defer()
    await interaction.channel.delete()

async def send_followers_image(channel, user):
    embed_image = discord.Embed(title="Precios", color=discord.Color.blue())
    if any(role.id == PREMIUM_ROLE_ID for role in user.roles):
        embed_image.set_image(url=PREMIUM_FOLLOWERS_IMAGE_URL)
    else:
        embed_image.set_image(url=FOLLOWERS_IMAGE_URL)
    await channel.send(embed=embed_image)

async def send_exchange_image(channel):
    embed_image = discord.Embed(title="Exchange", color=discord.Color.blue())
    embed_image.set_image(url="https://raw.githubusercontent.com/Kayy9961/Data-Base-Personal/refs/heads/main/ExchangeV3.png")
    await channel.send(embed=embed_image)

async def send_live_viewers_image(channel):
    embed_image = discord.Embed(title="Precios de Espectadores en Directo", color=discord.Color.blue())
    embed_image.set_image(url=LIVE_VIEWERS_IMAGE_URL)
    await channel.send(embed=embed_image)

async def send_buy_bits_image(channel):
    embed_image = discord.Embed(title="Comprar Bits", color=discord.Color.blue())
    embed_image.set_image(url=BITS_IMAGE_URL)
    await channel.send(embed=embed_image)


price_list = {
    "TikTok": {
        "Seguidores": {
            1000: 0.6,
            2000: 1.2,
            3000: 1.8,
            4000: 2.4,
            5000: 3.0,
            6000: 3.6,
            7000: 4.2,
            8000: 4.8,
            9000: 5.4,
            10000: 6.0,
            100000: 60.0
        },
        "Likes": {
            10000: 2.00,
            20000: 4.0,
            30000: 6.0,
            40000: 8.0,
            50000: 10.00,
            60000: 12.0,
            70000: 14.0,
            80000: 16.0,
            90000: 18.0,
            100000: 20.0,
            1000000: 200.0
        },
        "Visitas": {
            100000: 0.5,
            200000: 1,
            300000: 1.5,
            400000: 2,
            500000: 2.5,
            600000: 3,
            700000: 3.5,
            800000: 4.0,
            900000: 4.5,
            1000000: 5,
            10000000: 50.0
        }
    },
    "Instagram": {
        "Seguidores": {
            1000: 2.0,
            2000: 4.0,
            3000: 6.0,
            4000: 8.0,
            5000: 10.0,
            6000: 12.0,
            7000: 14.0,
            8000: 16.0,
            9000: 18.0,
            10000: 20.0,
            100000: 200.0
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

premium_price_list = {
    "TikTok": {
        "Seguidores": {
            1000: 0.5,
            2000: 1.0,
            3000: 1.5,
            4000: 2.0,
            5000: 2.5,
            6000: 3.0,
            7000: 3.5,
            8000: 4.0,
            9000: 4.5,
            10000: 5.0,
            100000: 50.0
        },
        "Likes": {
            10000: 1.7,
            20000: 3.4,
            30000: 5.1,
            40000: 6.8,
            50000: 8.5,
            60000: 10.2,
            70000: 11.9,
            80000: 13.6,
            90000: 15.3,
            100000: 17.0,
            1000000: 170.0
        },
        "Visitas": {
            100000: 0.43,
            200000: 0.85,
            300000: 1.28,
            400000: 1.7,
            500000: 2.13,
            600000: 2.55,
            700000: 2.98,
            800000: 3.4,
            900000: 3.83,
            1000000: 4.25,
            10000000: 42.5
        }
    },
    "Instagram": {
        "Seguidores": {
            1000: 1.7,
            2000: 3.4,
            3000: 5.1,
            4000: 6.8,
            5000: 8.5,
            6000: 10.2,
            7000: 11.9,
            8000: 13.6,
            9000: 15.3,
            10000: 17.0,
            100000: 170.0
        },
        "Likes": {
            1000: 0.13,
            2000: 0.26,
            3000: 0.38,
            4000: 0.51,
            5000: 0.64,
            6000: 0.77,
            7000: 0.89,
            8000: 1.02,
            9000: 1.15,
            10000: 1.28,
            100000: 12.75
        },
        "Visitas": {
            10000: 0.26,
            20000: 0.51,
            30000: 0.77,
            40000: 1.02,
            50000: 1.28,
            60000: 1.53,
            70000: 1.79,
            80000: 2.04,
            90000: 2.3,
            100000: 2.55,
            500000: 12.75
        }
    }
}

live_viewers_price_list = {
    "15m": {100: 0.10, 500: 0.50, 1000: 1.00},
    "30m": {100: 0.20, 500: 1.00, 1000: 2.00},
    "60m": {100: 0.40, 500: 2.00, 1000: 4.00},
    "90m": {100: 0.60, 500: 3.00, 1000: 6.00},
    "120m": {100: 0.80, 500: 4.00, 1000: 8.00},
    "180m": {100: 1.20, 500: 6.00, 1000: 12.00},
    "240m": {100: 1.60, 500: 8.00, 1000: 16.00},
    "300m": {100: 2.00, 500: 10.00, 1000: 20.00},
    "360m": {100: 2.40, 500: 12.00, 1000: 24.00},
    "24h": {100: 8.99, 500: 34.99, 1000: 45.00}
}

live_service_ids = {
    "15m": 3548,
    "30m": 3549,
    "60m": 3550,
    "90m": 3551,
    "120m": 3552,
    "180m": 3553,
    "240m": 3554,
    "300m": 4029,
    "360m": 4030,
    "24h": 5936
}

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
        await interaction.response.defer()
        await interaction.message.edit(content="Buena elección, ahora elige el servicio:", view=SocialMediaView(category="Instagram"))

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
        service = None
        title = ""
        if interaction.data['custom_id'].startswith("insta_seguidores"):
            service = "Seguidores"
            title = "Cantidad de Seguidores Instagram"
        elif interaction.data['custom_id'].startswith("insta_likes"):
            service = "Likes"
            title = "Cantidad de Likes Instagram"
        elif interaction.data['custom_id'].startswith("insta_visitas"):
            service = "Visitas"
            title = "Cantidad de Visitas Instagram"
        elif interaction.data['custom_id'].startswith("tiktok_seguidores"):
            service = "Seguidores"
            title = "Cantidad de Seguidores TikTok"
        elif interaction.data['custom_id'].startswith("tiktok_likes"):
            service = "Likes"
            title = "Cantidad de Likes TikTok"
        elif interaction.data['custom_id'].startswith("tiktok_visitas"):
            service = "Visitas"
            title = "Cantidad de Visitas TikTok"
        elif interaction.data['custom_id'].startswith("tiktok_compartidos"):
            service = "Compartidos"
            title = "Cantidad de Compartidos TikTok"

        if any(role.id == PREMIUM_ROLE_ID for role in interaction.user.roles):
            prices = premium_price_list
        else:
            prices = price_list

        service_info = {
            "category": self.category,
            "service": service,
            "title": title
        }

        quantities = [str(q) for q in sorted(prices[self.category][service].keys())]
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
            f"Has seleccionado {quantity} {self.service_info['title']}. Por favor, envía el enlace de tu perfil/video para completar el pedido",
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

        if any(role.id == PREMIUM_ROLE_ID for role in interaction.user.roles):
            base_prices = premium_price_list[self.service_info["category"]][self.service_info["service"]]
        else:
            base_prices = price_list[self.service_info["category"]][self.service_info["service"]]

        total_price = base_prices[int(self.service_info["quantity"])]

        embed_payment = discord.Embed(
            title="Instrucciones de Pago",
            description=(
                f"- Por favor, envía el dinero a: https://www.paypal.me/KayyShop **como amigos y familiares**.\n"
                f"- Importe a pagar: {total_price:.2f}€\n"
                "- Recuerda que no hacemos reembolso pase lo que pase.\n"
                "- La cuenta debe de ser pública.\n"
                "- Hay un 0% de posibilidades de baneo.\n"
                "- Suele caer entre un 0%-4% por seguridad.\n"
                "- Si tienes algún problema envía un mensaje a <@1291162796796411969>.\n"
                "- Cualquier tipo de problemas con los pagos o cuentas baneadas, no somos responsables y eres responsable de ello."
            ),
            color=discord.Color.green()
        )

        if self.service_info["category"] == "Instagram" and self.service_info["service"] == "Seguidores":
            embed_warning = discord.Embed(
                title="Importante",
                description=(
                    "- Por favor, asegúrate de que la opción **'Marcar Para Revisión'** está desactivada antes de continuar.\n"
                    "- Haz clic en el botón de abajo cuando estés listo para continuar con el pago."
                ),
                color=discord.Color.red()
            )
            embed_warning.set_image(url="https://raw.githubusercontent.com/Kayy9961/Data-Base-Personal/main/IMG_5466%20copia.png")
            await interaction.channel.send(embed=embed_warning)

        elif self.service_info["category"] == "TikTok" and self.service_info["service"] == "Seguidores":
            embed_warning_tiktok = discord.Embed(
                title="Importante",
                description=(
                    "- Antes del pedido **DEBE ABRIR DIRECTO DE LA CUENTA HASTA QUE SE COMPLETE EL PEDIDO**.\n"
                    "- DE LO CONTRARIO, EL PEDIDO NO SE COMPLETARÁ.\n"
                    "- **NO SE OFRECE NINGÚN REEMBOLSO SI NO SE SIGUE LA ADVERTENCIA**."
                ),
                color=discord.Color.red()
            )
            embed_warning_tiktok.set_image(url="https://www.socialchamp.com/wp-content/uploads/2023/07/how-do-you-go-live-on-tiktok.jpg")
            await interaction.channel.send(embed=embed_warning_tiktok)

        await interaction.channel.send(embed=embed_payment)

        payment_confirmation_view = PaymentConfirmationView(self.service_info)
        await interaction.channel.send(
            "Una vez hayas hecho el pago, presiona el botón:",
            view=payment_confirmation_view
        )

    async def retry(self, interaction: discord.Interaction):
        await interaction.channel.purge(limit=100)
        await send_followers_image(interaction.channel, interaction.user)
        await interaction.channel.send(
            "Vamos a empezar de nuevo. Selecciona la plataforma para seguidores:",
            view=PersistentPlatformSelectView()
        )


class PaymentConfirmationView(View):
    def __init__(self, service_info):
        super().__init__(timeout=None)
        self.service_info = service_info
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
            confirmation_buttons = PaymentActionView(self.service_info, interaction.user, interaction.channel)
            message = await canal_informacion.send(embed=embed_order, view=confirmation_buttons)
            confirmation_buttons.message = message
        else:
            await interaction.response.send_message(
                "Error: No se pudo encontrar el canal de información para enviar el resumen del pedido.",
                ephemeral=True
            )


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
        if self.service_info["category"] == "TikTok Live":
            service_id = self.service_info["service_id"]
            quantity = self.service_info["quantity"]
            use_alternate_api = True
        else:
            service_ids = {
                "Instagram": {
                    "Seguidores": 6362,
                    "Likes": 8035,
                    "Visitas": 5463
                },
                "TikTok": {
                    "Seguidores": 6389,
                    "Likes": 542,
                    "Visitas": 1563,
                    "Compartidos": 5783
                }
            }
            service_id = service_ids.get(self.service_info["category"], {}).get(self.service_info["service"])
            if service_id is None:
                await interaction.response.send_message("Servicio no válido.", ephemeral=True)
                return

            use_alternate_api = (
                self.service_info["category"] == "TikTok"
                or (self.service_info["category"] == "Instagram" and self.service_info["service"] != "Likes")
            )
            quantity = int(self.service_info["quantity"])
        resultado = realizar_pedido(
            url=self.service_info["link"],
            seguidores=quantity,
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
            await self.ticket_channel.send(
                f"{self.user.mention}, una vez que se haya entregado tu pedido, "
                f"por favor deja tu reseña en <#1296608195124396072>."
            )

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
        await send_followers_image(self.ticket_channel, interaction.user)
        await self.ticket_channel.send("Vamos a empezar de nuevo. Selecciona la plataforma para seguidores:", view=PersistentPlatformSelectView())

    async def close_ticket(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await self.ticket_channel.delete()

class LiveDurationView(View):
    def __init__(self):
        super().__init__(timeout=None)
        durations = [
            ("15 Minutos", "15m"),
            ("30 Minutos", "30m"),
            ("60 Minutos", "60m"),
            ("90 Minutos", "90m"),
            ("120 Minutos", "120m"),
            ("180 Minutos", "180m"),
            ("240 Minutos", "240m"),
            ("300 Minutos", "300m"),
            ("360 Minutos", "360m"),
            ("24 Horas", "24h")
        ]
        for label, duration_key in durations:
            button = Button(label=label, style=discord.ButtonStyle.primary, custom_id=f"duration_{duration_key}")
            button.callback = self.duration_selected
            self.add_item(button)

        self.close_ticket_button = Button(label="Cerrar Ticket", style=discord.ButtonStyle.danger, custom_id="close_ticket_from_duration")
        self.close_ticket_button.callback = self.cerrar_ticket
        self.add_item(self.close_ticket_button)

    async def duration_selected(self, interaction: discord.Interaction):
        duration_key = interaction.data['custom_id'].split('_')[1]
        await interaction.response.edit_message(content="Selecciona el número de espectadores:", view=LiveViewersView(duration_key))

    async def cerrar_ticket(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await interaction.channel.delete()


class LiveViewersView(View):
    def __init__(self, duration_key):
        super().__init__(timeout=None)
        self.duration_key = duration_key

        viewers_options = [
            ("100 Espectadores", "100", 100),
            ("500 Espectadores", "500", 500),
            ("1000 Espectadores", "1000", 1000)
        ]
        for label, viewers_key, quantity in viewers_options:
            button = Button(label=label, style=discord.ButtonStyle.primary, custom_id=f"viewers_{viewers_key}")
            button.callback = self.viewers_selected
            button.quantity = quantity
            self.add_item(button)

        self.back_button = Button(label="Atrás", style=discord.ButtonStyle.secondary, custom_id="back_to_duration")
        self.back_button.callback = self.back_to_duration
        self.add_item(self.back_button)

        self.close_ticket_button = Button(label="Cerrar Ticket", style=discord.ButtonStyle.danger, custom_id="close_ticket_from_viewers")
        self.close_ticket_button.callback = self.cerrar_ticket
        self.add_item(self.close_ticket_button)

    async def viewers_selected(self, interaction: discord.Interaction):
        quantity_key = interaction.data['custom_id'].split('_')[1]
        quantity = int(quantity_key)
        price = live_viewers_price_list[self.duration_key][quantity]
        service_id = live_service_ids[self.duration_key]
        service_info = {
            "category": "TikTok Live",
            "service": f"Espectadores en Directo ({self.duration_key})",
            "quantity": quantity,
            "service_id": service_id,
            "price": price
        }
        await interaction.response.send_message(
            f"Has seleccionado {quantity} espectadores por {self.duration_key}. Por favor, envía el enlace del stream para completar el pedido.",
            ephemeral=True
        )

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            mensaje = await bot.wait_for('message', check=check, timeout=120)
            service_info["link"] = mensaje.content
            await interaction.followup.send("Enlace recibido. Generando resumen de pedido...", ephemeral=True)

            embed = discord.Embed(
                title="Resumen del Pedido",
                description="A continuación se muestra la información que has proporcionado:",
                color=discord.Color.blue()
            )
            embed.add_field(name="Plataforma", value=service_info["category"], inline=False)
            embed.add_field(name="Servicio", value=service_info["service"], inline=False)
            embed.add_field(name="Cantidad", value=service_info["quantity"], inline=False)
            embed.add_field(name="Enlace", value=service_info["link"], inline=False)
            embed.add_field(name="Precio", value=f"{service_info['price']:.2f}€", inline=False)

            confirmation_view = LiveConfirmationView(service_info)
            await interaction.channel.purge(limit=100)
            await interaction.channel.send(embed=embed, view=confirmation_view)

        except asyncio.TimeoutError:
            await interaction.followup.send("No se recibió ningún enlace. Inténtalo de nuevo más tarde.", ephemeral=True)

    async def back_to_duration(self, interaction: discord.Interaction):
        await interaction.response.edit_message(content="Selecciona la duración del stream:", view=LiveDurationView())

    async def cerrar_ticket(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await interaction.channel.delete()


class LiveConfirmationView(View):
    def __init__(self, service_info):
        super().__init__(timeout=None)
        self.service_info = service_info

        self.confirm_button = Button(label="Sí, todo está correcto", style=discord.ButtonStyle.success, custom_id="confirm_live")
        self.retry_button = Button(label="No, empezar de nuevo", style=discord.ButtonStyle.danger, custom_id="retry_live")

        self.confirm_button.callback = self.confirm
        self.retry_button.callback = self.retry

        self.add_item(self.confirm_button)
        self.add_item(self.retry_button)

    async def confirm(self, interaction: discord.Interaction):
        await interaction.channel.purge(limit=100)
        total_price = self.service_info['price']

        embed_payment = discord.Embed(
            title="Instrucciones de Pago",
            description=(
                f"- Por favor, envía el dinero a: [PayPal](https://www.paypal.me/KayyShop) **como amigos y familiares**.\n"
                f"- Importe a pagar: {total_price:.2f}€\n"
                "- Recuerda que no hacemos reembolso pase lo que pase.\n"
                "- La cuenta debe de ser pública.\n"
                "- Si tienes algún problema, contacta a <@1291162796796411969>.\n"
                "- Cualquier tipo de problemas con los pagos o cuentas baneadas, no somos responsables y eres responsable de ello."
            ),
            color=discord.Color.green()
        )
        await interaction.channel.send(embed=embed_payment)

        payment_confirmation_view = PaymentConfirmationView(self.service_info)
        await interaction.channel.send(
            "Una vez hayas hecho el pago, presiona el botón:",
            view=payment_confirmation_view
        )

    async def retry(self, interaction: discord.Interaction):
        await interaction.channel.purge(limit=100)
        await send_live_viewers_image(interaction.channel)
        await interaction.channel.send("Vamos a empezar de nuevo. Selecciona la duración del stream:", view=LiveDurationView())


class BuyBitsView(View):
    def __init__(self):
        super().__init__(timeout=None)
        bits_options = ["5000", "6000", "7000", "8000", "9000", "10000", "20000", "30000", "40000", "50000"]
        for bits in bits_options:
            button = Button(label=bits, style=discord.ButtonStyle.primary, custom_id=f"bits_{bits}")
            button.callback = self.bits_selected
            self.add_item(button)

        self.cerrar_ticket_button = Button(label="Cerrar Ticket", style=discord.ButtonStyle.danger, custom_id="cerrar_ticket_bits")
        self.cerrar_ticket_button.callback = self.cerrar_ticket
        self.add_item(self.cerrar_ticket_button)

    async def bits_selected(self, interaction: discord.Interaction):
        bits = interaction.data['custom_id'].split('_')[1]
        price = bits_price_mapping.get(bits)
        if not price:
            await interaction.response.send_message("Cantidad de bits no válida.", ephemeral=True)
            return

        self.bits = bits
        self.price = price

        await interaction.response.send_message(
            "Has seleccionado {} bits. Por favor, envía el enlace de tu canal de Twitch para completar el pedido.".format(bits),
            ephemeral=True
        )

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            mensaje = await bot.wait_for('message', check=check, timeout=120)
            twitch_link = mensaje.content

            embed_payment = discord.Embed(
                title="Instrucciones de Pago",
                description=(
                    f"- Por favor, envía el dinero a: [PayPal](https://www.paypal.me/KayyShop) **como amigos y familiares** o "
                    f"a la dirección de Litecoin **LdJG7Cq8eAVe5uFVuoo8uWsS6ES6jyq5Qw**.\n"
                    f"- Importe a pagar: {price:.2f}€\n"
                    "- Recuerda que no hacemos reembolso pase lo que pase.\n"
                    "- La cuenta debe de ser pública.\n"
                    "- Si tienes algún problema, contacta a <@1291162796796411969>.\n"
                    "- Cualquier tipo de problemas con los pagos o cuentas baneadas, no somos responsables y eres responsable de ello."
                ),
                color=discord.Color.green()
            )
            embed_payment.set_footer(text="Por favor, una vez hayas enviado el pago, pulsa el botón de abajo para confirmar.")

            await interaction.followup.send(embed=embed_payment, ephemeral=True)

            confirmation_view = BuyBitsConfirmationView(bits, price, twitch_link)
            await interaction.channel.send(
                "Una vez hayas hecho el pago, presiona el botón de abajo:",
                view=confirmation_view
            )

        except asyncio.TimeoutError:
            await interaction.followup.send("No se recibió ningún enlace. Inténtalo de nuevo más tarde.", ephemeral=True)

    async def cerrar_ticket(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await interaction.channel.delete()


class BuyBitsConfirmationView(View):
    def __init__(self, bits, price, twitch_link):
        super().__init__(timeout=None)
        self.bits = bits
        self.price = price
        self.twitch_link = twitch_link

        self.confirm_button = Button(label="Confirmar Pago", style=discord.ButtonStyle.success, custom_id="confirm_pay_bits")
        self.confirm_button.callback = self.confirm_payment
        self.add_item(self.confirm_button)

    async def confirm_payment(self, interaction: discord.Interaction):
        await interaction.response.defer()
        admin_id = 399876603229896704
        mention_admin = f"<@{admin_id}> " * 3
        await interaction.channel.send(
            f"{mention_admin}\nUn administrador atenderá tu pedido en breve."
        )

class ExchangeReceiveView(View):
    def __init__(self, channel, user, exchange_info: dict):
        super().__init__(timeout=None)
        self.channel = channel
        self.user = user
        self.exchange_info = exchange_info

        methods = [("LTC", "exchange_receive_ltc"),
                   ("PayPal", "exchange_receive_paypal"),
                   ("Bizum", "exchange_receive_bizum")]

        for label, custom_id in methods:
            btn = Button(label=label, style=discord.ButtonStyle.primary, custom_id=custom_id)
            btn.callback = self.select_receive
            self.add_item(btn)

    async def select_receive(self, interaction: discord.Interaction):
        chosen = interaction.data["custom_id"]
        if chosen == "exchange_receive_ltc":
            self.exchange_info["receive"] = "LTC"
        elif chosen == "exchange_receive_paypal":
            self.exchange_info["receive"] = "PayPal"
        elif chosen == "exchange_receive_bizum":
            self.exchange_info["receive"] = "Bizum"

        await interaction.response.edit_message(
            content="Ahora, ¿por dónde vas a pagar?",
            view=ExchangePayView(self.channel, self.user, self.exchange_info)
        )

    async def go_back(self, interaction: discord.Interaction):
        await interaction.response.edit_message(
            content="Volviendo al menú de ticket...",
            view=TicketView()
        )


class ExchangePayView(View):
    def __init__(self, channel, user, exchange_info: dict):
        super().__init__(timeout=None)
        self.channel = channel
        self.user = user
        self.exchange_info = exchange_info

        self.prompt_msg = None
        self.user_input_msg = None

        possible_pays = [
            ("LTC", "exchange_pay_ltc"),
            ("PayPal", "exchange_pay_paypal"),
            ("Paysafecard", "exchange_pay_paysafecard"),
            ("Bizum", "exchange_pay_bizum")
        ]
        receive_method = self.exchange_info.get("receive")

        for label, custom_id in possible_pays:
            if label == receive_method:
                continue
            btn = Button(label=label, style=discord.ButtonStyle.primary, custom_id=custom_id)
            btn.callback = self.select_pay
            self.add_item(btn)

        self.back_button = Button(label="Atrás", style=discord.ButtonStyle.secondary, custom_id="exchange_pay_back")
        self.back_button.callback = self.go_back
        self.add_item(self.back_button)

    async def cleanup(self):
        if self.prompt_msg:
            try:
                await self.prompt_msg.delete()
            except:
                pass
            self.prompt_msg = None

        if self.user_input_msg:
            try:
                await self.user_input_msg.delete()
            except:
                pass
            self.user_input_msg = None

    async def select_pay(self, interaction: discord.Interaction):
        cid = interaction.data["custom_id"]

        if cid == "exchange_pay_ltc":
            self.exchange_info["pay"] = "LTC"
            prompt_text = "Por favor, escribe la **wallet** LTC a la que quieres que te envíen el dinero."
            info_key = "user_ltc_wallet"
        elif cid == "exchange_pay_paypal":
            self.exchange_info["pay"] = "PayPal"
            prompt_text = "Por favor, escribe el **correo de PayPal** a donde quieras que te envíen el dinero."
            info_key = "user_paypal_email"
        elif cid == "exchange_pay_paysafecard":
            self.exchange_info["pay"] = "Paysafecard"
            prompt_text = "Por favor, envía la **información de Paysafecard** (código o datos)."
            info_key = "user_paysafecard_info"
        elif cid == "exchange_pay_bizum":
            self.exchange_info["pay"] = "Bizum"
            prompt_text = "Por favor, escribe el **número de teléfono** (Bizum) a donde quieras que te envíen el dinero."
            info_key = "user_bizum_number"
        else:
            self.exchange_info["pay"] = "Desconocido"
            prompt_text = "Método de pago desconocido."
            info_key = "user_unknown"

        await interaction.response.defer()

        self.prompt_msg = await interaction.channel.send(prompt_text)

        def check(m: discord.Message):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            self.user_input_msg = await bot.wait_for("message", timeout=120, check=check)

            self.exchange_info[info_key] = self.user_input_msg.content

            await self.cleanup()

            await interaction.followup.edit_message(
                message_id=interaction.message.id,
                content="Selecciona la cantidad a intercambiar (€):",
                view=ExchangeAmountView(self.channel, self.user, self.exchange_info)
            )

        except asyncio.TimeoutError:
            await self.cleanup()
            await interaction.followup.send(
                "No recibí tu información a tiempo. Vuelve a pulsar el método de pago para intentarlo de nuevo.",
                ephemeral=True
            )

    async def go_back(self, interaction: discord.Interaction):
        await self.cleanup()

        await interaction.response.edit_message(
            content="Elige en dónde quieres recibir el dinero:",
            embed=None,
            view=ExchangeReceiveView(self.channel, self.user, self.exchange_info)
        )

class ExchangeAmountView(View):
    def __init__(self, channel, user, exchange_info: dict):
        super().__init__(timeout=None)
        self.channel = channel
        self.user = user
        self.exchange_info = exchange_info

        cantidades = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        for c in cantidades:
            label = f"{c}€"
            button = Button(label=label, style=discord.ButtonStyle.primary, custom_id=f"exchange_amount_{c}")
            button.callback = self.select_amount
            self.add_item(button)

        self.back_button = Button(label="Atrás", style=discord.ButtonStyle.secondary, custom_id="exchange_amount_back")
        self.back_button.callback = self.go_back
        self.add_item(self.back_button)

    async def select_amount(self, interaction: discord.Interaction):
        cantidad_str = interaction.data["custom_id"].split("_")[-1]
        try:
            cantidad = int(cantidad_str)
        except ValueError:
            await interaction.response.send_message("Cantidad no válida.", ephemeral=True)
            return

        self.exchange_info["amount"] = cantidad

        pay = self.exchange_info.get("pay")
        receive = self.exchange_info.get("receive")

        pairs_5_percent = {
            ("PayPal", "Paysafecard"),
            ("PayPal", "Bizum"),
            ("Paysafecard", "Bizum")
        }

        if frozenset([pay, receive]) in [frozenset(x) for x in pairs_5_percent]:
            calculated = round(cantidad * 0.95, 2)
        elif ((pay == "LTC" and receive in ["PayPal", "Paysafecard", "Bizum"]) or
              (receive == "LTC" and pay in ["PayPal", "Paysafecard", "Bizum"])):
            tabla = {10: 9.3, 20: 18.6, 30: 27.9, 40: 37.2, 50: 46.5,
                     60: 56.4, 70: 65.8, 80: 75.2, 90: 84.6, 100: 95}
            calculated = tabla.get(cantidad, 0)
        else:
            calculated = cantidad

        self.exchange_info["calculated"] = calculated

        embed = discord.Embed(
            title=f"**{pay} → {receive}**",
            description=(
                f"Envia el dinero a: **{self.get_instructions(pay)}**\n\n"
                f"- Debes pagar: **{cantidad}€**\n"
                f"- Vas a recibir: **{calculated}€**\n\n"
                "Recuerda que una vez hecho el pedido **no se reembolsa**."
            ),
            color=discord.Color.green()
        )
        await interaction.response.edit_message(
            content="Si todo es correcto, pulsa el botón de abajo:",
            embed=embed,
            view=ExchangeSummaryView(self.channel, self.user, self.exchange_info)
        )

    def get_instructions(self, pay_method: str) -> str:
        if pay_method == "PayPal":
            return "https://www.paypal.me/KayyShop (enviar como amigos y familiares)"
        elif pay_method == "LTC":
            return "LdJG7Cq8eAVe5uFVuoo8uWsS6ES6jyq5Qw"
        elif pay_method == "Paysafecard":
            return "Envía los códigos Paysafecard en el chat (solo de España)"
        elif pay_method == "Bizum":
            return "+34 602 53 12 05"
        else:
            return "Información de pago no definida"

    async def go_back(self, interaction: discord.Interaction):
        await interaction.response.edit_message(
            content="Ahora, ¿por dónde vas a pagar?",
            embed=None,
            view=ExchangePayView(self.channel, self.user, self.exchange_info)
        )


class ExchangeSummaryView(View):
    def __init__(self, channel, user, exchange_info: dict):
        super().__init__(timeout=None)
        self.channel = channel
        self.user = user
        self.exchange_info = exchange_info

        self.confirm_button = Button(
            label="Pulsame una vez hayas pagado",
            style=discord.ButtonStyle.success,
            custom_id="exchange_confirm_payment"
        )
        self.confirm_button.callback = self.confirm_payment
        self.add_item(self.confirm_button)

        self.back_button = Button(
            label="Atrás",
            style=discord.ButtonStyle.secondary,
            custom_id="exchange_summary_back"
        )
        self.back_button.callback = self.go_back
        self.add_item(self.back_button)

        self.close_ticket_button = Button(
            label="Cerrar Ticket",
            style=discord.ButtonStyle.danger,
            custom_id="exchange_summary_close_ticket"
        )
        self.close_ticket_button.callback = self.close_ticket
        self.add_item(self.close_ticket_button)

    async def confirm_payment(self, interaction: discord.Interaction):
        await interaction.response.defer()

        pay_method = self.exchange_info.get("pay", "Desconocido")

        if pay_method == "PayPal":
            info_key = "user_paypal_email"
        elif pay_method == "LTC":
            info_key = "user_ltc_wallet"
        elif pay_method == "Paysafecard":
            info_key = "user_paysafecard_info"
        elif pay_method == "Bizum":
            info_key = "user_bizum_number"
        else:
            info_key = "user_unknown"

        info_value = self.exchange_info.get(info_key, "No se encontró información")

        embed = discord.Embed(
            title="Pago confirmado",
            description=(
                f"**Método de pago:** {pay_method}\n"
                f"**Información del usuario:** `{info_value}`\n\n"
                "Muchas gracias por confiar, espera a que un agente atienda tu ticket. "
                "Si tienes alguna pregunta o información adicional, escríbela aquí."
            ),
            color=discord.Color.blue()
        )
        await self.channel.send(embed=embed)

        admin_id = 399876603229896704
        mention_admin = f"<@{admin_id}> " * 3
        await self.channel.send(
            f"{mention_admin}\n"
            f"El usuario {interaction.user.mention} ha confirmado que va a realizar el pago."
        )

    async def go_back(self, interaction: discord.Interaction):
        await interaction.response.edit_message(
            content="Selecciona la cantidad a intercambiar (€):",
            embed=None,
            view=ExchangeAmountView(self.channel, self.user, self.exchange_info)
        )

    async def close_ticket(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await self.channel.delete()

    def get_instructions(self, pay_method: str) -> str:
        if pay_method == "PayPal":
            return "https://www.paypal.me/KayyShop (enviar como amigos y familiares)"
        elif pay_method == "LTC":
            return "LdJG7Cq8eAVe5uFVuoo8uWsS6ES6jyq5Qw"
        elif pay_method == "Paysafecard":
            return "Envía los códigos Paysafecard en el chat (solo de España)"
        elif pay_method == "Bizum":
            return "+34 602 53 12 05"
        else:
            return "Información de pago no definida"

class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())


class TicketSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="👤 Comprar Seguidores", value="buy_followers"),
            discord.SelectOption(label="💱 Exchange", value="exchange"),
            discord.SelectOption(label="🎉 Comprar Bits", value="buy_bits"),
            discord.SelectOption(label="💰 Comprar Cuenta", value="buy_account"),
            discord.SelectOption(label="📺 Espectadores TikTok En Directo", value="live_viewers_tiktok"),
            discord.SelectOption(label="💎 Comprar Rol Premiun", value="Premiun"),
            discord.SelectOption(label="❓ Otra cosa", value="other"),
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
            await send_followers_image(ticket_channel, member)
            await ticket_channel.send("Selecciona la plataforma para seguidores:", view=PersistentPlatformSelectView())

        elif self.values[0] == "live_viewers_tiktok":
            await send_live_viewers_image(ticket_channel)
            await ticket_channel.send("Selecciona la duración del stream:", view=LiveDurationView())

        elif self.values[0] == "exchange":
            await send_exchange_image(ticket_channel)
            exchange_info = {}
            await ticket_channel.send("Has seleccionado **Exchange**.\nElige en dónde quieres recibir el dinero:", view=ExchangeReceiveView(ticket_channel, member, exchange_info))

        elif self.values[0] == "buy_bits":
            await send_buy_bits_image(ticket_channel)
            await ticket_channel.send("Selecciona la cantidad de bits que deseas comprar:", view=BuyBitsView())

        else:
            close_ticket_button = Button(label="Cerrar Ticket", style=discord.ButtonStyle.danger, custom_id="cerrar_ticket_general")
            close_ticket_view = View(timeout=None)
            close_ticket_view.add_item(close_ticket_button)

            async def close_ticket(interaction: discord.Interaction):
                await interaction.response.defer()
                await ticket_channel.delete()

            close_ticket_button.callback = close_ticket
            await ticket_channel.send("Un moderador atenderá su ticket lo más rápido posible.")
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
        description=(
            "Abre un ticket si estás interesado en cualquier producto o tienes alguna pregunta.\n\n"
            "Si deseas una asistencia más rápida, escribe a este número: **+34 622 02 75 87**"
        ),
        color=discord.Color.green()
    )
    embed_intro.set_footer(text="Ticket Tool Created By Kayy")

    view = TicketView()
    bot.add_view(view)

    await canal.send(embed=embed_intro, view=view)
    print(f"Botón de creación de ticket enviado al canal: {canal.name}")

bot.run('EL TOKEN DE TU BOT DE DISCORD')
