import flet as ft
import json

cropsStorage = 'assets/CropsStorage.json'

def main(page: ft.Page):
    page.title = "Crop Clicker"

    class Player(ft.UserControl):
        def __init__(self, playerMoney=0, playerMultipler=1):
            super().__init__()
            self.playerMoney = playerMoney
            self.playerMultiplier = playerMultipler
        
        def build(self):
            self.displayText = ft.Text(f'${self.playerMoney}')
            self.displayMoney = ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[self.displayText])
            return self.displayMoney

        def getMoney(self):
            return self.playerMoney

        def addMoney(self, value):
            self.playerMoney += value*self.playerMultiplier
            self.displayText.value = f'${self.playerMoney}'
            self.update()
        
        def delMoney(self, value):
            self.playerMoney -= value
            self.displayText.value = f'${self.playerMoney}'
            self.update()

    class Crop(ft.UserControl):
        def __init__(self, cropValue, cropImage, cropName, cropLevel=1):
            super().__init__()
            self.cropValue = cropValue
            self.cropImage = cropImage
            self.cropName = cropName
            self.cropLevel = cropLevel

        def build(self):
            self.cropText = ft.Text(f'{self.cropName}: ${self.cropValue}')
            self.displayCrop = ft.Image(self.cropImage)
            self.displayCrop.width=200
            self.displayCrop.height=160

            self.cropObject = ft.Column(controls=[
                ft.Container(content=self.displayCrop, on_click=self.crop_click, width=200, height=160, image_fit=ft.ImageFit.NONE),
                ft.Row(width=200, alignment=ft.MainAxisAlignment.CENTER, controls=[self.cropText])])
            return self.cropObject
    
        def crop_click(self, e):
            currentPlayer.addMoney(currentCrop.cropValue)
            print(currentPlayer.getMoney())
        
        def cropUpdate(self, e):
            with open(cropsStorage) as f:
                cropBag = json.load(f)
                self.cropValue = int(cropBag[str(self.cropLevel+1)]['value'])
                self.cropName = cropBag[str(self.cropLevel+1)]['name']
                self.cropText.value = f'{self.cropName}: ${self.cropValue}'
                self.displayCrop.src = f'/images/{str(self.cropName)}.png'
                self.cropLevel+=1
                print(self.cropLevel)
                self.update()
    
    currentPlayer = Player()
    currentCrop = Crop(1, f"/images/Carrot.png", 'Carrot')

    page.add(ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[currentPlayer, ft.ElevatedButton(text='Upgrade Crop', icon=ft.icons.KEYBOARD_DOUBLE_ARROW_UP, on_click=currentCrop.cropUpdate)]),
    ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[currentCrop]))


ft.app(target=main, assets_dir="assets")