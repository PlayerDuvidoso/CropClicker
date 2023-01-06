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
        
        def cropUpgrade(self, e):
            with open(cropsStorage) as f:
                cropBag = json.load(f)
                self.cropValue = int(cropBag[str(self.cropLevel+1)]['value'])
                self.cropName = cropBag[str(self.cropLevel+1)]['name']
                self.cropText.value = f'{self.cropName}: ${self.cropValue}'
                self.displayCrop.src = f'/images/{str(self.cropName)}.png'
                self.cropLevel+=1
                print(self.cropLevel)
                currentShop.updateShop(e=1)
                self.update()
        
        def getNextCrop(self, e):
            with open(cropsStorage) as f:
                cropBag = json.load(f)
                nextCropName = cropBag[str(self.cropLevel+1)]['name']
                nextCropPrice = int(cropBag[str(self.cropLevel+1)]['price'])
                nextCropValue = int(cropBag[str(self.cropLevel+1)]['value'])
                nextCropImage = f'/images/{str(nextCropName)}.png'
                return nextCropName, nextCropPrice, nextCropValue, nextCropImage
    
    class Shop(ft.UserControl):
        def __init__(self):
            super().__init__()

        def build(self):
            self.nextCropName, self.nextCropPrice, self.nextCropValue, self.nextCropImage = currentCrop.getNextCrop(e=1)
            self.nextCropInfo = ft.Text(f'{self.nextCropName}: ${self.nextCropValue}', text_align=ft.TextAlign.CENTER, width=100)
            self.nextCropImageShop = ft.Image(src=self.nextCropImage, width=100, height=100)
            self.upgradeBtnTxt = ft.Text(f'Upgrade: ${self.nextCropPrice}', size=12, text_align=ft.TextAlign.CENTER)
            self.upgradeBtn = ft.FilledButton(content=ft.Row(alignment=ft.MainAxisAlignment.START, controls=[self.upgradeBtnTxt]), on_click=self.upgradeClick, width=100)
            
            self.shopTitle = ft.Container(width=200, content=ft.Text('Shop', text_align=ft.TextAlign.CENTER), border_radius=5, border=ft.border.all(1, color='#06283D'))
            
            self.cropInfo = ft.Column(alignment=ft.MainAxisAlignment.CENTER, width=100, controls=[self.nextCropInfo, self.nextCropImageShop, self.upgradeBtn])
            self.cropContainer = ft.Container(alignment=ft.alignment.center, width=200, content=self.cropInfo, border=ft.border.all(width=2), border_radius=5)


            self.displayShop = ft.Column(alignment=ft.MainAxisAlignment.CENTER, width=200, controls=[self.shopTitle, self.cropContainer])
            return self.displayShop
        
        def upgradeClick(self, e):
            if currentPlayer.getMoney() >= self.nextCropPrice:
                currentCrop.cropUpgrade(e=1)
                currentPlayer.delMoney(self.nextCropPrice)

                self.nextCropName, self.nextCropPrice, self.nextCropValue, self.nextCropImage = currentCrop.getNextCrop(e=1)
                self.nextCropInfo.value = f'{self.nextCropName}: ${self.nextCropValue}'
                self.nextCropImageShop.src = self.nextCropImage
                self.upgradeBtn.text = f'Upgrade: {self.nextCropPrice}'

                self.update()
        
        def updateShop(self, e):
                self.nextCropName, self.nextCropPrice, self.nextCropValue, self.nextCropImage = currentCrop.getNextCrop(e=1)
                self.nextCropInfo.value = f'{self.nextCropName}: ${self.nextCropValue}'
                self.nextCropImageShop.src = self.nextCropImage
                self.upgradeBtnTxt.value = f'Upgrade: {self.nextCropPrice}'
                self.update()

                

    currentShop = Shop()
    currentPlayer = Player()
    currentCrop = Crop(1, f"/images/Carrot.png", 'Carrot')

    def moneyCheat(e):
        currentPlayer.addMoney(100)

    page.add(ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[currentPlayer, ft.ElevatedButton(text='Upgrade Crop', icon=ft.icons.KEYBOARD_DOUBLE_ARROW_UP, on_click=currentCrop.cropUpgrade), ft.ElevatedButton(text='Money Cheat', icon=ft.icons.ADD, on_click=moneyCheat)]),
    ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[currentCrop]),
    ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[currentShop]))


ft.app(target=main, assets_dir="assets")