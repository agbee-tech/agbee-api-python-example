import json
import requests
from dotenv import load_dotenv
import os
import flet as ft
import threading


load_dotenv()

Authorization_URL = os.getenv("Authorization_URL")
api_key = os.getenv("API_KEY")
AGBEE_USERNAME = os.getenv("AGBEE_USERNAME")
AGBEE_PASSWORD = os.getenv("AGBEE_PASSWORD")
API_URL = os.getenv("API_URL")

def get_token():
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json",
    }
    payload = {
        "username": AGBEE_USERNAME,
        "password": AGBEE_PASSWORD
    }
    response = requests.post(Authorization_URL + "token", headers=headers, data=json.dumps(payload))
    return response

def call_appsync_api_example(id_token):
    headers = {
        "Authorization": id_token
    }
    # GraphQLクエリ。例えば、GraphQLのqueryやmutationなど
    graphql_query = {
        "query": """query MyQuery {
            listDevices {
                items {
                id
                name
                ownerID
                uuid
                SKU
                firmwareVersion
                status
                mode
                bumper
                vbumper
                estop
                temperature
                batteryPercent
                createdAt
                updatedAt
                }
            }
        }"""
    }
    response = requests.post(API_URL, json=graphql_query, headers=headers)
    return response.json()

def main(page: ft.Page):
    page.title = "agbee status viewer"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.bgcolor = ft.colors.WHITE
    page.padding = 20
    page.spacing = 20
    textbox_width = 300
    label_width = 150

    txt_input_name = ft.TextField(
        value="", 
        text_align=ft.TextAlign.RIGHT, 
        width=textbox_width,
        bgcolor=ft.colors.TEAL_100,
        border_radius=5,
    )
    txt_id = ft.TextField(
        value="", 
        text_align=ft.TextAlign.RIGHT, 
        width=textbox_width,
        bgcolor=ft.colors.TEAL_100,
        border_radius=5,
    )
    txt_name = ft.TextField(
        value="", 
        text_align=ft.TextAlign.RIGHT, 
        width=textbox_width,
        bgcolor=ft.colors.TEAL_100,
        border_radius=5,
    )
    txt_ownerID = ft.TextField(
        value="", 
        text_align=ft.TextAlign.RIGHT, 
        width=textbox_width,
        bgcolor=ft.colors.TEAL_100,
        border_radius=5,
    )
    txt_uuid = ft.TextField(
        value="", 
        text_align=ft.TextAlign.RIGHT, 
        width=textbox_width,
        bgcolor=ft.colors.TEAL_100,
        border_radius=5,
    )
    txt_SKU = ft.TextField(
        value="", 
        text_align=ft.TextAlign.RIGHT, 
        width=textbox_width,
        bgcolor=ft.colors.TEAL_100,
        border_radius=5,
    )
    txt_firmwareVersion = ft.TextField(
        value="", 
        text_align=ft.TextAlign.RIGHT, 
        width=textbox_width,
        bgcolor=ft.colors.TEAL_100,
        border_radius=5,
    )
    txt_status = ft.TextField(
        value="", 
        text_align=ft.TextAlign.RIGHT, 
        width=textbox_width,
        bgcolor=ft.colors.TEAL_100,
        border_radius=5,
    )
    txt_mode = ft.TextField(
        value="", 
        text_align=ft.TextAlign.RIGHT, 
        width=textbox_width,
        bgcolor=ft.colors.TEAL_100,
        border_radius=5,
    )
    txt_bumper = ft.TextField(
        value="", 
        text_align=ft.TextAlign.RIGHT, 
        width=textbox_width,
        bgcolor=ft.colors.TEAL_100,
        border_radius=5,
    )
    txt_vbumper = ft.TextField(
        value="", 
        text_align=ft.TextAlign.RIGHT, 
        width=textbox_width,
        bgcolor=ft.colors.TEAL_100,
        border_radius=5,
    )
    txt_estop = ft.TextField(
        value="", 
        text_align=ft.TextAlign.RIGHT, 
        width=textbox_width,
        bgcolor=ft.colors.TEAL_100,
        border_radius=5,
    )
    txt_temperature = ft.TextField(
        value="", 
        text_align=ft.TextAlign.RIGHT, 
        width=textbox_width,
        bgcolor=ft.colors.TEAL_100,
        border_radius=5,
    )
    txt_batteryPercent = ft.TextField(
        value="", 
        text_align=ft.TextAlign.RIGHT, 
        width=textbox_width,
        bgcolor=ft.colors.TEAL_100,
        border_radius=5,
    )
    txt_createdAt = ft.TextField(
        value="", 
        text_align=ft.TextAlign.RIGHT, 
        width=textbox_width,
        bgcolor=ft.colors.TEAL_100,
        border_radius=5,
    )
    txt_updatedAt = ft.TextField(
        value="", 
        text_align=ft.TextAlign.RIGHT, 
        width=textbox_width,
        bgcolor=ft.colors.TEAL_100,
        border_radius=5,
    )
    
    toggle_switch = ft.Switch(value=False)
    txt_interval = ft.TextField(
        value="5", 
        text_align=ft.TextAlign.RIGHT, 
        width=100,
        bgcolor=ft.colors.TEAL_100,
        border_radius=5,
    )
    

    def refresh_click(e=None): 
        auth_response = get_token()
        if auth_response.status_code == 200:
            tokens = json.loads(auth_response.text)
            response = call_appsync_api_example(tokens["IdToken"])
            print(response)
            for item in response["data"]["listDevices"]["items"]:
                if item["name"] == txt_input_name.value:
                    txt_id.value = item["id"]
                    txt_name.value = item["name"]
                    txt_ownerID.value = item["ownerID"]
                    txt_uuid.value = item["uuid"]
                    txt_SKU.value = item["SKU"]
                    txt_firmwareVersion.value = item["firmwareVersion"]
                    txt_status.value = item["status"]
                    txt_mode.value = item["mode"]
                    txt_bumper.value = item["bumper"]
                    txt_vbumper.value = item["vbumper"]
                    txt_estop.value = item["estop"]
                    txt_temperature.value = item["temperature"]
                    txt_batteryPercent.value = item["batteryPercent"]
                    txt_createdAt.value = item["createdAt"]
                    txt_updatedAt.value = item["updatedAt"]

                    page.update()
        else:
            print(auth_response)
            
    refresh_thread = None
    stop_event = threading.Event()

    def auto_refresh():
        while not stop_event.is_set():
            refresh_click()
            stop_event.wait(int(txt_interval.value))

    def toggle_changed(e):
        nonlocal refresh_thread, stop_event
        if toggle_switch.value:
            stop_event.clear()
            refresh_thread = threading.Thread(target=auto_refresh, daemon=True)
            refresh_thread.start()
        else:
            stop_event.set()
            if refresh_thread:
                refresh_thread.join()
    

    view = ft.Column(
        width=800,
        controls=[
            ft.Row(
                controls=[
                    ft.Text(value="Input your agbee name", size=20, weight=ft.FontWeight.BOLD),
                    txt_input_name,
                    ft.IconButton(ft.icons.REFRESH, on_click=refresh_click, icon_color=ft.colors.BLUE, icon_size=30)
                ],
            ),
            ft.Row(
                controls=[
                    ft.Text(value="Auto Refresh Interval (seconds):", size=18, weight=ft.FontWeight.BOLD),
                    txt_interval,
                    toggle_switch
                ],
            ),
            
            ft.Divider(height=20), # 区切り線を追加
            ft.Row(controls=[ft.Container(ft.Text(value="id", size=18, weight=ft.FontWeight.BOLD), width=label_width), txt_id]),
            ft.Row(controls=[ft.Container(ft.Text(value="name", size=18, weight=ft.FontWeight.BOLD), width=label_width), txt_name]),
            ft.Row(controls=[ft.Container(ft.Text(value="ownerID", size=18, weight=ft.FontWeight.BOLD), width=label_width), txt_ownerID]),
            ft.Row(controls=[ft.Container(ft.Text(value="uuid", size=18, weight=ft.FontWeight.BOLD), width=label_width), txt_uuid]),
            ft.Row(controls=[ft.Container(ft.Text(value="SKU", size=18, weight=ft.FontWeight.BOLD), width=label_width), txt_SKU]),
            ft.Row(controls=[ft.Container(ft.Text(value="firmwareVersion", size=18, weight=ft.FontWeight.BOLD), width=label_width), txt_firmwareVersion]),
            ft.Row(controls=[ft.Container(ft.Text(value="status", size=18, weight=ft.FontWeight.BOLD), width=label_width), txt_status]),
            ft.Row(controls=[ft.Container(ft.Text(value="mode", size=18, weight=ft.FontWeight.BOLD), width=label_width), txt_mode]),
            ft.Row(controls=[ft.Container(ft.Text(value="bumper", size=18, weight=ft.FontWeight.BOLD), width=label_width), txt_bumper]),
            ft.Row(controls=[ft.Container(ft.Text(value="vbumper", size=18, weight=ft.FontWeight.BOLD), width=label_width), txt_vbumper]),
            ft.Row(controls=[ft.Container(ft.Text(value="estop", size=18, weight=ft.FontWeight.BOLD), width=label_width), txt_estop]),
            ft.Row(controls=[ft.Container(ft.Text(value="temperature", size=18, weight=ft.FontWeight.BOLD), width=label_width), txt_temperature]),
            ft.Row(controls=[ft.Container(ft.Text(value="batteryPercent", size=18, weight=ft.FontWeight.BOLD), width=label_width), txt_batteryPercent]),
            ft.Row(controls=[ft.Container(ft.Text(value="createdAt", size=18, weight=ft.FontWeight.BOLD), width=label_width), txt_createdAt]),
            ft.Row(controls=[ft.Container(ft.Text(value="updatedAt", size=18, weight=ft.FontWeight.BOLD), width=label_width), txt_updatedAt]),
        ],
    )
    
    toggle_switch.on_change = toggle_changed
    
    scroll_view = ft.ListView(
        expand=True,
        controls=[view],
    )
    page.add( 
        scroll_view
    )

ft.app(target=main)

