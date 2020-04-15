import arcade

class TheGame(arcade.Window):  
    
    def on_key_press(self, key, modifiers):
        pass
    def on_key_release(self, key, modifiers):
        pass

    def another_game_function(self):
        pass


    def on_update(self, deltatime):
        """
        Huvudfunktion för uppdateringar av HELA spel-loopen.
        Placera all uppdatering av spellogik här
        Alltså här skriver du in ordning för när
        alla spelobjekt ska uppdateras.
        """
        pass
    def on_draw(self, deltatime):
        """
        Huvudfunktion för utritningar av ALLA spelobjekt.
        Ordningen saker ritas på spelar stor roll.
        Ritar du exempelvis bakgrund sist, så är
        bakgrunden överst! Ordningen spelar roll.
        """
        pass